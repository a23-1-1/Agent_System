"""
apps/api — FastAPI 后端

路由：
  GET    /api/health                   健康检查
  GET    /api/tools                    工具列表

  # 对话管理
  GET    /api/conversations            对话列表
  POST   /api/conversations            创建对话
  GET    /api/conversations/{id}       对话详情
  PATCH  /api/conversations/{id}       更新对话
  DELETE /api/conversations/{id}       删除对话
  GET    /api/conversations/{id}/messages  消息历史

  # 演示
  POST   /api/ai/chat                  SSE 流式对话（向后兼容）
  GET    /api/demos/{demo_id}          获取演示

  # WebSocket（核心）
  WS     /ws/chat                      双向对话协议

依赖（需要安装）：
  pip install fastapi uvicorn python-dotenv pymysql psycopg2-binary redis
"""

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import sys
import os
import asyncio
import time
import re
import uuid
from dotenv import load_dotenv
from typing import Optional

_APP_DIR = os.path.dirname(os.path.abspath(__file__))          # apps/api/
_STUDIO_DIR = os.path.dirname(os.path.dirname(_APP_DIR))       # apps/ 或项目根
_STUDIO_ROOT = os.path.dirname(_STUDIO_DIR)                    # 项目根

# Load .env — 可能在 _STUDIO_ROOT 也可能在 _STUDIO_DIR（本地 vs Docker）
_env_path = os.path.join(_STUDIO_ROOT, ".env")
if not os.path.exists(_env_path):
    _env_path = os.path.join(_STUDIO_DIR, ".env")
load_dotenv(_env_path)

# 让 api 引用同仓库的 packages
for pkg in ["ai-tools", "db-engine", "execution-workflow"]:
    sys.path.insert(0, os.path.join(_STUDIO_ROOT, "packages", pkg))

from tools import (
    sql_analyze, explain_mysql, explain_postgres,
    assemble_execution_steps, validate_demo_package,
    generate_narration, TOOL_MAP, TOOL_SCHEMAS,
)
from apps.api.redis_client import ping as redis_ping, cache_message, get_cached_messages

app = FastAPI(title="DB Demo Studio API", version="5.0")

# CORS — allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════
# In-memory Conversation Store (will use Redis later)
# ═══════════════════════════════════════════════

conversations: dict = {}
messages: dict[str, list] = {}  # convId -> list of messages
conversation_order: list = []  # sorted list of convIds by recency


def _create_conv(title: str = "新对话") -> dict:
    conv_id = f"conv_{uuid.uuid4().hex[:12]}"
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    conv = {
        "id": conv_id,
        "title": title,
        "status": "active",
        "demoType": "standard",
        "messageCount": 0,
        "lastActivity": now,
        "summary": "",
        "tags": [],
    }
    conversations[conv_id] = conv
    messages[conv_id] = []
    conversation_order.insert(0, conv_id)
    return conv


# Create a default conversation
_create_conv("JOIN 查询讲解")


# ═══════════════════════════════════════════════
# 演示流水线（复用 ai-tools）
# ═══════════════════════════════════════════════

def _normalize_plan(raw: dict) -> dict | None:
    plan = raw.get("plan")
    if plan and not raw.get("error"):
        if isinstance(plan, dict):
            if "EXPLAIN" in plan:
                try:
                    return json.loads(plan["EXPLAIN"])
                except (json.JSONDecodeError, TypeError):
                    return plan
            if "query_block" in plan or (len(plan) == 1 and isinstance(list(plan.values())[0], str)):
                return plan
            return plan
    return None


def _build_demo_from_sql(sql: str, message: str = "", curriculum_node: str = None) -> dict:
    """SQL + 对话 → DemoPackage"""
    analysis = sql_analyze(sql)
    mysql_exp = explain_mysql(sql)
    pg_exp = explain_postgres(sql)

    mysql_plan = _normalize_plan(mysql_exp)
    pg_plan = _normalize_plan(pg_exp)

    ir_result = assemble_execution_steps(sql, mysql_plan, pg_plan)
    steps = ir_result.get("steps", [])

    for step in steps:
        ctx = {
            "phase": step.get("workflowPhase", ""),
            "sql": sql,
            "tables": analysis.get("tables", []),
            "explain_summary": str(mysql_plan)[:200] if mysql_plan else "",
            "engine_evidence": step.get("engineEvidence", {}),
        }
        narration = generate_narration(ctx)
        step["narration"] = {
            "zh": narration.get("zh", f"[{step['workflowPhase']}]"),
            "en": narration.get("en", f"[{step['workflowPhase']}]"),
            "source": narration.get("source", "ai"),
        }
        if step["workflowPhase"] in ("plan", "execute"):
            step["enginePlan"] = {"mysql": mysql_plan, "postgres": pg_plan}

    dp = {
        "id": f"dp_{abs(hash(sql)) % 10**8:08d}",
        "version": 4,
        "title": {
            "zh": (curriculum_node or "SQL 演示") + " 执行过程",
            "en": (curriculum_node or "SQL Demo") + " Execution",
        },
        "steps": steps,
        "workflowTrace": {
            "workflowId": ir_result.get("workflow_id", ""),
            "workflowType": "sql-execution",
            "aiSessionId": "session_001",
        },
        "engineCompare": {
            "mysql": {"query": sql, "plan": mysql_plan, "error": mysql_exp.get("error")},
            "postgres": {"query": sql, "plan": pg_plan, "error": pg_exp.get("error")},
        },
        "metadata": {
            "aiDraftVersion": "ai-v1",
            "teacherVersion": 1,
            "lastAiAction": "full-generate",
        },
        "playback": {"defaultStepDurationMs": 5000},
    }

    v_result = validate_demo_package(dp)
    dp["_validation"] = {"valid": v_result["valid"], "errors": v_result.get("errors")}
    return dp


# ═══════════════════════════════════════════════
# REST 路由
# ═══════════════════════════════════════════════

@app.get("/api/health")
async def health():
    redis_ok = "unknown"
    try:
        redis_ok = await redis_ping()
    except Exception:
        redis_ok = False
    return {"status": "ok", "tools": len(TOOL_MAP), "mode": "fastapi", "redis": redis_ok}


@app.get("/api/tools")
async def tools():
    return {"tools": TOOL_SCHEMAS}


# ── 对话管理 ──

@app.get("/api/conversations")
async def list_conversations(search: Optional[str] = None):
    result = [conversations[cid] for cid in conversation_order if cid in conversations]
    if search:
        result = [c for c in result if search.lower() in c["title"].lower()]
    return {"conversations": result}


@app.post("/api/conversations")
async def create_conversation(body: dict):
    title = body.get("title", "新对话")
    conv = _create_conv(title)
    return conversations[conv["id"]]


@app.get("/api/conversations/{conv_id}")
async def get_conversation(conv_id: str):
    conv = conversations.get(conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="对话不存在")
    return {**conv, "messages": messages.get(conv_id, [])}


@app.patch("/api/conversations/{conv_id}")
async def update_conversation(conv_id: str, body: dict):
    conv = conversations.get(conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="对话不存在")
    if "title" in body:
        conv["title"] = body["title"]
    if "status" in body:
        conv["status"] = body["status"]
    return conv


@app.delete("/api/conversations/{conv_id}")
async def delete_conversation(conv_id: str):
    if conv_id not in conversations:
        raise HTTPException(status_code=404, detail="对话不存在")
    del conversations[conv_id]
    if conv_id in messages:
        del messages[conv_id]
    if conv_id in conversation_order:
        conversation_order.remove(conv_id)
    return {"ok": True}


@app.get("/api/conversations/{conv_id}/messages")
async def get_messages(conv_id: str, limit: int = 50, offset: int = 0):
    if conv_id not in conversations:
        raise HTTPException(status_code=404, detail="对话不存在")
    msgs = messages.get(conv_id, [])
    return {
        "messages": msgs[-limit:] if limit else msgs[offset:],
        "conversation": conversations[conv_id],
        "total": len(msgs),
    }


# ── SSE 对话（向后兼容）──

@app.post("/api/ai/chat")
async def chat_sse(body: dict):
    """SSE 流式对话（保留向后兼容）"""
    message = body.get("message", "")
    sql = body.get("sql") or message
    sql_match = re.search(r'(SELECT|INSERT|UPDATE|DELETE|CREATE).*', message, re.IGNORECASE | re.DOTALL)
    if sql_match:
        sql = sql_match.group(0).strip()
    curriculum_node = body.get("curriculum_node")

    async def generate():
        try:
            yield f"data: {json.dumps({'type': 'assistant-text', 'content': '正在分析 SQL 并生成执行计划...'})}\n\n"
            await asyncio.sleep(0.1)

            dp = _build_demo_from_sql(sql, message, curriculum_node)

            for step in dp.get("steps", []):
                yield f"data: {json.dumps({'type': 'step-preview', 'step': step})}\n\n"
                await asyncio.sleep(0.05)

            yield f"data: {json.dumps({'type': 'demo-updated', 'demo': dp})}\n\n"
            yield f"data: {json.dumps({'type': 'demo-complete', 'demo_id': dp['id']})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── 演示 ──

@app.get("/api/demos/{demo_id}")
async def get_demo(demo_id: str):
    demo_path = os.path.join(_STUDIO_ROOT, "packages", "demo-schema", "examples", f"{demo_id}.json")
    if os.path.exists(demo_path):
        with open(demo_path, encoding="utf-8") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail=f"演示 {demo_id} 不存在")


# ═══════════════════════════════════════════════
# WebSocket
# ═══════════════════════════════════════════════

connected_rooms: dict[str, set] = {}  # convId -> set of WebSocket connections


async def _ws_handle_message(ws: WebSocket, data: dict, teacher_id: str, conv_id: str) -> str:
    """Handle incoming WebSocket message"""
    msg_type = data.get("type", "")

    if msg_type == "ping":
        await ws.send_text(json.dumps({"type": "pong"}))
        return conv_id

    elif msg_type == "chat:message":
        content = data.get("content", {})
        text = content.get("text", "")
        sql = content.get("sql", "")

        # Store user message
        user_msg = {
            "id": f"msg_{uuid.uuid4().hex[:10]}",
            "convId": conv_id,
            "role": "user",
            "type": "text",
            "content": {"text": text, "sql": sql or None},
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        msgs = messages.setdefault(conv_id, [])
        msgs.append(user_msg)
        if conv_id in conversations:
            conversations[conv_id]["messageCount"] = len(msgs)

        try:
            await cache_message(conv_id, user_msg)
        except Exception:
            pass

        # Send thinking indicator
        await ws.send_text(json.dumps({
            "type": "agent:thinking", "convId": conv_id,
            "content": "正在分析..."
        }))

        await asyncio.sleep(0.1)
        await ws.send_text(json.dumps({
            "type": "agent:thinking", "convId": conv_id,
            "content": "调用工具链..."
        }))
        await asyncio.sleep(0.05)

        try:
            # Determine what to process
            actual_sql = sql or ""
            if not actual_sql:
                sql_match = re.search(r'(SELECT|INSERT|UPDATE|DELETE|CREATE).*', text, re.IGNORECASE | re.DOTALL)
                if sql_match:
                    actual_sql = sql_match.group(0).strip()

            if actual_sql:
                # Run demo generation — LLM calls are blocking (15s+)
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    dp = await asyncio.get_event_loop().run_in_executor(
                        pool, _build_demo_from_sql, actual_sql, text, data.get("curriculum_node")
                    )

                # Stream step previews
                for i, step in enumerate(dp.get("steps", [])):
                    await ws.send_text(json.dumps({
                        "type": "step:preview", "convId": conv_id,
                        "step": step, "order": i + 1,
                    }))
                    await asyncio.sleep(0.03)

                # Build reply text
                steps = dp.get("steps", [])
                reply_text = f"已生成 {len(steps)} 步演示：\n\n"
                for i, s in enumerate(steps):
                    label = s.get("workflowPhase", "")
                    zh = s.get("narration", {}).get("zh", "")
                    reply_text += f"【{i+1}. {label}】{zh[:60]}...\n"

                await ws.send_text(json.dumps({
                    "type": "demo:complete", "convId": conv_id,
                    "demo": dp, "demo_id": dp["id"],
                }))

            else:
                # Non-SQL: concept mode
                reply_text = f"关于「{text}」的知识点讲解：\n\n这是数据库课程中的重要概念。建议使用 Mermaid 可视化或 SQL 示例来辅助理解。你可以粘贴相关 SQL 来生成执行演示。"
                dp = None

            # Push assistant text reply (so it appears in chat)
            await ws.send_text(json.dumps({
                "type": "assistant-text", "convId": conv_id,
                "content": reply_text,
            }))

            # Store and send assistant message
            assistant_msg = {
                "id": f"msg_{uuid.uuid4().hex[:10]}",
                "convId": conv_id,
                "role": "assistant",
                "type": "demo_snapshot" if dp else "text",
                "content": {
                    "text": reply_text,
                    "demoSnapshotId": dp["id"] if dp else None,
                },
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            msgs.append(assistant_msg)

            await ws.send_text(json.dumps({
                "type": "conv:new_message", "convId": conv_id,
                "message": assistant_msg,
            }))

            try:
                await cache_message(conv_id, assistant_msg)
            except Exception:
                pass

        except Exception as e:
            import traceback
            traceback.print_exc()
            await ws.send_text(json.dumps({
                "type": "error", "convId": conv_id,
                "message": str(e),
            }))
        return conv_id

    elif msg_type == "conv:switch":
        new_conv_id = data.get("convId", "")
        if new_conv_id in conversations:
            # Move connection to the target room and update active conv for this socket
            room = connected_rooms.setdefault(conv_id, set())
            room.discard(ws)
            connected_rooms.setdefault(new_conv_id, set()).add(ws)

            await ws.send_text(json.dumps({
                "type": "conv:loaded",
                "convId": new_conv_id,
                "messages": messages.get(new_conv_id, []),
                "currentDemo": None,
            }))
            return new_conv_id
        return conv_id

    elif msg_type == "conv:delete":
        cid = data.get("convId", "")
        if cid in conversations:
            del conversations[cid]
            if cid in messages:
                del messages[cid]
            if cid in conversation_order:
                conversation_order.remove(cid)
            # Notify room
            room = connected_rooms.setdefault(conv_id, set())
            for client in room:
                try:
                    await client.send_text(json.dumps({
                        "type": "conv:deleted", "convId": cid,
                    }))
                except Exception:
                    pass
        return conv_id

    elif msg_type == "conv:clear_messages":
        cid = data.get("convId", "")
        if cid in messages:
            messages[cid] = []
        if cid in conversations:
            conversations[cid]["messageCount"] = 0
        await ws.send_text(json.dumps({
            "type": "conv:cleared", "convId": cid,
        }))
        return conv_id

    elif msg_type == "message:delete":
        cid = data.get("convId", "")
        msg_id = data.get("msgId", "")
        if cid in messages:
            messages[cid] = [m for m in messages[cid] if m.get("id") != msg_id]
            if cid in conversations:
                conversations[cid]["messageCount"] = len(messages[cid])
        await ws.send_text(json.dumps({
            "type": "message:deleted", "convId": cid, "msgId": msg_id,
        }))
        return conv_id

    elif msg_type == "player:seek":
        # Broadcast to room
        room = connected_rooms.setdefault(conv_id, set())
        for client in room:
            try:
                await client.send_text(json.dumps({
                    "type": "player:sync",
                    "convId": conv_id,
                    "stepIndex": data.get("stepIndex", 0),
                }))
            except Exception:
                pass

    return conv_id


@app.websocket("/ws/chat")
async def ws_chat(ws: WebSocket, teacher_id: str = "local", conv_id: str = ""):
    await ws.accept()

    # Ensure conversation exists
    if conv_id not in conversations:
        conv = _create_conv("新对话")
        conv_id = conv["id"]

    # Register in room
    room = connected_rooms.setdefault(conv_id, set())
    room.add(ws)

    try:
        # Send initial state
        await ws.send_text(json.dumps({
            "type": "conv:loaded",
            "convId": conv_id,
            "messages": messages.get(conv_id, []),
            "currentDemo": None,
        }))

        # Send conversation list
        conv_list = [conversations[cid] for cid in conversation_order if cid in conversations]
        await ws.send_text(json.dumps({
            "type": "conv:list",
            "conversations": conv_list,
        }))

        # Message loop
        while True:
            raw = await ws.receive_text()
            if raw == "ping" or raw.startswith("{"):
                try:
                    data = json.loads(raw)
                    if data.get("type") == "ping":
                        await ws.send_text(json.dumps({"type": "pong"}))
                    else:
                        conv_id = await _ws_handle_message(ws, data, teacher_id, conv_id)
                except json.JSONDecodeError:
                    pass
            else:
                pass  # Ignore non-JSON

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"[WS] error: {e}")
    finally:
        room.discard(ws)


if __name__ == "__main__":
    import uvicorn
    print("Starting DB Demo Studio API (FastAPI)...")
    print(f"  Health: http://localhost:8000/api/health")
    print(f"  Chat SSE: POST http://localhost:8000/api/ai/chat")
    print(f"  WebSocket: ws://localhost:8000/ws/chat")
    uvicorn.run(app, host="0.0.0.0", port=8000)
