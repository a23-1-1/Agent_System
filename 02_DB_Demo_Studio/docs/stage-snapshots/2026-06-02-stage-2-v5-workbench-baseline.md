# Stage 2 Snapshot — v5 对话工作台基线

> 日期：2026-06-02  
> 阶段：Stage 2 完成，进入 Stage 3  
> 来源：`docs/requirements-spec.md` v5

---

## 阶段目标

完成 AI 协作式数据库演示工作台的基础全栈闭环：多对话、WebSocket、AI 工具链、演示步骤预览和 Player 播放。

---

## 完成内容

- FastAPI 后端：REST + WebSocket + SSE 兼容入口。
- WebSocket 协议：`chat:message`、`conv:switch`、`player:seek`、`step:preview`、`demo:complete`。
- Redis 客户端：消息缓存、会话缓存、Pub/Sub 基础能力。
- React 教师工作台：ConversationPanel、ChatPanel、FlowEditor、ExecutionPlayer。
- Zustand 状态：conversationStore、demoStore、playbackStore、teacherStore。
- 工具链：`sql_analyze`、`explain_mysql`、`explain_postgres`、`assemble_execution_steps`、`generate_narration`。
- Docker Compose：MySQL、PostgreSQL、Redis、API、Web。

---

## 关键文件

| 文件 | 作用 |
|---|---|
| `apps/api/main.py` | REST + WS + DemoPackage 生成 |
| `apps/api/redis_client.py` | Redis 缓存与 Pub/Sub |
| `apps/web/src/pages/TeacherWorkbenchPage.tsx` | 教师三栏工作台 |
| `apps/web/src/lib/ws-client.ts` | WS 连接、心跳、重连 |
| `apps/web/src/stores/conversationStore.ts` | 多对话状态 |
| `apps/web/src/stores/demoStore.ts` | 当前演示与快照 |
| `packages/ai-tools/tools.py` | AI 工具与 DeepSeek 兼容调用 |
| `packages/execution-workflow/workflow.py` | SQL 6 阶段 DAG |

---

## 运行与验证

已知可执行验证：

```bash
python -m py_compile apps/api/main.py apps/api/redis_client.py
cd apps/web && npx tsc --noEmit
cd apps/web && npm run build
```

阶段验收：

- 多对话 UI 可创建/切换。
- WebSocket 使用 `teacher_id` / `conv_id`。
- SQL 输入可生成 DemoPackage。
- 非 SQL 输入不会触发 `demo=null` 崩溃。
- 前端构建通过。

---

## 已知问题

- 后端 conversations/messages 仍是内存 dict，Redis 只做缓存，未接 PostgreSQL 持久化。
- API 文档有 `/api/v5/*` 愿景，代码当前仍是 `/api/*`。
- P2 模拟器尚未落地，当前主要是解释型步骤 + Mermaid/Quiz 雏形。
- 教师编辑闭环、版本快照、导出链路尚未完成。

---

## 下一阶段入口

Stage 3：SQL 过程模拟器。

核心目标：让 JOIN SQL 能产生 FROM/JOIN/ON/SELECT 的中间结果表，并在 Player 中随步骤播放。

---

## 下一阶段提示词

见 `docs/prompts/next-stage-prompt.md`。
