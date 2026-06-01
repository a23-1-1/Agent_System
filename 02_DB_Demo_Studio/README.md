# DB Demo Studio — AI 原生数据库演示平台

> **完整学习项目**：需求澄清 → **AI 优先架构** → PoC → 分阶段实现。  
> 核心：**AI 交互式生成演示** + **执行演示工作流** → 同源导出交互网页与双语 MP4。

| 字段 | 值 |
|---|---|
| **项目代号** | `db_demo_video` / DB Demo Studio |
| **状态** | Phase 0 — AI 架构 v2 就绪，待 PoC |
| **代码根目录** | 本目录 `02_DB_Demo_Studio/` |

---

## 项目目标

为大学数据库课教师提供 **AI 对话式演示生产工具**：用自然语言描述知识点或粘贴 SQL，**AI Agent** 结合 MySQL/PostgreSQL **EXPLAIN 真值**与课纲上下文，**流式生成**分步执行演示；教师可对话修改任一步；定稿后**同源发布**交互网页与带双语字幕 MP4。

### 两大核心能力

| 能力 | 说明 |
|---|---|
| **AI 交互式生成** | AI Studio 对话界面 — 流式预览、单步重写、Slash 快捷指令 |
| **执行演示工作流** | SQL/概念 → 标准阶段 DAG（解析→计划→执行→结果）— EXPLAIN grounding，防幻觉 |

**双交付物（同源）：** 交互网页 + MP4（含字幕，至少中英双语）

**三场景：** 教师备课（AI Studio）· 课堂分步演示（Execution Player）· 学生课后自学

---

## 文档索引

| 文档 | 路径 | 说明 |
|---|---|---|
| **需求澄清** | [`00_Notes/requirements/db_demo_video_requirements.md`](../00_Notes/requirements/db_demo_video_requirements.md) | Q1–Q10；含 AI 交互与执行工作流功能 |
| **架构设计 v2（AI 优先）** | [`docs/architecture.md`](./docs/architecture.md) | Agent + 执行工作流 + 方案 A/B |
| **AI 工作流详设** | [`docs/ai-workflow.md`](./docs/ai-workflow.md) | AI Studio、Agent、Tools、SSE 协议 |
| **课纲—模板映射** | [`docs/curriculum-mapping.md`](./docs/curriculum-mapping.md) | 8 大类与 workflowType 映射 |

---

## 与 Agent_System 仓库的关系

| 路径 | 关系 |
|---|---|
| `00_Notes/requirements/` | 需求与历史架构跳转；**不**放产品代码 |
| `01_AI_Dev_Workflow_Kit/` | 可复用 Prompt 模板、Docker、AI 工作流**经验**；**运行时零耦合** |
| `02_DB_Demo_Studio/` | **本产品**独立 monorepo 根目录（本文档所在） |

---

## 建议目录结构（Phase 1 落地时）

```
02_DB_Demo_Studio/
├── apps/
│   ├── web/
│   │   └── src/features/
│   │       ├── ai-studio/          ★ AI 对话式生成
│   │       ├── execution-player/   ★ 分步执行演示
│   │       └── step-editor/
│   ├── api/                        AI SSE + workflow routes
│   └── renderer/
├── packages/
│   ├── ai-orchestrator/            ★ Agent 编排
│   ├── ai-tools/                   ★ LLM 工具（EXPLAIN 等）
│   ├── execution-workflow/         ★ 执行演示工作流引擎
│   ├── llm-pipeline/
│   ├── prompt-registry/
│   ├── demo-schema/
│   └── ...
├── infra/
└── docs/
```

当前 Phase 0 仅包含 `docs/` 与占位目录；PoC 通过后初始化 monorepo 工具链（pnpm + Turborepo）。

### W1 学习 PoC（本周验收，先于下方 8–10 周纵向切片）

| PoC | 交付 | 验收 |
|---|---|---|
| **#1** | 手写 `DemoPackage` JSON + 最小 Execution Player | 浏览器 ←/→/空格 控制 ≥3 步 |
| **#2** | `explain_mysql` + `explain_postgres` → 工作流 IR | ≥3 步且含 `groundingRef` |
| **#3** | 最小 AI Studio SSE | 单轮对话生成一步讲解词 |

> 下方 Gantt 为 **Phase 1 产品化纵向切片（约 8–10 周）**，与 W1 日计划并行但不等同。

---

## Phase 1 路线图

```mermaid
gantt
    title Phase 1 — AI 纵向切片
    dateFormat YYYY-MM-DD
    section 内核
    DemoPackage + Execution Player   :a1, 2026-06-02, 7d
    execution-workflow + db-engine     :a2, after a1, 7d
    section AI
    ai-tools + ai-orchestrator         :b1, after a2, 10d
    AI Studio SSE 对话生成             :b2, after b1, 7d
    单步 regenerate-step               :b3, after b2, 5d
    section 交付
    Remotion MP4 + 字幕                :c1, after b3, 14d
    LMS + 教师试用                     :d1, after c1, 14d
```

### Phase 1 交付清单

- [ ] **Execution Workflow** — SQL 分步 DAG + EXPLAIN grounding
- [ ] **AI Studio** — 对话流式生成演示初稿（≤60s）
- [ ] **单步 AI 重写** — regenerate-step，不整包重来
- [ ] **DemoPackage** 驱动 Player 与 MP4（步骤一致）
- [ ] LLM 讲解 + 教师编辑；MySQL EXPLAIN；PG 部分对照
- [ ] 非 SQL 工作流 ×3（ER、范式、事务）
- [ ] 交互网页 + 中英字幕 MP4；LMS 试嵌入

### Phase 2 方向（概要）

全课纲 8 大类模板补齐、双引擎完整并排、多 LMS、双语 TTS、案例库版本化、校内私有化运维。详见 [`docs/architecture.md`](./docs/architecture.md) 实施步骤。

---

## 快速开始（PoC 阶段）

1. 阅读 [需求](../00_Notes/requirements/db_demo_video_requirements.md)、[架构 v2](./docs/architecture.md)、[AI 工作流](./docs/ai-workflow.md)
2. PoC **#1**：手写带 `workflowPhase` 的 DemoPackage → Execution Player 分步播放
3. PoC **#2**：`explain_mysql` 工具 → 工作流 IR → 至少 3 步 grounding
4. PoC **#3**：最小 AI Studio — 单轮对话 SSE 生成一步讲解词

---

## 变更记录

| 日期 | 变更 |
|---|---|
| 2026-06-01 | 初始化学习项目目录、架构 canonical、课纲映射初稿 |
| 2026-06-01 | **v2 AI 优先**：architecture 重构、新增 ai-workflow.md |
