# DB Demo Studio

AI 原生的数据库教学演示平台。教师在对话中输入 SQL 或知识点，AI 生成分步执行演示，可交互播放。

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI + Uvicorn + WebSocket + Redis |
| Frontend | React 19 + TypeScript + Vite 8 + TailwindCSS v4 + Zustand |
| Packages | `ai-tools` `db-engine` `execution-workflow` `demo-schema` |
| AI | DeepSeek API (via `ai-tools/tools.py`) |
| Deploy | Docker Compose (api + web + mysql + postgres + redis) |

## Architecture (one paragraph)

教师工作台三栏：ConversationPanel | ChatPanel + FlowEditor | ExecutionPlayer。用户通过 WebSocket `chat:message` 发送 SQL/概念 → 后端工具链 (`sql_analyze` → `explain_mysql/postgres` → `assemble_execution_steps` → `generate_narration`) → 流式 `step:preview` + `demo:complete`。Vite dev 代理 `/api` 与 `/ws` → FastAPI `:8000`。

## Run

```bash
# 全栈 Docker
cd 02_DB_Demo_Studio && docker compose up -d --build
# 前端 http://localhost:8080  后端 http://localhost:8000

# 本地开发
cd apps/api && uvicorn apps.api.main:app --reload --port 8000
cd apps/web && npm run dev   # :5173
```

## Conventions

- 文件名: `kebab-case`
- 组件: `PascalCase` 文件 + 命名导出（features）
- WS query: `teacher_id`, `conv_id`（与 FastAPI 一致）
- REST: `/api/<resource>`
- 一次 session 做一个垂直切片

## Current Sprint

稳定主链路：对话创建/切换 → WebSocket 生成 DemoPackage → Player 播放 → 错误与空状态。

## Key Files

| File | Purpose |
|---|---|
| `apps/api/main.py` | FastAPI REST + WebSocket + demo pipeline |
| `apps/api/redis_client.py` | Redis 消息缓存 |
| `apps/web/src/pages/TeacherWorkbenchPage.tsx` | 三栏教师工作台 |
| `apps/web/src/lib/ws-client.ts` | WebSocket 客户端 |
| `apps/web/src/stores/*.ts` | Zustand 状态 |
| `packages/ai-tools/tools.py` | AI 工具链 |
| `docs/project-snapshot.md` | 跨 session 冷启动快照 |
