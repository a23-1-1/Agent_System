# 课纲 — 模板与工作流映射表

| 字段 | 值 |
|---|---|
| **日期** | 2026-06-01 |
| **状态** | v2 — 对齐 AI 执行工作流 |
| **关联** | [需求](../../00_Notes/requirements/db_demo_video_requirements.md) · [架构](./architecture.md) · [AI 工作流](./ai-workflow.md) |

> 将课纲章节映射到 `templateType`、**workflowType** 与 AI Agent 工具链。

---

## workflowType 说明

| workflowType | 适用 | 标准阶段（workflowPhase） |
|---|---|---|
| `sql-execution` | SQL 查询类 | lex → parse → optimize → plan → execute → result |
| `concept-progression` | ER/范式/事务/B+树/恢复 | concept → transform → compare → summary |

**AI 规则：** `sql-execution` 类必须经过 `explain_mysql` / `explain_postgres` 工具；`plan`/`execute` 步须有 `groundingRef`。

---

## 8 大类课纲节点

| # | 课纲章节 | templateType | workflowType | Phase 1 | AI 工具链 |
|:---:|---|---|:---:|:---:|---|
| 1 | 关系模型与 SQL 基础 | `sql-explain` | `sql-execution` | ✅ | sql_analyze → explain_* → assemble_steps |
| 2 | 多表查询（JOIN） | `sql-explain` | `sql-execution` | ✅ | 同上 + 引擎对照 |
| 3 | 聚合与分组 | `sql-explain` | `sql-execution` | ✅ | 同上 |
| 4 | ER 建模 | `er-model` | `concept-progression` | ✅ | curriculum_search → concept 步 |
| 5 | 范式分解 | `normalization` | `concept-progression` | ✅ | transform 步（1NF→3NF） |
| 6 | 事务与 ACID | `transaction` | `concept-progression` | ✅ | 时间线 + concept 步 |
| 7 | 索引与 B+ 树 | `bplus-tree` | `concept-progression` | Phase 2 | B+ 树 viz + concept |
| 8 | 查询优化与执行计划 | `sql-explain` | `sql-execution` | ✅ | 双引擎 explain + compare |
| 9 | 存储、日志与恢复 | `storage-recovery` | `concept-progression` | Phase 2 | WAL 示意 concept 步 |

---

## AI Studio 快捷指令 × 课纲

| Slash 指令 | 典型课纲 | 触发的 workflow |
|---|---|---|
| `/generate` | 任意 | 完整 Agent 循环 |
| `/compare-engine` | JOIN、优化 | sql-execution + 双 EXPLAIN |
| `/simplify` | 全部 | regenerate-step（当前步） |
| `/bilingual` | 全部 | translate_bilingual |

---

## Phase 1 优先顺序（AI PoC）

1. 单表 SELECT — 验证 `sql-execution` + AI Studio 流式 3 步
2. INNER JOIN — 验证 EXPLAIN grounding + PlanTree
3. ER 建模 — 验证 `concept-progression`
4. 范式 — concept-progression + transform 步
5. 事务 — concept-progression + 时间线 viz
6. JOIN 双引擎 — `/compare-engine`

---

## 变更记录

| 日期 | 变更 |
|---|---|
| 2026-06-01 | 初稿 |
| 2026-06-01 | v2：workflowType、AI 工具链、Slash 映射 |
