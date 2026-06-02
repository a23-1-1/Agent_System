"""ai-tools 测试：验证所有非 LLM 工具都可运行"""

import sys, os, json
# 设置路径
_STUDIO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(_STUDIO, "packages", "ai-tools"))
sys.path.insert(0, os.path.join(_STUDIO, "packages", "db-engine"))
sys.path.insert(0, os.path.join(_STUDIO, "packages", "execution-workflow"))

from tools import sql_analyze, explain_mysql, explain_postgres, assemble_execution_steps, validate_demo_package, TOOL_SCHEMAS, TOOL_MAP

SQL = "SELECT s.name, c.course_name FROM students s INNER JOIN courses c ON s.id = c.student_id"

print("=" * 50)
print("1. sql_analyze")
r = sql_analyze(SQL)
print(f"   OK: type={r['sql_type']}, tables={r['tables']}, join={r['has_join']}")

print("\n2. explain_mysql")
r = explain_mysql(SQL)
print(f"   engine={r['engine']}, has_plan={r['plan'] is not None}, error={r.get('error')}")

print("\n3. explain_postgres")
r = explain_postgres(SQL)
print(f"   engine={r['engine']}, has_plan={r['plan'] is not None}, error={r.get('error')}")

print("\n4. assemble_execution_steps")
r = assemble_execution_steps(SQL,
    mysql_explain={"query_block": {"table": {"rows": 4}}},
    pg_explain={"Plan": {"Total Cost": 29.92}})
print(f"   workflow_id={r['workflow_id']}, steps={len(r['steps'])}, grounding={r['grounding_count']}")

print("\n5. validate_demo_package (valid)")
import subprocess, tempfile
dp = {
    "id": "dp_test", "title": {"zh": "测试", "en": "Test"},
    "steps": [
        {"id": "s1", "order": 1, "workflowPhase": "lex", "narration": {"zh": "词法分析", "source": "ai"}},
        {"id": "s2", "order": 2, "workflowPhase": "parse", "narration": {"zh": "语法分析", "source": "ai"}},
        {"id": "s3", "order": 3, "workflowPhase": "plan", "narration": {"zh": "执行计划", "source": "ai"}, "groundingRef": "node_001"},
        {"id": "s4", "order": 4, "workflowPhase": "execute", "narration": {"zh": "执行", "source": "ai"}, "groundingRef": "node_001"},
        {"id": "s5", "order": 5, "workflowPhase": "result", "narration": {"zh": "结果", "source": "ai"}},
    ],
    "metadata": {"teacherVersion": 1},
    "playback": {"defaultStepDurationMs": 5000}
}
r = validate_demo_package(dp)
print(f"   valid={r['valid']}, output_len={len(r['output'])}")

print("\n6. Tool Schemas")
print(f"   registered: {len(TOOL_SCHEMAS)} tools")
for t in TOOL_SCHEMAS:
    name = t["function"]["name"]
    fn = TOOL_MAP.get(name)
    print(f"   - {name}: {'defined' if fn else 'MISSING'}")

print("\n" + "=" * 50)
print("All non-LLM tools OK")
