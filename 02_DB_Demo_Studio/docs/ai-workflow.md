# AI 交互生成与执行演示工作流 — 详设

| 字段 | 值 |
|---|---|
| **日期** | 2026-06-02 |
| **父文档** | [`architecture.md`](./architecture.md) |
| **状态** | v2 — 已对齐 Flask + Python 全栈 |

---

## 1. 设计目标

| 目标 | 说明 |
|---|---|
| **AI 交互式生成** | 教师通过自然语言与系统对话，**流式**获得演示初稿，而非填表点按钮 |
| **执行演示工作流** | SQL/概念被拆解为**可逐步推进**的标准阶段，每步可 grounding |
| **人机协作** | AI 生成 → 教师预览 → 对话修改单步 → 定稿，循环直至满意 |
| **双交付同源** | 所有 AI 输出写入 `DemoPackage`，驱动 Player 与 MP4 |

---

## 2. AI Studio — 交互界面

### 2.1 布局

```text
┌─────────────────────────────────────────────────────────────┐
│  AI Studio — 数据库演示助手                                    │
├──────────────────────┬──────────────────────────────────────┤
│  对话区               │  实时预览区                            │
│  ─────────────────   │  ┌────────────────────────────────┐  │
│  教师: 讲这个 JOIN    │  │  Execution Player（分步）       │  │
│  AI: 正在 EXPLAIN…   │  │  [1 解析] [2 计划] [3 执行] …   │  │
│  AI: 已生成 4 步      │  │  ▶ 当前步骤动画 + 讲解词          │  │
│                      │  └────────────────────────────────┘  │
│  [输入框] [发送]      │  步骤列表 │ 编辑 │ Ask AI 重写此步    │
└──────────────────────┴──────────────────────────────────────┘
```

### 2.2 快捷指令（Slash Commands）

| 指令 | 行为 |
|---|---|
| `/generate` | 根据当前 SQL/课纲触发完整工作流 |
| `/simplify` | 对当前步骤 regenerate（面向基础班） |
| `/compare-engine` | 触发 MySQL vs PG 对照步骤 |
| `/add-step` | AI 建议在 DAG 中插入一步 |
| `/bilingual` | 生成/更新英文字幕与讲解 |
| `/export` | 打开导出面板（MP4 + 网页） |

### 2.3 SSE 事件协议

```typescript
// 客户端订阅 POST /ai/sessions/:id/chat
interface AiStreamEvent {
  type:
    | 'assistant-text'      // AI 说明正在做什么
    | 'tool-start'          // 开始调用 explain_mysql 等
    | 'tool-result'         // 工具返回摘要（不含敏感 SQL 全文给前端日志）
    | 'workflow-phase'      // 工作流阶段变更
    | 'step-draft'          // 新步骤初稿（增量追加）
    | 'step-updated'        // 单步被重写
    | 'demo-complete'       // DemoPackage 初稿完成
    | 'error';
  payload: unknown;
}
```

---

## 3. Demo Agent — 编排逻辑

### 3.1 Agent 角色定义（System Prompt 要点）

```markdown
你是 DB Demo Studio 的 AI 演示助手，帮助大学数据库课教师生成分步执行演示。

规则：
1. 生成 SQL 演示前，默认必须同时调用 explain_mysql 与 explain_postgres；若某一引擎失败，须记录 engineFallback / issues[] 并在 DemoPackage 中标注降级原因，不得静默省略
2. 每一步必须对应 workflowPhase，并引用 groundingRef
3. 讲解词面向本科生，避免未解释术语
4. 不确定时向教师提问，不要编造执行计划
5. 输出结构化 DemoStep，而非自由散文
```

### 3.2 ReAct 循环（简化）

```text
Thought → Action(tool, args) → Observation → … → Final DemoPackage
```

| 典型 Action 序列（SQL JOIN） | 说明 |
|---|---|
| `curriculum_search("JOIN")` | 获取课纲上下文与示例 |
| `sql_analyze(sql)` | 语法校验 |
| `explain_mysql(sql)` | MySQL 计划 |
| `explain_postgres(sql)` | PG 计划 |
| `assemble_execution_steps(...)` | 工作流引擎产出 DAG |
| `generate_narration(stepId)` × N | 逐步讲解 |
| `generate_visual_spec(stepId)` × N | 动画脚本 |
| `translate_bilingual(...)` | 英文字幕 |
| `validate_demo_package(...)` | 校验通过才 demo-complete |

### 3.3 单步重写（regenerate-step）

```text
输入: stepId=3, hint="面向大一，少术语"
上下文: 该步 groundingRef + 前后步骤 narration + EXPLAIN 片段
输出: 更新后的 DemoStep（仅一步）
副作用: demo.metadata.lastAiAction = 'regenerate-step'
```

---

## 4. Execution Workflow — 工作流引擎

### 4.1 工作流类型

| workflowType | 适用章节 | 标准阶段 |
|---|---|---|
| `sql-execution` | SELECT/JOIN/聚合/子查询 | lex → parse → optimize → plan → execute → result |
| `concept-progression` | ER/范式/事务/B+树/恢复 | concept → transform → compare → summary |

### 4.2 SQL 执行工作流 IR

```typescript
interface ExecutionWorkflowIR {
  workflowId: string;
  sql: string;
  phases: WorkflowPhase[];
  enginePlans: { mysql?: ExplainSnapshot; postgres?: ExplainSnapshot };
  stepMapping: Array<{ stepId: string; phase: string; explainNodeId?: string }>;
}

interface WorkflowPhase {
  id: string;
  order: number;
  phase: 'lex' | 'parse' | 'optimize' | 'plan' | 'execute' | 'result';
  label: { zh: string; en: string };
  engineEvidence?: { mysql?: unknown; postgres?: unknown };
  simplification?: boolean; // 是否为教学简化步骤
}
```

### 4.3 组装规则（assemble_execution_steps）

1. 从 `sql-analyzer` 获取 AST → 至少产生 `parse` 步
2. 从 `db-engine` 获取 EXPLAIN → 映射为 `plan` / `execute` 步
3. 若 MySQL 与 PG 计划结构差异 > 阈值 → 插入 `compare` 子步（Phase 1 可选）
4. AI **不得**添加 IR 中不存在的 `plan`/`execute` 阶段（校验在 `validate_demo_package`）

---

## 5. packages/ai-tools 工具清单

| 工具名 | 输入 | 输出 | Grounding |
|---|---|---|---|
| `curriculum_search` | query, nodeId? | 课纲片段、示例 SQL | 静态 JSON / 向量库 |
| `sql_analyze` | sql | AST、errors | 解析器 |
| `explain_mysql` | sql | ExplainSnapshot | Docker 沙箱 |
| `explain_postgres` | sql | ExplainSnapshot | Docker 沙箱 |
| `assemble_execution_steps` | sql, plans | ExecutionWorkflowIR | 规则引擎 + IR |
| `generate_narration` | step, context | zh/en 文案 | LLM |
| `generate_visual_spec` | step, vizType | VisualSpec | LLM → schema 约束 |
| `translate_bilingual` | text, targetLang | string | LLM |
| `validate_demo_package` | DemoPackage | ok / errors[] | Zod + 规则 |

---

## 6. Prompt Registry

路径：`packages/prompt-registry/prompts/`

| Prompt ID | 用途 | 版本策略 |
|---|---|---|
| `agent-system` | Demo Agent 系统角色 | semver，变更需回归测试 |
| `narration-step` | 单步讲解词 | 按课纲模板变体 |
| `visual-spec` | 动画脚本 | 绑定 viz-primitives 类型枚举 |
| `regenerate-step` | 单步重写 | 含 hint 注入 |
| `bilingual-translate` | 英译/中译 | 独立 |

---

## 7. 三场景下的 AI 行为

| 场景 | AI 能力 | 限制 |
|---|---|---|
| **备课（ai-studio）** | 完整对话、生成、重写、导出 | 教师权限 |
| **课堂（execution-player）** | 可选「AI 补充讲解」一键朗读当前步 | 无编辑；低延迟 |
| **自学（study）** | 可选「向 AI 提问本演示」（Phase 2） | 仅基于已发布 Demo grounding |

---

## 8. Phase 1 PoC 验收（AI 专项）

- [ ] 教师发送自然语言 + SQL，**60s 内** SSE 收到 ≥3 个 `step-draft` 事件
- [ ] 每步 `workflowPhase` 非空；SQL 类至少 1 步 `groundingRef` 指向 EXPLAIN
- [ ] 「讲简单点」触发 `regenerate-step`，仅该步 narration 变化
- [ ] `validate_demo_package` 拒绝无 grounding 的 plan/execute 步
- [ ] 定稿 DemoPackage 驱动 Player 与 MP4 步骤一致

---

## 变更记录

| 日期 | 变更 |
|---|---|
| 2026-06-02 | v2：技术栈更新 —— Flask + React + Tailwind + Python 全栈 |
