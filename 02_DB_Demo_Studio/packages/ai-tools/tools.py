#!/usr/bin/env python3
"""
packages/ai-tools — LLM 可调工具集

职责：
  - 注册所有 DB Demo Studio 专用工具
  - 提供 DeepSeek Function Calling 兼容的 Tool Schema
  - 每个工具独立可测试

工具清单（对齐 ai-workflow.md §5）：
  - explain_mysql         : MySQL EXPLAIN JSON
  - explain_postgres      : PostgreSQL EXPLAIN JSON
  - sql_analyze           : SQL 语法检查 + 提取表名/关键字
  - assemble_execution_steps : EXPLAIN + IR → DemoStep[]
  - validate_demo_package : Schema/grounding 校验
  - generate_narration    : DeepSeek LLM 生成讲解词
  - generate_visual_spec  : 生成动画脚本 VisualSpec
  - translate_bilingual   : 中英互译
"""

from __future__ import annotations
import json
import sys
import os
from typing import Optional, Callable

# ── 路径 hack：让 ai-tools 引用同仓库模块 ──
_PKG_DIR = os.path.dirname(os.path.abspath(__file__))          # .../packages/ai-tools/
_STUDIO_DIR = os.path.dirname(os.path.dirname(_PKG_DIR))      # .../02_DB_Demo_Studio/
sys.path.insert(0, os.path.join(_STUDIO_DIR, "packages", "db-engine"))
sys.path.insert(0, os.path.join(_STUDIO_DIR, "packages", "execution-workflow"))

from connector import explain_both, get_mysql, get_pg, JOIN_SQL
from workflow import ExecutionWorkflowEngine


# ═══════════════════════════════════════════════════════════════
# 1. 工具定义
# ═══════════════════════════════════════════════════════════════

def explain_mysql(sql: str = JOIN_SQL) -> dict:
    """执行 MySQL EXPLAIN，返回 ExplainSnapshot"""
    try:
        m = get_mysql()
        m.connect()
        plan = m.explain(sql)
        m.close()
        return {"query": sql, "plan": plan, "error": None, "engine": "mysql"}
    except Exception as e:
        return {"query": sql, "plan": None, "error": str(e), "engine": "mysql"}


def explain_postgres(sql: str = JOIN_SQL) -> dict:
    """执行 PostgreSQL EXPLAIN，返回 ExplainSnapshot"""
    try:
        p = get_pg()
        p.connect()
        plan = p.explain(sql)
        p.close()
        return {"query": sql, "plan": plan, "error": None, "engine": "postgres"}
    except Exception as e:
        return {"query": sql, "plan": None, "error": str(e), "engine": "postgres"}


def sql_analyze(sql: str) -> dict:
    """SQL 语法检查 + 提取关键信息（词法/表名/类型）"""
    from workflow import (
        LEX_PATTERN, get_sql_type, extract_tables,
        has_join, has_where, has_group_by, has_order_by
    )
    tokens = LEX_PATTERN.findall(sql)
    return {
        "sql_type": get_sql_type(sql),
        "tables": extract_tables(sql),
        "tokens_found": len(tokens),
        "keywords": list(set(tokens)),
        "has_join": has_join(sql),
        "has_where": has_where(sql),
        "has_group_by": has_group_by(sql),
        "has_order_by": has_order_by(sql),
        "is_valid": get_sql_type(sql) != "OTHER",
    }


def assemble_execution_steps(sql: str, mysql_explain: Optional[dict] = None, pg_explain: Optional[dict] = None) -> dict:
    """将 SQL + EXPLAIN → ExecutionWorkflowIR → DemoStep[]"""
    engine = ExecutionWorkflowEngine(sql, mysql_explain, pg_explain)
    ir = engine.build()
    steps = engine.to_demo_package_steps()
    from dataclasses import asdict
    return {
        "workflow_id": ir.workflow_id,
        "steps": steps,
        "phase_count": len(ir.phases),
        "grounding_count": sum(1 for s in steps if s.get("groundingRef")),
    }


def validate_demo_package(dp: dict) -> dict:
    """对 DemoPackage 进行 Schema/grounding 校验"""
    import subprocess
    validate_py = os.path.join(_STUDIO_DIR, "packages", "demo-schema", "validate.py")

    # 临时写入
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(dp, f, ensure_ascii=False)
        tmp_path = f.name

    result = subprocess.run(
        [sys.executable, validate_py, tmp_path],
        capture_output=True, text=True, timeout=10
    )
    os.unlink(tmp_path)

    return {
        "valid": result.returncode == 0,
        "output": result.stdout[-500:] if result.stdout else "",
        "errors": result.stderr if result.stderr else None,
    }


def generate_narration(step_context: dict, style: str = "大学本科数据库课程", api_key: Optional[str] = None) -> dict:
    """调用 DeepSeek LLM 生成单步讲解词（zh + en）

    step_context: {"phase": "plan", "sql": "...", "explain_summary": "...", "tables": [...]}
    """
    if not api_key:
        api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return {"zh": f"[需要 DEEPSEEK_API_KEY] 步骤: {step_context.get('phase', '')}", "en": f"[Need DEEPSEEK_API_KEY] step: {step_context.get('phase', '')}", "source": "ai"}

    from openai import OpenAI
    client = OpenAI(
        base_url="https://api.deepseek.com",
        api_key=api_key,
    )

    phase = step_context.get("phase", "")
    sql = step_context.get("sql", "")
    explain = step_context.get("explain_summary", "")
    tables = step_context.get("tables", [])

    prompt = f"""你是大学数据库课程的助教，请为以下 SQL 执行演示的「{phase}」阶段写讲解词。

SQL: {sql}
涉及表: {', '.join(tables) if tables else '(自动分析)'}
EXPLAIN 摘要: {explain if explain else '(无)'}

要求：
1. 面向{style}学生，语言通俗易懂
2. {phase} 阶段的核心概念必须解释清楚
3. 输出 JSON 格式：{{"zh": "中文讲解", "en": "English narration"}}
4. zh 字数 80-150 字，en 对应翻译
5. 如果 EXPLAIN 有数据，必须引用具体信息"""

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=500,
        )
        content = resp.choices[0].message.content
        result = json.loads(content)
        result["source"] = "ai"
        result["tokens_used"] = resp.usage.total_tokens if resp.usage else 0
        return result
    except Exception as e:
        return {"zh": f"[AI 生成失败: {e}] 步骤: {phase}", "en": f"[AI failed: {e}] step: {phase}", "source": "ai"}


def generate_visual_spec(step_context: dict, api_key: Optional[str] = None) -> dict:
    """生成动画脚本 VisualSpec"""
    if not api_key:
        api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return {"type": "highlight-sql", "description": "默认高亮 SQL", "source": "template"}

    from openai import OpenAI
    client = OpenAI(base_url="https://api.deepseek.com", api_key=api_key)

    prompt = f"""为数据库课程演示的某个步骤设计动画脚本。
步骤信息: {json.dumps(step_context, ensure_ascii=False)}

可选类型: highlight-sql, plan-tree, table-result, er-diagram, concept-flow
输出 JSON: {{"type": "可视化类型", "highlightRange": [start, end] (仅highlight-sql), "description": "动画描述", "duration": 建议时长秒数}}"""

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.5,
            max_tokens=300,
        )
        result = json.loads(resp.choices[0].message.content)
        result["source"] = "ai"
        result["tokens_used"] = resp.usage.total_tokens if resp.usage else 0
        return result
    except Exception as e:
        return {"type": "highlight-sql", "description": str(e), "source": "fallback"}


def translate_bilingual(text: str, target_lang: str = "en", api_key: Optional[str] = None) -> dict:
    """中英互译"""
    if not api_key:
        api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return {"original": text, "translated": text, "source": "no_key"}

    from openai import OpenAI
    client = OpenAI(base_url="https://api.deepseek.com", api_key=api_key)

    prompt = f"将以下文本翻译为{'英文' if target_lang == 'en' else '中文'}，保持教学风格。只返回翻译结果：\n{text}"

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300,
        )
        return {
            "original": text,
            "translated": resp.choices[0].message.content.strip(),
            "source": "ai",
            "tokens_used": resp.usage.total_tokens if resp.usage else 0,
        }
    except Exception as e:
        return {"original": text, "translated": text, "source": f"error: {e}"}


# ═══════════════════════════════════════════════════════════════
# 2. Tool Schema（DeepSeek Function Calling 兼容）
# ═══════════════════════════════════════════════════════════════

TOOL_SCHEMAS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "explain_mysql",
            "description": "对 MySQL 执行 EXPLAIN 分析，返回执行计划 JSON。用于 grounding SQL 演示步骤，防止幻觉。",
            "parameters": {
                "type": "object",
                "properties": {"sql": {"type": "string", "description": "要分析的 SQL 语句"}},
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "explain_postgres",
            "description": "对 PostgreSQL 执行 EXPLAIN 分析，返回执行计划 JSON。与 explain_mysql 对照使用。",
            "parameters": {
                "type": "object",
                "properties": {"sql": {"type": "string", "description": "要分析的 SQL 语句"}},
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sql_analyze",
            "description": "解析 SQL 语句：提取表名、关键字、判断类型（SELECT/INSERT/...）",
            "parameters": {
                "type": "object",
                "properties": {"sql": {"type": "string"}},
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "assemble_execution_steps",
            "description": "根据 SQL 和 EXPLAIN 结果，生成标准 6 步执行演示 DAG。输出与 DemoStep Schema 兼容。",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {"type": "string"},
                    "mysql_explain": {"type": "object", "description": "MySQL EXPLAIN JSON（可选）"},
                    "pg_explain": {"type": "object", "description": "PostgreSQL EXPLAIN JSON（可选）"},
                },
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "validate_demo_package",
            "description": "校验 DemoPackage 的结构、枚举、grounding 约束。SQL 类的 plan/execute 步必须有 groundingRef。",
            "parameters": {
                "type": "object",
                "properties": {"dp": {"type": "object", "description": "完整的 DemoPackage JSON"}},
                "required": ["dp"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_narration",
            "description": "用 LLM 为单个演示步骤生成中英双语讲解词",
            "parameters": {
                "type": "object",
                "properties": {
                    "step_context": {"type": "object", "description": "含 phase/sql/explain_summary/tables"},
                    "style": {"type": "string", "default": "大学本科数据库课程"},
                },
                "required": ["step_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_visual_spec",
            "description": "为演示步骤生成动画脚本（VisualSpec）",
            "parameters": {
                "type": "object",
                "properties": {"step_context": {"type": "object"}},
                "required": ["step_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "translate_bilingual",
            "description": "中英/英中翻译",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "target_lang": {"type": "string", "enum": ["en", "zh"]},
                },
                "required": ["text"],
            },
        },
    },
]

# ── 工具名 → 函数映射 ──
TOOL_MAP: dict[str, Callable] = {
    "explain_mysql": explain_mysql,
    "explain_postgres": explain_postgres,
    "sql_analyze": sql_analyze,
    "assemble_execution_steps": assemble_execution_steps,
    "validate_demo_package": validate_demo_package,
    "generate_narration": generate_narration,
    "generate_visual_spec": generate_visual_spec,
    "translate_bilingual": translate_bilingual,
}


# ═══════════════════════════════════════════════════════════════
# 3. CLI 测试入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python tools.py <tool_name> [args...]")
        print(f"可用工具: {', '.join(TOOL_MAP.keys())}")
        sys.exit(1)

    tool = sys.argv[1]
    if tool not in TOOL_MAP:
        print(f"未知工具: {tool}")
        sys.exit(1)

    func = TOOL_MAP[tool]
    kw = {}
    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                kw[k] = v
            else:
                kw["sql"] = arg

    result = func(**kw) if kw else func()
    print(json.dumps(result, indent=2, ensure_ascii=False))
