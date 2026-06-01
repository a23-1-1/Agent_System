#!/usr/bin/env python3
"""
execution-workflow — 执行演示工作流引擎

职责：
  将 SQL + EXPLAIN 结果转换为标准步骤 DAG，
  输出与 DemoPackage / DemoStep schema 兼容的结构。

工作流阶段（sql-execution）：
  lex → parse → optimize → plan → execute → result

输入：
  sql: str — 用户输入的 SQL
  mysql_explain: dict — MySQL EXPLAIN JSON
  pg_explain: dict — PostgreSQL EXPLAIN JSON

输出：
  ExecutionWorkflowIR — 完整步骤 DAG

使用：
  python workflow.py "SELECT ..."           # 仅解析 SQL
  python workflow.py "SELECT ..." --explain  # 接 db-engine 真实 EXPLAIN
"""

from __future__ import annotations
import json
import re
import sys
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


# ═══════════════════════════════════════════════════════════════
# 1. 数据结构（对齐 ai-workflow.md 中的 ExecutionWorkflowIR）
# ═══════════════════════════════════════════════════════════════

@dataclass
class WorkflowPhase:
    id: str
    order: int
    phase: str                                # lex | parse | optimize | plan | execute | result
    label_zh: str = ""
    label_en: str = ""
    engine_evidence: dict = field(default_factory=dict)


@dataclass
class ExplainSnapshot:
    query: str = ""
    plan: Optional[dict] = None
    error: Optional[str] = None


@dataclass
class StepMapping:
    step_id: str
    phase: str
    explain_node_id: Optional[str] = None


@dataclass
class ExecutionWorkflowIR:
    workflow_id: str
    sql: str
    phases: list[WorkflowPhase] = field(default_factory=list)
    engine_plans: dict = field(default_factory=lambda: {"mysql": None, "postgres": None})
    step_mapping: list[StepMapping] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
# 2. SQL 解析器（用 sqlparse 提取关键信息）
# ═══════════════════════════════════════════════════════════════

PHASE_LABELS = {
    "lex":     {"zh": "词法分析", "en": "Lexical Analysis"},
    "parse":   {"zh": "语法分析", "en": "Parsing"},
    "optimize":{"zh": "查询优化", "en": "Query Optimization"},
    "plan":    {"zh": "执行计划", "en": "Execution Plan"},
    "execute": {"zh": "执行过程", "en": "Execution"},
    "result":  {"zh": "结果集",   "en": "Result Set"},
    "concept": {"zh": "概念",     "en": "Concept"},
}

# SQL 关键字 → phase 映射
LEX_PATTERN = re.compile(
    r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|FROM|WHERE|JOIN|'
    r'INNER|LEFT|RIGHT|FULL|ON|AND|OR|GROUP|BY|ORDER|HAVING|LIMIT|OFFSET)\b',
    re.IGNORECASE
)


def get_sql_type(sql: str) -> str:
    """判断 SQL 类型：SELECT / INSERT / UPDATE / DELETE / OTHER"""
    sql = sql.strip().upper()
    for kw in ("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"):
        if sql.startswith(kw):
            return kw
    return "OTHER"


def extract_tables(sql: str) -> list[str]:
    """简单提取表名（位于 FROM/JOIN/UPDATE/INTO 之后）"""
    from re import findall, IGNORECASE
    # 匹配 FROM/JOIN 后的表名
    tables = findall(r'(?:FROM|JOIN|UPDATE|INTO)\s+(\w+)', sql, IGNORECASE)
    # 去重但保持顺序
    seen = set()
    result = []
    for t in tables:
        if t.lower() not in seen:
            seen.add(t.lower())
            result.append(t)
    return result


def has_join(sql: str) -> bool:
    """是否包含 JOIN"""
    return bool(re.search(r'\bJOIN\b', sql, re.IGNORECASE))


def has_where(sql: str) -> bool:
    """是否包含 WHERE"""
    return bool(re.search(r'\bWHERE\b', sql, re.IGNORECASE))


def has_group_by(sql: str) -> bool:
    """是否包含 GROUP BY"""
    return bool(re.search(r'\bGROUP\s+BY\b', sql, re.IGNORECASE))


def has_order_by(sql: str) -> bool:
    """是否包含 ORDER BY"""
    return bool(re.search(r'\bORDER\s+BY\b', sql, re.IGNORECASE))


def estimate_scan_type(sql: str, explain_json: Optional[dict]) -> str:
    """从 EXPLAIN JSON 中推断扫描类型"""
    if not explain_json:
        return "unknown"

    plan = explain_json
    # MySQL EXPLAIN FORMAT=JSON 结构
    if "query_block" in str(plan):
        plan_str = json.dumps(plan).lower()
        if "full table scan" in plan_str or "table_scan" in plan_str:
            return "full_table_scan"
        if "index" in plan_str and "lookup" in plan_str:
            return "index_lookup"
        if "nested_loop" in plan_str or "nestedloop" in plan_str:
            return "nested_loop_join"
        if "hash_join" in plan_str or "hashjoin" in plan_str:
            return "hash_join"
        if "index_only" in plan_str or "covering" in plan_str:
            return "index_only_scan"
    return "unknown"


# ═══════════════════════════════════════════════════════════════
# 3. 工作流引擎
# ═══════════════════════════════════════════════════════════════

class ExecutionWorkflowEngine:
    """SQL 执行工作流引擎 — 解析 SQL → 编排步骤 DAG"""

    def __init__(self, sql: str, mysql_explain: Optional[dict] = None, pg_explain: Optional[dict] = None):
        self.sql = sql.strip()
        self.mysql_explain = mysql_explain
        self.pg_explain = pg_explain
        self.sql_type = get_sql_type(sql)
        self.tables = extract_tables(sql)
        self._ir: Optional[ExecutionWorkflowIR] = None

    def build(self) -> ExecutionWorkflowIR:
        phases: list[WorkflowPhase] = []
        mapping: list[StepMapping] = []

        # Step 1: lex — 词法分析
        tokens_found = LEX_PATTERN.findall(self.sql)
        phases.append(WorkflowPhase(
            id="phase_lex", order=1, phase="lex",
            label_zh=f"词法分析 — 识别 {len(tokens_found)} 个关键字",
            label_en=f"Lexical Analysis — {len(tokens_found)} tokens found",
            engine_evidence={"token_count": len(tokens_found), "tokens": list(set(tokens_found))}
        ))
        mapping.append(StepMapping(step_id="step_1", phase="lex"))

        # Step 2: parse — 语法分析
        sql_ast_desc = f"{self.sql_type} 查询"
        if self.tables:
            sql_ast_desc += f"，涉及表: {', '.join(self.tables)}"
        if has_join(self.sql):
            sql_ast_desc += "，包含 JOIN"
        if has_where(self.sql):
            sql_ast_desc += "，含 WHERE 条件"
        phases.append(WorkflowPhase(
            id="phase_parse", order=2, phase="parse",
            label_zh=f"语法分析 — {sql_ast_desc}",
            label_en=f"Parsing — {sql_ast_desc}",
            engine_evidence={
                "tables": self.tables,
                "has_join": has_join(self.sql),
                "has_where": has_where(self.sql),
                "has_group_by": has_group_by(self.sql),
                "has_order_by": has_order_by(self.sql),
            }
        ))
        mapping.append(StepMapping(step_id="step_2", phase="parse"))

        # Step 3: optimize — 查询优化
        scan_type = estimate_scan_type(self.sql, self.mysql_explain)
        if has_join(self.sql):
            optimize_desc = "JOIN 策略选择"
        elif self.tables:
            optimize_desc = f"扫描方式选择 ({scan_type})"
        else:
            optimize_desc = "执行策略选择"
        phases.append(WorkflowPhase(
            id="phase_optimize", order=3, phase="optimize",
            label_zh=f"查询优化 — {optimize_desc}",
            label_en=f"Query Optimization — {optimize_desc}",
            engine_evidence={"scan_type": scan_type, "table_count": len(self.tables)}
        ))
        mapping.append(StepMapping(step_id="step_3", phase="optimize"))

        # Step 4: plan — 执行计划（依赖 EXPLAIN）
        plan_info = {"mysql_cost": None, "pg_cost": None}
        if self.mysql_explain:
            plan_info["mysql_cost"] = self.mysql_explain.get("query_block", {}).get("cost", None) if isinstance(self.mysql_explain, dict) else None
        if self.pg_explain:
            pg_plan = self.pg_explain.get("Plan", {}) if isinstance(self.pg_explain, dict) else {}
            plan_info["pg_cost"] = pg_plan.get("Total Cost", None) if pg_plan else None

        phases.append(WorkflowPhase(
            id="phase_plan", order=4, phase="plan",
            label_zh=f"执行计划 — {scan_type.replace('_', ' ')}",
            label_en=f"Execution Plan — {scan_type.replace('_', ' ')}",
            engine_evidence=plan_info
        ))
        mapping.append(StepMapping(
            step_id="step_4", phase="plan",
            explain_node_id="mysql_explain.node_001" if self.mysql_explain else None
        ))

        # Step 5: execute — 执行过程
        row_estimate = None
        if self.mysql_explain and isinstance(self.mysql_explain, dict):
            qb = self.mysql_explain.get("query_block", {})
            row_estimate = qb.get("table", {}).get("rows_examined_per_join", None) if isinstance(qb, dict) else None
        phases.append(WorkflowPhase(
            id="phase_execute", order=5, phase="execute",
            label_zh=f"执行过程 — 扫描数据并应用条件",
            label_en=f"Execution — Scanning data and applying filters",
            engine_evidence={"rows_estimate": row_estimate}
        ))
        mapping.append(StepMapping(
            step_id="step_5", phase="execute",
            explain_node_id="mysql_explain.node_001" if self.mysql_explain else None
        ))

        # Step 6: result — 结果集
        phases.append(WorkflowPhase(
            id="phase_result", order=6, phase="result",
            label_zh="返回结果集",
            label_en="Return Result Set",
        ))
        mapping.append(StepMapping(step_id="step_6", phase="result"))

        self._ir = ExecutionWorkflowIR(
            workflow_id=f"wf_{abs(hash(self.sql)) % 10**8:08d}",
            sql=self.sql,
            phases=phases,
            engine_plans={
                "mysql": ExplainSnapshot(query=self.sql, plan=self.mysql_explain).__dict__,
                "postgres": ExplainSnapshot(query=self.sql, plan=self.pg_explain).__dict__,
            },
            step_mapping=mapping,
        )
        return self._ir

    def to_demo_package_steps(self) -> list[dict]:
        """将 IR 转换为 DemoStep 列表（可直接喂给 Player）"""
        if not self._ir:
            self.build()
        steps = []
        for phase in self._ir.phases:
            step = {
                "id": f"wfstep_{phase.order}",
                "order": phase.order,
                "workflowPhase": phase.phase,
                "narration": {
                    "zh": f"【{phase.label_zh}】",
                    "en": f"[{phase.label_en}]",
                    "source": "ai",
                },
                "visuals": {"type": "highlight-sql"},
                "groundingRef": None,
            }
            # 如果是 plan/execute 步骤且有 explain_node_id，加上 grounding
            for mapping in self._ir.step_mapping:
                if mapping.step_id == f"step_{phase.order}" and mapping.explain_node_id:
                    step["groundingRef"] = mapping.explain_node_id
                    break
            steps.append(step)
        return steps


# ═══════════════════════════════════════════════════════════════
# 4. CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    sql = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "parse"

    mysql_exp = None
    pg_exp = None

    if mode == "--explain":
        # 尝试连接 db-engine
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "db-engine"))
            from connector import explain_both
            result = explain_both(sql)
            mysql_exp = result.get("mysql")
            pg_exp = result.get("postgres")
            print(f"[db-engine] MySQL EXPLAIN: {'OK' if mysql_exp and 'error' not in mysql_exp else 'FAIL'}")
            print(f"[db-engine] PG EXPLAIN: {'OK' if pg_exp and 'error' not in pg_exp else 'FAIL'}")
        except ImportError:
            print("[!] db-engine connector 不可用，跳过真实 EXPLAIN")
        except Exception as e:
            print(f"[!] db-engine 错误: {e}")

    engine = ExecutionWorkflowEngine(sql, mysql_exp, pg_exp)
    ir = engine.build()
    steps = engine.to_demo_package_steps()

    print(f"\n{'='*50}")
    print(f"  Workflow IR")
    print(f"{'='*50}")
    print(f"  ID:    {ir.workflow_id}")
    print(f"  SQL:   {ir.sql[:80]}{'...' if len(ir.sql)>80 else ''}")
    print(f"  类型:  {sql}")
    print(f"  表:    {', '.join(engine.tables) if engine.tables else '(无)'}")
    print(f"  阶段:  {len(ir.phases)} 步")
    print()

    for p in ir.phases:
        print(f"  [{p.order}] {p.phase:10s}  {p.label_zh}")

    print(f"\n{'='*50}")
    print(f"  DemoPackage Steps（可直接用于 Player）")
    print(f"{'='*50}")
    print(json.dumps(steps, indent=2, ensure_ascii=False))

    print(f"\n{'='*50}")
    print(f"  完整 IR")
    print(f"{'='*50}")
    # 序列化时不输出过长的 plan 内容
    ir_dict = asdict(ir)
    for eng in ("mysql", "postgres"):
        if ir_dict.get("engine_plans", {}).get(eng, {}).get("plan"):
            ir_dict["engine_plans"][eng]["plan"] = "(truncated)"
    print(json.dumps(ir_dict, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
