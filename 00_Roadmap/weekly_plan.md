# Weekly Plan - 2026-W22

> 周期：2026-05-26 ~ 2026-06-01（W1 可延续至 2026-06-02 周复盘）  
> 总目标：**12 周完成完整路线图** → [`3month_plan.md`](3month_plan.md)  
> **Phase 1 实战代码库：** [`02_DB_Demo_Studio/`](../02_DB_Demo_Studio/)  
> **工作流工具包：** [`01_AI_Dev_Workflow_Kit/`](../01_AI_Dev_Workflow_Kit/)  
> 今日指南 → Day 1 [`day1_guide.md`](day1_guide.md) · 历史 [`day1_2026-05-27_workflow.md`](day1_2026-05-27_workflow.md) · Day 2 [`day2_2026-05-28_guide.md`](day2_2026-05-28_guide.md)  
> API 约束 / 命名规范 → [`learning_constraints.md`](learning_constraints.md)  
> 阶段：M1 Week 1 — AI 辅助开发工作流 + DB Demo Studio PoC

---

## 本周目标

1. 搭建完整的学习记录体系（目录、模板、看板）— ✅ 已启动
2. 明确个人 AI 辅助开发工作流（模板在 Kit，实战在 Studio）
3. 在 **DB Demo Studio** 上完成 PoC #1 路径（DemoPackage → Player）
4. 收集 **5 条** AI 辅助开发使用记录（`02_DB_Demo_Studio/logs/` 或 `01_AI_Dev_Workflow_Kit/logs/`）
5. 完成 AI Dev Workflow Kit 第一版骨架（prompt + workflow 文档）

---

## Week 1 任务分解（DB Demo Studio）

| 天 | AI 工作流环节 | DB Demo Studio 交付 | 使用记录 |
|---|---|---|---|
| D1 | 需求澄清 | 读 requirements + PoC #1 结构化需求 / 样例 JSON | `logs/*_poc_player*` |
| D2 | 架构设计 | 细化 `demo-schema` / 模块边界（@ architecture.md） | `logs/*_architecture*` |
| D3 | 编码 + 测试 | 最小 Player 或 JSON Schema 校验脚本 | `logs/*_player_poc*` |
| D4 | Debug | 修复步进、空步骤、JSON 校验失败 | `logs/*_debug*` |
| D5 | Code Review | 可选 `ai_commit_review.py --unstaged` 审查 Studio diff | `logs/review_*` |
| D6 | 整合文档 | `workflow.md` v1 + 双项目 README 对齐 | — |
| D7 | 周复盘 | `2026-W22.md` + `project_matrix.md` 更新 | Phase 1 自评 |

**PoC #1 验收（architecture 实施步骤 #1）：** 手写 `DemoPackage` JSON → 浏览器 Player 用 ←/→/空格 控制 ≥3 步。

---

## 重点任务（只列 5 件）

| 优先级 | 任务 | 状态 | 产出 |
|:---:|---|---|---|
| P0 | DB Demo Studio PoC #1（DemoPackage + Player） | In Progress | `02_DB_Demo_Studio/` 可见代码/样例 |
| P0 | 5 条 AI 辅助开发使用记录 | In Progress | `02_DB_Demo_Studio/logs/` 为主 |
| P1 | 5 个 Prompt 模板实战验证 | In Progress | Kit `prompts/*.md` |
| P1 | `workflow.md` 定稿 | In Progress | 双项目路径写清 |
| P2 | 可选：`ai_commit_review.py` 审查 Studio 变更 | Done（脚本） / 待复用 | Kit `logs/review_*` |

---

## 每日安排

### Day 1（2026-05-27）— 系统搭建 + 首次 AI 实战 ✅

- [x] 创建 `00_Roadmap`、`00_Learning_Logs`、`00_Notes`、`00_Portfolio`
- [x] 学习管理体系 + 首次 DeepSeek 实战（`ai_commit_review`，侧车工具）
- [x] 第 1 条 AI 辅助开发使用记录（Kit）

> **2026-06-01 起：** Phase 1 主代码库切换为 `02_DB_Demo_Studio`。新 Day 1 任务见 [`day1_guide.md`](day1_guide.md)。

### Day 2（2026-05-28）— 场景 + 架构 Prompt ✅

> 详细流程：[`day2_2026-05-28_guide.md`](day2_2026-05-28_guide.md)

- [x] 整理 `scenarios.md`（案例指向 DB Demo Studio）
- [x] 用 `prompts/architecture.md` 细化 `ai-orchestrator` / 模块划分
- [x] 第 2 条使用记录 → `02_DB_Demo_Studio/logs/2026-06-01_day2_ai_orchestrator_architecture.md`

### Day 3（2026-06-01）— 编码闭环：PoC #1 ⭐

- [ ] 补 Day 2 遗留：`workflow.md` v0.3 + 概念卡（agent / mcp / skill）
- [ ] 定义 `packages/demo-schema/schema.json`（DemoPackage JSON Schema）
- [ ] 手写 JOIN 5 步样例 `examples/join-query.json`
- [ ] 校验 schema / 样例 JSON
- [ ] 第 3 条使用记录

### Day 4 — Debug / Player 骨架

- [ ] `prompts/debug.md` 实战（Schema 校验问题 / 边界情况）
- [ ] 第 4 条使用记录

### Day 5 — Player 前端 + 整合

- [ ] 最小 Execution Player（支持 ←/→/空格步进，≥3 步手动 JSON）
- [ ] `python scripts/ai_commit_review.py --unstaged` 审查 Studio 变更
- [ ] 第 5 条使用记录

### Day 6 — 整合

- [ ] 更新 `02_DB_Demo_Studio/README.md` + 根 `README.md`
- [ ] 概念笔记：Agent / MCP / Skill

### Day 7 — 周复盘

- [ ] 写 `2026-W22.md`（或当前周）周复盘
- [ ] 更新 `project_matrix.md`
- [ ] Phase 1 七项验收自检（见 `3month_plan.md`）

---

## 本周阅读

- [ ] `02_DB_Demo_Studio/docs/architecture.md` — PoC 顺序与 Phase 1 步骤
- [ ] `02_DB_Demo_Studio/docs/curriculum-mapping.md` — 课纲与模板优先级
- [ ] Cursor 官方文档：Rules、MCP 概览
- [ ] 路线图 §1.2 关键词（Agent / MCP / Skill）

---

## 验收标准（Week 1 结束）

- 学习管理系统可正常使用，至少 5 篇 Daily Log
- **DB Demo Studio：** PoC #1 可演示（JSON + Player 步进）或等价可验收产物
- AI Dev Workflow Kit：5 个 prompt 模板 + workflow 文档
- **至少 5 条**真实 AI 辅助开发使用记录（Studio logs 优先）
- 能口头讲清楚：AI 在 **DB Demo Studio 开发** 中的 3 个作用点
