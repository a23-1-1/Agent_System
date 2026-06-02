# DB Demo Studio — 项目开发快照

> 生成时间：2026-06-02 (v5 重构后)
> 用途：跨 session 冷启动，让 AI 快速了解当前代码状态

---

## 1. 文件结构

```
02_DB_Demo_Studio/
├── CLAUDE.md                    ← 项目卡片（每次 AI session 先读）
├── .env                         ← API key 配置文件（gitignored）
├── .dockerignore
├── docker-compose.yml           ← 全栈编排：MySQL + PG + Redis + API + Web
│
├── apps/api/                    ← FastAPI 后端
│   ├── main.py                  ← 路由 + WebSocket + SSE + Conversation CRUD
│   ├── requirements.txt
│   └── Dockerfile
│
├── apps/web/                    ← React 19 + Vite 8 + TailwindCSS v4
│   ├── Dockerfile               ← 两阶段构建 (Node → Nginx)
│   ├── nginx.conf               ← SPA + /api + /ws 反向代理
│   ├── vite.config.ts           ← Vite 配置 (WebSocket proxy)
│   ├── tsconfig.app.json        ← strict mode (noUnusedLocals, noUnusedParameters)
│   └── src/
│       ├── main.tsx             ← 路由：/ /classroom /student/:demoId
│       ├── lib/
│       │   ├── types.ts         ← v5 完整类型 (Conversation/Message/DemoPackage/WS协议)
│       │   └── ws-client.ts     ← WebSocket 客户端 (连接/心跳/重连/事件路由)
│       ├── hooks/
│       │   └── useWebSocket.ts  ← React WS hook，事件分发到 Store
│       ├── stores/
│       │   ├── conversationStore.ts  ← 对话列表 + 消息 + 流式推送
│       │   ├── demoStore.ts          ← 当前演示 + 版本快照
│       │   ├── playbackStore.ts      ← 播放状态 + 自适应决策
│       │   └── teacherStore.ts       ← 教师风格 Profile
│       ├── pages/
│       │   ├── TeacherWorkbenchPage.tsx  ← 三栏：对话列表 | Chat+Flow | Player
│       │   ├── ClassroomPage.tsx         ← 课堂全屏播放
│       │   └── StudentPage.tsx          ← 学生端 + 测验 + 掌握度
│       └── features/
│           ├── conversation/    ← 对话列表面板 (Panel/Card/Search)
│           ├── chat/            ← ChatPanel + AgentThinkingChain + QuickActions
│           ├── flow-editor/     ← 步骤卡片链
│           └── execution-player/ ← 分步播放 + EXPLAIN 面板
│
├── packages/
│   ├── ai-tools/tools.py             ← 8 个工具 + Tool Schema + 规则讲解词
│   ├── db-engine/connector.py        ← MySQL/PG 连接器 + EXPLAIN
│   ├── execution-workflow/workflow.py ← 6 阶段 DAG 编排引擎
│   └── demo-schema/
│       ├── schema.json               ← DemoPackage JSON-Schema
│       ├── validate.py               ← Schema 校验器
│       └── examples/                 ← 内嵌示例数据
│
├── docs/
│   ├── requirements-spec.md    ← 需求规格 v5 (AI 协作对话版)
│   ├── frontend-design.md      ← 前端架构设计 v5
│   ├── architecture.md         ← 架构设计 (v2，存档用)
│   └── project-snapshot.md     ← 本文档
```

---

## 2. 运行状态

| 服务 | 地址 | 状态 |
|---|---|---|
| Nginx 前端 | http://localhost:8080 | ✅ 运行中 (Docker) |
| FastAPI 后端 | http://localhost:8000 | ✅ 运行中 (Docker) |
| Redis | `db_demo_redis` :6379 | ✅ 容器运行 |
| MySQL 8.0 | `db_demo_mysql` :3306(内)/3308(外) | ✅ 容器运行 |
| PostgreSQL 16 | `db_demo_pg` :5432(内)/5433(外) | ✅ 容器运行 |

**启动命令：**
```bash
# 全栈 Docker 启动
docker compose up -d --build

# 或本地开发（前后端分离）
cd apps/api && uvicorn main:app --port 8000
cd apps/web && npm run dev
```

---

## 3. 架构变更 (v4 → v5)

| 维度 | v4 (之前) | v5 (当前) |
|---|---|---|
| 后端框架 | Flask + SSE | **FastAPI + WebSocket + SSE 兼容** |
| 前端状态 | 无状态管理 | **Zustand 4 Store** |
| 对话模型 | 单次问答，无历史 | **多对话管理** + 消息持久化 |
| 通信协议 | SSE (单向) | **WebSocket (双向) + SSE 保留** |
| 部署方式 | 手动启动 | **Docker Compose 全栈编排** |

---

## 4. API 端点

```
REST:
  GET    /api/health                     → 健康检查
  GET    /api/tools                      → 工具列表
  GET    /api/conversations              → 对话列表
  POST   /api/conversations              → 创建对话
  GET    /api/conversations/{id}         → 对话详情
  PATCH  /api/conversations/{id}         → 更新对话
  DELETE /api/conversations/{id}         → 删除对话
  GET    /api/conversations/{id}/messages → 消息历史
  POST   /api/ai/chat                    → SSE 流式 (向后兼容)
  GET    /api/demos/{id}                 → 获取演示

WebSocket:
  WS     /ws/chat?teacher_id=&conv_id=   → 双向对话协议
    客户端→服务端: chat:message, conv:switch, player:seek, ...
    服务端→客户端: agent:thinking, step:preview, demo:complete, ...
```

---

## 5. 核心数据流

```
用户在 ChatPanel 输入 SQL/知识点
  │
  WebSocket chat:message → FastAPI ws_handler
  │
  ├─ agent:thinking  ← "正在分析 SQL..."
  ├─ agent:thinking  ← "调用 sql_analyze → explain_mysql → explain_postgres"
  │
  ├─ step:preview ×6  ← 流式推送每步 (lex→parse→optimize→plan→execute→result)
  │     demoStore.step:preview → Player 实时更新
  │
  └─ demo:complete   ← 完整 DemoPackage
        demoStore.demo:complete → Player 刷新 + ChatPanel 显示完成

用户切换对话:
  ConversationPanel.onClick → conv:switch
    → 后端返回 conv:loaded (消息历史)
    → conversationStore + demoStore 刷新
```

---

## 6. Player 阶段面板 (保留 v4 实现)

| 阶段 | 面板内容 |
|---|---|
| lex | SQL 关键字标签 (蓝色) + 数量统计 |
| parse | 表名标签 (紫色) + 子句检测 (绿色✓/灰色—) |
| optimize | 扫描方式中文名 (黄色) + 关联说明 |
| plan | MySQL vs PG 代价卡片 + EXPLAIN JSON 树 |
| execute | 估计扫描行数 (黄色) + EXPLAIN JSON |
| result | 仅讲解词 |

---

## 7. 下一步开发 (P1/P2 优先级)

| 优先级 | 功能 | 说明 | 涉及文件 |
|---|---|---|---|
| **P1** | Mermaid 可视化渲染 | Agent 生成 Mermaid 流程图，步骤高亮联动 | 新增 `features/animation/MermaidRenderer.tsx` |
| **P1** | 嵌入式测验 Quiz | 每步可出选择题，答题后 AI 解释 | 新增 `features/quiz/QuizPanel.tsx` |
| **P1** | Redis 集成 | 对话缓存 + 消息缓存 + LLM cache | `apps/api/main.py`, `redis_client.py` |
| **P1** | 对话历史搜索 | 按知识点/日期搜索历史对话 | `features/conversation/ConversationSearch.tsx` |
| **P2** | SQL 分步执行模拟器 | FROM→WHERE→SELECT 分步展示中间结果 | 新增 `features/animation/SqlSimulator.tsx` |
| **P2** | B+树索引动画 | D3.js 实现 B+树插入/查找动画 | 新增 `features/animation/BPlusTreeCanvas.tsx` |
| **P2** | 事务隔离演示器 | 4 种隔离级别对比脏读/不可重复读/幻读 | 新增 `features/animation/TransactionDemo.tsx` |
| **P2** | 课堂广播 | Redis Pub/Sub 教师→学生端同步 | `ws_handler.py`, `features/student/` |
| **P2** | 掌握度自适应 | 基于答题+停留时长，AI 建议跳过/展开 | `playbackStore.ts`, `StudentPage.tsx` |

---

## 8. 关键数据模型

```typescript
interface DemoPackage {
  id: string; convId?: string; version?: number;
  title: { zh: string; en: string }
  demoType?: 'mermaid' | 'sql-simulator' | 'bplus-tree' | 'transaction'
  steps: DemoStep[]
  simulationData?: { mermaidCode?, sqlSimulator?, indexAnimation?, transactionDemo? }
  metadata: { teacherId?, model?, difficulty?, teacherVersion }
  playback: { defaultStepDurationMs }
}

interface DemoStep {
  id: string; order: number; workflowPhase: string
  narration: { zh: string; en: string; source: 'ai'|'teacher'|'rule'; ttsUrl?: string }
  visuals?: { type: VisualType; config?: Record<string, unknown> }
  quiz?: { question: string; options: string[]; answer: number; explanation: string }
  engineEvidence?: Record<string, unknown>
  enginePlan?: { mysql?, postgres? }
  groundingRef?: string | null
}
```

---

## 9. 常见陷阱

| 问题 | 原因 | 修复 |
|---|---|---|
| Docker 端口冲突 | Vite 或旧容器占用 5173/8000 | `docker compose down` + 杀进程 |
| TypeScript 构建失败 | `noUnusedLocals` 严格模式 | 加 `_` 前缀或用 `unknown as` |
| WebSocket 连不上 | Vite proxy 未配置 `/ws` | `vite.config.ts` 加 `ws: true` |
| EXPLAIN 数据为 None | `normalize_plan()` 格式判断 | 已通过 `query_block` 检测修复 |
| MySQL 容器健康检查失败 | `demo` 用户权限 | docker-compose 设 `MYSQL_USER=demo` |
