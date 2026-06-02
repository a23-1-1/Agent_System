#!/usr/bin/env python3
"""
apps/api — FastAPI 后端

路由：
  POST   /api/ai/chat                  SSE 流式对话
  POST   /api/ai/regenerate-step       单步重写
  GET    /api/demos/:id                获取演示
  GET    /api/demos/:id/export/mp4     导出 MP4

依赖（需要安装）：
  pip install fastapi uvicorn sse-starlette
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
import sys
import os
import asyncio

# 让 api 引用同仓库的 ai-tools
_STUDIO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# _STUDIO_DIR = .../02_DB_Demo_Studio/apps  → 再上一级
_STUDIO_ROOT = os.path.dirname(_STUDIO_DIR)
sys.path.insert(0, os.path.join(_STUDIO_ROOT, "packages", "ai-tools"))
sys.path.insert(0, os.path.join(_STUDIO_ROOT, "packages", "db-engine"))
sys.path.insert(0, os.path.join(_STUDIO_ROOT, "packages", "execution-workflow"))

from tools import (
    sql_analyze, explain_mysql, explain_postgres,
    assemble_execution_steps, validate_demo_package,
    generate_narration, TOOL_MAP, TOOL_SCHEMAS,
)
from workflow import ExecutionWorkflowEngine

app = FastAPI(title="DB Demo Studio API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段全放行
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════

class ChatRequest(BaseModel):
    message: str
    sql: Optional[str] = None
    curriculum_node: Optional[str] = None
    demo_id: Optional[str] = None


class RegenerateRequest(BaseModel):
    demo_id: str
    step_id: str
    hint: Optional[str] = None


class DemoOut(BaseModel):
    id: str
    title: dict
    steps: list
    metadata: dict
    playback: dict


# ═══════════════════════════════════════════════
# 演示流水线
# ═══════════════════════════════════════════════

def _build_demo_from_sql(sql: str, message: str, curriculum_node: Optional[str] = None) -> dict:
    """SQL + 对话 → DemoPackage"""

    # Step 1: SQL 分析
    analysis = sql_analyze(sql)

    # Step 2: 双引擎 EXPLAIN
    mysql_exp = explain_mysql(sql)
    pg_exp = explain_postgres(sql)

    # Step 3: 组装步骤 DAG
    mysql_plan = mysql_exp.get("plan") if mysql_exp.get("plan") and "error" not in mysql_exp else None
    pg_plan = pg_exp.get("plan") if pg_exp.get("plan") and "error" not in pg_exp else None

    ir_result = assemble_execution_steps(sql, mysql_plan, pg_plan)
    steps = ir_result.get("steps", [])

    # Step 4: LLM 生成讲解词（如果 API Key 可用）
    for step in steps:
        ctx = {
            "phase": step.get("workflowPhase", ""),
            "sql": sql,
            "tables": analysis.get("tables", []),
            "explain_summary": str(mysql_plan)[:200] if mysql_plan else "",
        }
        narration = generate_narration(ctx)
        step["narration"] = {
            "zh": narration.get("zh", f"[{step['workflowPhase']}]"),
            "en": narration.get("en", f"[{step['workflowPhase']}]"),
            "source": narration.get("source", "ai"),
        }

    # 组装 DemoPackage
    engine_compare = {
        "mysql": {"query": sql, "plan": mysql_plan, "error": mysql_exp.get("error")},
        "postgres": {"query": sql, "plan": pg_plan, "error": pg_exp.get("error")},
    }

    dp = {
        "id": f"dp_{abs(hash(sql)) % 10**8:08d}",
        "title": {
            "zh": curriculum_node or analysis.get("tables", ["SQL 演示"])[0] + " 执行过程",
            "en": (curriculum_node or "SQL Demo") + " Execution",
        },
        "steps": steps,
        "workflowTrace": {
            "workflowId": ir_result.get("workflow_id", ""),
            "workflowType": "sql-execution",
            "aiSessionId": "session_001",
        },
        "engineCompare": engine_compare,
        "metadata": {
            "aiDraftVersion": "ai-v1",
            "teacherVersion": 1,
            "lastAiAction": "full-generate",
        },
        "playback": {"defaultStepDurationMs": 5000},
    }

    # 校验
    v_result = validate_demo_package(dp)
    dp["_validation"] = {"valid": v_result["valid"], "errors": v_result.get("errors")}

    return dp


# ═══════════════════════════════════════════════
# 路由
# ═══════════════════════════════════════════════

@app.get("/api/health")
def health():
    return {"status": "ok", "tools": len(TOOL_MAP)}


@app.get("/api/tools")
def tools():
    return {"tools": TOOL_SCHEMAS}


@app.post("/api/ai/chat")
async def chat(req: ChatRequest):
    """SSE 流式对话"""
    sql = req.sql or req.message
    import re
    sql_match = re.search(r'(SELECT|INSERT|UPDATE|DELETE|CREATE).*', req.message, re.IGNORECASE | re.DOTALL)
    if sql_match:
        sql = sql_match.group(0).strip()

    async def event_stream():
        try:
            # 发送分析中的事件
            yield f"data: {json.dumps({'type': 'assistant-text', 'content': '正在分析 SQL 并生成执行计划...'})}\n\n"
            await asyncio.sleep(0.1)

            # 执行完整流水线
            dp = _build_demo_from_sql(sql, req.message, req.curriculum_node)

            # 发送每个步骤的预览
            for step in dp.get("steps", []):
                yield f"data: {json.dumps({'type': 'step-preview', 'step': step})}\n\n"
                await asyncio.sleep(0.05)

            # 发送完成事件
            yield f"data: {json.dumps({'type': 'demo-updated', 'demo': dp})}\n\n"
            yield f"data: {json.dumps({'type': 'demo-complete', 'demo_id': dp['id']})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/demos/{demo_id}")
def get_demo(demo_id: str):
    """获取已生成的演示"""
    demo_path = os.path.join(_STUDIO_DIR, "packages", "demo-schema", "examples", f"{demo_id}.json")
    if os.path.exists(demo_path):
        with open(demo_path, encoding="utf-8") as f:
            return json.load(f)
    raise HTTPException(404, f"演示 {demo_id} 不存在")


if __name__ == "__main__":
    import uvicorn
    print("Starting DB Demo Studio API...")
    print(f"  Health: http://localhost:8000/api/health")
    print(f"  Chat SSE: POST http://localhost:8000/api/ai/chat")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
