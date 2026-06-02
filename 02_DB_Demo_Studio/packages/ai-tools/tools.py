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
# Docker 中通过 PYTHONPATH 环境变量注入，本地开发通过 sys.path fallback
_PKG_DIR = os.path.dirname(os.path.abspath(__file__))
_STUDIO_DIR = os.path.dirname(os.path.dirname(_PKG_DIR))
if "packages" not in sys.path[0] if sys.path else False:
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
    """生成单步讲解词（zh + en）— 有 DEEPSEEK_API_KEY 时调 LLM，否则用规则模板

    step_context: {"phase": "plan", "sql": "...", "explain_summary": "...", "tables": [...], "engine_evidence": {...}}
    """
    api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return _rule_narration(step_context)

    from openai import OpenAI
    client = OpenAI(base_url="https://api.deepseek.com", api_key=api_key)

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
        return _rule_narration(step_context)


def _rule_narration(ctx: dict) -> dict:
    """无 API key 时，基于 engineEvidence 生成有意义的规则化讲解词"""
    phase = ctx.get("phase", "")
    sql = ctx.get("sql", "")
    ev = ctx.get("engine_evidence", {}) or {}
    sql_type = "查询" if sql.strip().upper().startswith("SELECT") else "操作"

    templates = {
        "lex": lambda: _lex_narration(sql, ev),
        "parse": lambda: _parse_narration(sql, ev),
        "optimize": lambda: _optimize_narration(ev),
        "plan": lambda: _plan_narration(ev),
        "execute": lambda: _execute_narration(ev),
        "result": lambda: _result_narration(sql, sql_type),
    }
    fn = templates.get(phase)
    if fn:
        return {**fn(), "source": "rule"}
    return {
        "zh": f"正在执行 {sql_type} 的「{phase}」阶段。",
        "en": f"Executing the {phase} phase of the {sql_type}.",
        "source": "rule",
    }


def _lex_narration(sql: str, ev: dict) -> dict:
    tokens = ev.get("tokens", [])
    count = ev.get("token_count", len(tokens))
    token_str = "、".join(tokens[:8]) if tokens else "关键字"
    return {
        "zh": f"SQL 解析器首先对语句进行词法分析，将输入的文本拆分为有意义的单词（Token）。"
              f"本条 SQL 共识别出 {count} 个关键字，包括 {token_str} 等。"
              f"词法分析是数据库执行 SQL 的第一步，它负责识别 SELECT、FROM、WHERE 等保留字，"
              f"以及表名、列名等标识符，为后续的语法分析奠定基础。",
        "en": f"The SQL parser first performs lexical analysis, splitting the input text into meaningful tokens. "
              f"This query contains {count} keywords, including {token_str}. "
              f"Lexical analysis is the first step of SQL execution — it identifies reserved words "
              f"like SELECT, FROM, WHERE, as well as identifiers such as table and column names.",
    }


def _parse_narration(sql: str, ev: dict) -> dict:
    tables = ev.get("tables", [])
    features = []
    if ev.get("has_join"): features.append("JOIN 连接")
    if ev.get("has_where"): features.append("WHERE 条件过滤")
    if ev.get("has_group_by"): features.append("GROUP BY 分组")
    if ev.get("has_order_by"): features.append("ORDER BY 排序")
    feature_str = "，".join(features) if features else "基本查询"

    table_str = "、".join(tables) if tables else "相关表"
    return {
        "zh": f"语法分析阶段检查 SQL 语句是否符合数据库的语法规则，并构建抽象语法树（AST）。"
              f"本条 SQL 涉及表「{table_str}」，包含 {feature_str}。"
              f"语法分析器会验证表名和列名是否存在、数据类型是否匹配、"
              f"以及 JOIN 条件中的关联字段是否类型兼容等语义约束。",
        "en": f"The parsing phase checks whether the SQL conforms to the database grammar rules "
              f"and builds an Abstract Syntax Tree (AST). "
              f"This query involves table(s) «{table_str}», with {feature_str}. "
              f"The parser validates table/column existence, data type compatibility, "
              f"and JOIN condition field type consistency.",
    }


SCAN_LABELS = {
    "full_table_scan": "全表扫描",
    "index_lookup": "索引查找",
    "index_only_scan": "索引覆盖扫描",
    "nested_loop_join": "嵌套循环连接",
    "hash_join": "哈希连接",
}


def _optimize_narration(ev: dict) -> dict:
    scan = ev.get("scan_type", "unknown")
    scan_zh = SCAN_LABELS.get(scan, scan.replace("_", " "))
    table_count = ev.get("table_count", "?")

    explanations = {
        "full_table_scan": "这意味着数据库将逐行扫描整张表。对于小表来说这是高效的，但大表上应尽量避免。",
        "index_lookup": "数据库将通过索引树快速定位数据行，而非逐行扫描。这通常能显著减少 I/O 次数。",
        "index_only_scan": "所有需要的数据都在索引中，无需回表访问数据行，这是最高效的访问方式之一。",
        "nested_loop_join": "对于驱动表的每一行，数据库会到被驱动表中查找匹配行。当驱动表较小且被驱动表有索引时效率很高。",
        "hash_join": "数据库为较小的表构建内存哈希表，然后扫描大表进行匹配。适用于两表均较大且无合适索引的场景。",
    }
    explain = explanations.get(scan, "优化器根据统计信息选择了合适的执行策略。")

    return {
        "zh": f"查询优化器根据表统计信息和系统配置，评估多种可能的执行计划并选择代价最小的方案。"
              f"当前选择的扫描方式为「{scan_zh}」，涉及 {table_count} 张表。{explain}",
        "en": f"The query optimizer evaluates multiple execution strategies based on table statistics "
              f"and system configuration, selecting the plan with the lowest estimated cost. "
              f"The chosen scan method is «{scan_zh}», involving {table_count} table(s).",
    }


def _plan_narration(ev: dict) -> dict:
    mysql_cost = ev.get("mysql_cost")
    pg_cost = ev.get("pg_cost")
    cost_detail = ""
    if mysql_cost is not None:
        cost_detail += f"MySQL 估计代价为 {mysql_cost}。"
    if pg_cost is not None:
        cost_detail += f" PostgreSQL 估计代价为 {pg_cost}。"

    if not cost_detail:
        cost_detail = "代价估算需要数据库连接提供 EXPLAIN 数据。"

    return {
        "zh": f"执行计划是数据库优化器产出的最终操作指令序列，描述了如何访问表、使用哪些索引、"
              f"按什么顺序执行 JOIN 等具体步骤。{cost_detail}"
              f"执行计划中的代价单位是数据库内部的抽象度量，综合考虑了 I/O、CPU 和内存开销。",
        "en": f"The execution plan is the optimizer's final set of operation instructions — "
              f"describing how to access tables, which indexes to use, "
              f"and in what order to perform JOIN operations. {cost_detail} "
              f"The cost unit is an abstract metric combining I/O, CPU, and memory overhead.",
    }


def _execute_narration(ev: dict) -> dict:
    rows = ev.get("rows_estimate")
    row_detail = f"优化器估计需要扫描约 {rows:,} 行数据。" if rows is not None else ""

    return {
        "zh": f"执行器按照执行计划逐步执行各操作节点。{row_detail}"
              f"执行过程会涉及缓冲池读取、索引遍历、数据行过滤、临时表创建等实际数据库操作。"
              f"实际扫描行数可能与估计值有出入，这取决于统计信息的准确性和运行时条件。",
        "en": f"The executor walks through each operation node per the execution plan. {row_detail}"
              f"The execution involves buffer pool reads, index traversal, row filtering, "
              f"and temporary table creation. Actual rows scanned may differ from estimates "
              f"depending on statistics accuracy and runtime conditions.",
    }


def _result_narration(sql: str, sql_type: str) -> dict:
    return {
        "zh": f"执行完成，返回 {sql_type} 的结果集。"
              f"结果集由数据库以行（row）和列（column）的形式返回给客户端。"
              f"对于 SELECT 查询，结果集包含查询命中的所有数据行；"
              f"对于 INSERT / UPDATE / DELETE，则返回影响的行数。",
        "en": f"Execution complete, returning the {sql_type} result set. "
              f"The result set is returned to the client as rows and columns. "
              f"For SELECT queries, it contains the matching data rows; "
              f"for INSERT / UPDATE / DELETE, it returns the number of affected rows.",
    }


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
