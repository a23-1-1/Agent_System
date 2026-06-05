#!/usr/bin/env python3
"""
sql_simulator — 为 SQL 演示生成过程模拟器数据（中间结果表）

输出格式对齐 DemoPackage.simulationData.sqlSimulator
"""

from __future__ import annotations
import re
from typing import Any


# 教学用示例数据（JOIN 经典案例）
_JOIN_SAMPLE = {
    "students": [
        {"id": 1, "name": "Alice", "major": "CS"},
        {"id": 2, "name": "Bob", "major": "Math"},
        {"id": 3, "name": "Carol", "major": "CS"},
    ],
    "courses": [
        {"course_id": 101, "course_name": "Database Systems", "student_id": 1},
        {"course_id": 102, "course_name": "Algorithms", "student_id": 1},
        {"course_id": 103, "course_name": "Linear Algebra", "student_id": 2},
    ],
}


def _has_join(sql: str) -> bool:
    return bool(re.search(r"\bJOIN\b", sql, re.IGNORECASE))


def _select_columns(sql: str) -> list[str]:
    m = re.search(r"SELECT\s+(.+?)\s+FROM", sql, re.IGNORECASE | re.DOTALL)
    if not m:
        return ["*"]
    raw = m.group(1)
    cols = []
    for part in raw.split(","):
        part = part.strip()
        alias = part.split()[-1].split(".")[-1] if part else part
        cols.append(alias or part)
    return cols or ["*"]


def build_sql_simulator(sql: str, analysis: dict | None = None) -> dict[str, Any]:
    """
    根据 SQL 生成 sqlSimulator 步骤列表。
    当前支持：含 JOIN 的 SELECT；简单 SELECT 退化为单表扫描。
    """
    sql = (sql or "").strip()
    if not sql.upper().startswith("SELECT"):
        return {"steps": []}

    analysis = analysis or {}
    tables = analysis.get("tables") or []
    if _has_join(sql):
        return _build_join_simulator(sql, tables)
    return _build_simple_select_simulator(sql, tables)


def _build_join_simulator(sql: str, tables: list) -> dict[str, Any]:
    students = _JOIN_SAMPLE["students"]
    courses = _JOIN_SAMPLE["courses"]
    joined = [
        {**s, "course_id": c["course_id"], "course_name": c["course_name"], "student_id": c["student_id"]}
        for s in students
        for c in courses
        if s["id"] == c["student_id"]
    ]
    out_cols = _select_columns(sql)
    final_rows = []
    for row in joined:
        item = {}
        for col in out_cols:
            if col in row:
                item[col] = row[col]
            elif col == "name" and "name" in row:
                item[col] = row["name"]
            elif "course" in col.lower() and "course_name" in row:
                item[col] = row["course_name"]
        if item:
            final_rows.append(item)
    if not final_rows:
        final_rows = [{"name": r["name"], "course_name": r["course_name"]} for r in joined]

    steps = [
        {
            "clause": "FROM students s",
            "description": "读取驱动表 students，获得基础行集",
            "intermediateRows": len(students),
            "columns": list(students[0].keys()),
            "rows": students,
        },
        {
            "clause": "INNER JOIN courses c",
            "description": "引入 courses 表，准备按连接键匹配",
            "intermediateRows": len(courses),
            "columns": list(courses[0].keys()),
            "rows": courses,
        },
        {
            "clause": "ON s.id = c.student_id",
            "description": "按 ON 条件过滤，只保留匹配的行",
            "intermediateRows": len(joined),
            "columns": ["name", "course_name", "student_id"],
            "rows": [
                {"name": r["name"], "course_name": r["course_name"], "student_id": r["student_id"]}
                for r in joined
            ],
        },
        {
            "clause": "SELECT " + ", ".join(out_cols),
            "description": "投影最终输出列，形成结果集",
            "intermediateRows": len(final_rows),
            "columns": out_cols,
            "rows": final_rows,
        },
    ]
    return {"steps": steps}


def _build_simple_select_simulator(sql: str, tables: list) -> dict[str, Any]:
    table = tables[0] if tables else "t"
    rows = _JOIN_SAMPLE["students"][:2]
    cols = list(rows[0].keys()) if rows else ["col1"]
    steps = [
        {
            "clause": f"FROM {table}",
            "description": f"扫描表 {table}",
            "intermediateRows": len(rows),
            "columns": cols,
            "rows": rows,
        },
        {
            "clause": "SELECT " + ", ".join(_select_columns(sql)),
            "description": "投影并返回结果",
            "intermediateRows": len(rows),
            "columns": _select_columns(sql),
            "rows": [{c: r.get(c, "") for c in _select_columns(sql)} for r in rows],
        },
    ]
    return {"steps": steps}


if __name__ == "__main__":
    import json
    import sys

    sample = (
        "SELECT s.name, c.course_name FROM students s "
        "INNER JOIN courses c ON s.id = c.student_id"
    )
    q = sys.argv[1] if len(sys.argv) > 1 else sample
    print(json.dumps(build_sql_simulator(q), ensure_ascii=False, indent=2))
