# Day 2 架构 Prompt 实战 — packages/ai-orchestrator

> 日期：2026-06-01  
> Day：Day 2 架构设计实战  
> Prompt：`01_AI_Dev_Workflow_Kit/prompts/architecture.md`  
> 目标模块：`02_DB_Demo_Studio/packages/ai-orchestrator/`  
> 上下文：`02_DB_Demo_Studio/docs/architecture.md` + `02_DB_Demo_Studio/docs/ai-workflow.md` + `00_Notes/requirements/db_demo_video_requirements.md`

---

## 需求摘要

在 DB Demo Studio 中，`packages/ai-orchestrator/` 负责 **Agent 编排、多轮对话、工具调度**。它不是直接生成最终 UI 或视频的模块，而是连接 `ai-studio`、`ai-tools`、`execution-workflow`、`llm-pipeline` 与 `demo-schema` 的中枢：

- 接收教师在 AI Studio 中的自然语言请求、SQL、课纲上下文和单步修改指令
- 维护会话状态与 DemoPackage 草稿
- 决定何时调用 `curriculum_search`、`sql_analyze`、`explain_mysql`、`explain_postgres`、`assemble_execution_steps`、`validate_demo_package` 等工具
- 通过 SSE 事件把阶段进度、工具调用、步骤初稿和错误返回给前端
- 保证 SQL/执行计划类步骤必须有 grounding，避免纯 LLM 幻觉

---

## 现有系统上下文

### 技术栈

- TypeScript monorepo
- React 18 + Vite：`apps/web/src/features/ai-studio/`
- Fastify API：对外暴露 `/ai/sessions/:id/chat` 等接口
- DeepSeek API：本仓库统一 LLM Provider
- SSE：流式返回对话与生成进度
- Zod / TypeScript 类型：结构化输出与 DemoPackage 校验

### 相关模块

| 模块 | 与 ai-orchestrator 的关系 |
|---|---|
| `apps/web/src/features/ai-studio/` | 发起对话、展示 SSE、预览 DemoPackage |
| `packages/ai-tools/` | 提供 LLM 可调用工具 |
| `packages/execution-workflow/` | 产出执行阶段 DAG 与步骤 IR |
| `packages/llm-pipeline/` | Prompt、结构化输出、降级策略 |
| `packages/demo-schema/` | DemoPackage / DemoStep 单一真相源 |
| `packages/db-engine/` | MySQL / PostgreSQL EXPLAIN 沙箱 |
| `packages/prompt-registry/` | Agent system prompt 与任务 prompt 版本 |

### 约束

- 首 token ≤ 3s，完整初稿 ≤ 60s
- SQL 类 `plan` / `execute` 步骤必须引用 EXPLAIN 或 workflow grounding
- 教师可只重写当前步，不整包重来
- 网页 Player 与 MP4 共享同一个 DemoPackage
- 本仓库 LLM 调用统一使用 DeepSeek API
- 敏感 SQL 默认不写入前端日志；LLM 调用需可审计

---

## 1. 方案 A（推荐）— 单 Agent 会话编排 + 工具路由 + 工作流守卫

### 模块划分

```text
packages/ai-orchestrator/
├── src/
│   ├── index.ts
│   ├── orchestrator.ts        # AiOrchestrator facade，对外主入口
│   ├── session-store.ts       # AiSession / DemoPackage 草稿状态
│   ├── agent-runner.ts        # ReAct / tool-use 简化循环
│   ├── tool-router.ts         # 调用 ai-tools，并做权限与参数校验
│   ├── stream-events.ts       # SSE 事件类型与 emit helper
│   ├── step-regenerator.ts    # 单步 regenerate-step
│   ├── policies.ts            # 超时、最大 tool calls、grounding 规则
│   ├── errors.ts              # 结构化错误
│   └── types.ts
└── package.json
```

| 子模块 | 职责 |
|---|---|
| `orchestrator.ts` | 对外提供 `createSession`、`chat`、`regenerateStep` |
| `session-store.ts` | 保存会话消息、当前 DemoPackage 草稿、工具调用 trace |
| `agent-runner.ts` | 根据教师请求规划工具调用顺序，聚合结果 |
| `tool-router.ts` | 调 `ai-tools`，统一超时、schema 校验、审计记录 |
| `stream-events.ts` | 生成 `assistant-text`、`tool-start`、`step-draft` 等 SSE 事件 |
| `step-regenerator.ts` | 单步重写，只修改目标 step |
| `policies.ts` | 防循环、防幻觉、防超时策略 |

### 核心接口定义

```typescript
export interface AiOrchestrator {
  createSession(input: CreateAiSessionInput): Promise<AiSession>;
  chat(input: ChatInput): AsyncIterable<AiStreamEvent>;
  regenerateStep(input: RegenerateStepInput): AsyncIterable<AiStreamEvent>;
  getSession(sessionId: string): Promise<AiSession | null>;
}

export interface CreateAiSessionInput {
  teacherId: string;
  curriculumNodeId?: string;
  initialDemoId?: string;
  locale?: 'zh' | 'en' | 'bilingual';
}

export interface ChatInput {
  sessionId: string;
  message: string;
  sql?: string;
  engineTargets?: Array<'mysql' | 'postgres'>;
}

export interface RegenerateStepInput {
  sessionId: string;
  demoId: string;
  stepId: string;
  instruction: string;
}

export type AiStreamEvent =
  | { type: 'assistant-text'; content: string }
  | { type: 'tool-start'; toolName: AiToolName; callId: string }
  | { type: 'tool-result'; toolName: AiToolName; callId: string; summary: string }
  | { type: 'workflow-phase'; phase: string; status: 'running' | 'done' | 'failed' }
  | { type: 'step-draft'; step: DemoStep }
  | { type: 'step-updated'; step: DemoStep }
  | { type: 'demo-updated'; demo: DemoPackage }
  | { type: 'error'; code: string; message: string; recoverable: boolean };
```

```typescript
export interface AiSession {
  id: string;
  teacherId: string;
  demoDraft?: DemoPackage;
  messages: AiMessage[];
  toolTrace: ToolTraceEntry[];
  createdAt: string;
  updatedAt: string;
}

export interface ToolTraceEntry {
  callId: string;
  toolName: AiToolName;
  startedAt: string;
  finishedAt?: string;
  status: 'running' | 'ok' | 'error';
  // 不存完整敏感 SQL，只存 hash / 摘要 / explain snapshot id
  auditSummary: string;
}
```

### 数据流

```text
AI Studio
  → POST /ai/sessions/:id/chat
  → AiOrchestrator.chat()
  → AgentRunner 识别意图
  → ToolRouter 调用 ai-tools
      → curriculum_search
      → sql_analyze
      → explain_mysql / explain_postgres
      → assemble_execution_steps
  → llm-pipeline 生成 narration / visual_spec / bilingual
  → validate_demo_package
  → session-store 保存 DemoPackage 草稿
  → SSE 返回 step-draft / demo-updated
  → execution-player 实时预览
```

单步重写：

```text
AI Studio 选中 step
  → regenerateStep(sessionId, demoId, stepId, instruction)
  → 读取目标 step + 前后 step + groundingRef
  → llm-pipeline 只生成该 step 的 narration / visuals
  → validate_demo_package 局部校验
  → 替换 step，版本 +1
  → SSE step-updated / demo-updated
```

### 优点 / 缺点

| 优点 | 缺点 |
|---|---|
| 与现有 `ai-workflow.md` 完全一致，能承载 AI Studio 对话主路径 | 比普通 service 复杂，需要先定义事件和状态 |
| `ToolRouter` 把工具调用统一收口，方便后续加 MCP / 权限 / 审计 | Phase 1 需要控制范围，只做最小工具链 |
| `SessionStore` 支持多轮对话和单步重写 | 需要明确 DemoPackage 版本策略 |
| `policies.ts` 可集中处理防循环、超时、grounding | 需要测试覆盖，否则 Agent 难调试 |
| SSE 事件标准化，前端体验更稳定 | 事件类型过多会增加前端处理成本 |

---

## 2. 方案 B（备选）— API Route 直接编排工具，无独立 Agent 包

### 模块划分

```text
apps/api/src/routes/ai/
├── chat.ts                 # 直接串联 LLM + tools
├── regenerate-step.ts
└── stream.ts

packages/ai-tools/
packages/execution-workflow/
packages/llm-pipeline/
```

### 核心接口定义

```typescript
POST /ai/chat
POST /ai/regenerate-step
```

API route 内直接完成：

```text
解析请求 → 调 sql_analyze → 调 explain → 调 LLM → 返回 SSE
```

### 数据流

```text
AI Studio → apps/api route → ai-tools / llm-pipeline → DemoPackage → SSE
```

### 优点 / 缺点

| 优点 | 缺点 |
|---|---|
| 实现最快，适合 1-2 天 PoC | 编排逻辑散落在 route 中，后续难维护 |
| 少一个包，调试简单 | 多轮会话、单步重写、工具 trace 容易变乱 |
| 对 Phase 1 最小 Demo 友好 | 不利于后续 MCP、Memory、Skill 接入 |
| 初期类型少 | 很快会形成“大函数” |

---

## 3. 方案对比表

| 维度 | 方案 A：独立 ai-orchestrator | 方案 B：Route 直接编排 |
|---|---|---|
| 复杂度 | 中 | 低 |
| 可扩展性 | 高：可接 MCP、Memory、更多 tools | 低：route 会膨胀 |
| 维护成本 | 中：模块清晰但需测试 | 前期低，后期高 |
| 风险 | Agent 状态复杂 | 技术债快速积累 |
| 与现有架构兼容 | 高：已在 `architecture.md` 中定位为核心模块 | 中：会绕开既定模块边界 |
| 多轮对话 | 强 | 弱 |
| 单步 regenerate | 清晰 | 容易耦合 |
| 审计 / Trace | 易做 | 分散 |

---

## 4. 推荐方案及理由

推荐 **方案 A：单 Agent 会话编排 + 工具路由 + 工作流守卫**。

理由：

1. 需求明确要求 AI Studio 对话、多轮修改、工具调度和单步重写，独立 `ai-orchestrator` 更符合模块边界。
2. DB Demo Studio 的核心风险是 LLM 幻觉，必须通过 `ToolRouter + policies + validate_demo_package` 收口。
3. 后续 Phase 会学习 MCP、Agent、Memory、Skill，`ai-orchestrator` 正好是可演进的作品集核心模块。
4. 方案 B 只适合快速验证 SSE 或 EXPLAIN，不适合作为长期教学产品架构。

**YAGNI 标注：**

- Phase 1 不做多 Agent（Planner / Executor / Critic 拆包暂缓）
- Phase 1 不做长期 Memory，只保留会话内上下文
- Phase 1 不做复杂权限系统，只做 teacherId + session ownership
- Phase 1 不做向量 RAG，课纲可先用静态 JSON / markdown 检索

---

## 5. 实施步骤

### 阶段 1 — 类型与事件协议（可独立交付）

- 新建 `packages/ai-orchestrator/src/types.ts`
- 定义 `AiOrchestrator`、`AiSession`、`AiStreamEvent`
- 在 `apps/api` 先 mock SSE 返回

**验收：** 前端能看到 `assistant-text`、`workflow-phase`、`step-draft` 三类事件。

### 阶段 2 — SessionStore + 最小 chat()

- 实现内存版 `session-store.ts`
- `chat()` 先不调真实 LLM，用 mock DemoStep 流式返回

**验收：** 同一 session 能累积 messages 与 demoDraft。

### 阶段 3 — ToolRouter 接入 ai-tools

- 接入 `sql_analyze`
- 接入 `explain_mysql` / `explain_postgres`
- 接入 `assemble_execution_steps`

**验收：** SQL 输入能生成带 `workflowPhase` 和 `groundingRef` 的步骤草稿。

### 阶段 4 — DeepSeek + llm-pipeline

- 用 DeepSeek 生成 narration / visual spec
- 所有 LLM 输出必须过 Zod schema
- 失败时降级为模板文案

**验收：** 60s 内生成 ≥3 步 DemoPackage 初稿。

### 阶段 5 — regenerate-step

- 实现 `regenerateStep()`
- 只传目标 step、前后文、groundingRef
- 更新单步并保留其它 steps 不变

**验收：** “讲简单点”只改变目标 step 的 narration / visual spec。

### 阶段 6 — Trace / 审计 / 防循环

- `toolTrace` 记录工具调用摘要
- 最大 10 次 tool call
- 60s 超时
- 无 grounding 的 `plan` / `execute` 步拒绝发布

**验收：** 错误路径可解释，前端收到 recoverable error。

---

## 6. 风险与缓解措施

| 风险 | 缓解措施 |
|---|---|
| Agent 循环调用工具 | `MAX_TOOL_CALLS = 10`，每轮必须推进状态 |
| LLM 编造执行步骤 | `validate_demo_package` 强制校验 `groundingRef` |
| 首屏慢 | 先发 `assistant-text` / `workflow-phase`，长任务后台继续 |
| DeepSeek 返回非结构化内容 | `llm-pipeline` 做 schema parse + repair + fallback |
| 敏感 SQL 泄露 | trace 只存 hash/摘要；前端 tool-result 不展示完整 SQL |
| 单步重写破坏上下文 | 只替换目标 step，保留 workflowTrace 与 step order |
| 工具层异常 | `tool-router` 将错误转成 recoverable SSE error，允许教师重试 |

---

## 7. 人工校验点

- `AiStreamEvent` 是否足够前端驱动预览，但不过度细碎
- `ToolRouter` 是否只做路由，不吞掉业务逻辑
- `SessionStore` 后续是否能从内存平滑迁移到 DB
- `regenerateStep` 是否真的只改一步
- `plan` / `execute` 步是否都有 grounding

---

## 8. 使用记录

| 日期 | Prompt | 任务 | 产出 |
|---|---|---|---|
| 2026-06-01 | `architecture.md` | 设计 `packages/ai-orchestrator/` 架构 | 本文档 |

---

## 9. 迭代笔记

- 这次架构设计没有重复总架构，而是聚焦 `ai-orchestrator` 的内部模块边界。
- 下一步不要马上做完整 Agent，先实现 **类型 + SSE mock + SessionStore**，让前端 AI Studio 能接到真实事件。
- 方案 A 是长期主线；方案 B 只作为临时 Spike，不进入正式架构。
