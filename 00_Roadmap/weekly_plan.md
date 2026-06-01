# Weekly Plan - 2026-W22

> 周期：2026-05-26 ~ 2026-06-01  
> 总目标：**3 个月完成 12 个月全部内容** → [`3month_full_plan.md`](3month_full_plan.md)  
> 今日指南 → Day 1 [`day1_workflow.md`](day1_workflow.md) · Day 2 [`day2_guide.md`](day2_guide.md)  
> API 约束 → [`learning_constraints.md`](learning_constraints.md)  
> 阶段：M1 Week 1 — AI 辅助开发工作流  
> 主题：Git 初始化 + Workflow Kit 完成

---

## 本周目标

1. 搭建完整的学习记录体系（目录、模板、看板）。
2. 明确个人 AI 辅助开发工作流。
3. 收集并整理 5 个 AI 编程常用场景。
4. 完成 AI Dev Workflow Kit 第一版骨架。

---

## 重点任务（只列 5 件）

| 优先级 | 任务 | 状态 | 产出 |
|:---:|---|---|---|
| P0 | 初始化 Git 并完成首次 commit | Done | 已 push 到 GitHub |
| P0 | 创建学习管理目录与模板 | Done | `00_*` 目录结构 |
| P0 | 写第一篇 Daily Log | Done | `2026-05-27.md` |
| P1 | 整理 5 个 AI 编程场景 | Done | `01_AI_Dev_Workflow_Kit/docs/scenarios.md` |
| P1 | 写第一版 AI 开发工作流 | In Progress | `01_AI_Dev_Workflow_Kit/docs/workflow.md` |
| P2 | 完成 3 个 Prompt 模板 | In Progress | `prompts/*.md`（requirements 已实战） |
| P0 | ai_commit_review DeepSeek 接入 | Done | 提前于 Day 5 完成 |

---

## 每日安排

### Day 1（2026-05-27）— 系统搭建 + 首次 AI 实战 ✅

- [x] 创建 `00_Roadmap`、`00_Learning_Logs`、`00_Notes`、`00_Portfolio`
- [x] 创建 `project_matrix.md`、本周计划、今日日志
- [x] 阅读路线图 Phase 1 部分，写下 3 条个人学习目标
- [x] 列出 5 个你日常开发中最想用 AI 加速的场景
- [x] ai_commit_review 接入 DeepSeek API（提前完成）
- [x] 第 1 条 AI 辅助开发使用记录

### Day 2（2026-05-28）— 场景与模板

> 详细流程：[`day2_guide.md`](day2_guide.md)

- [ ] 完善 `scenarios.md`：每个场景写「人工做法 vs AI 做法」
- [ ] 完成 `prompts/requirements.md` 和 `prompts/architecture.md`
- [ ] 用 Cursor 实际完成一个小任务，记录过程

### Day 3（2026-05-29）— 编码闭环

- [ ] 完成 `prompts/code_review.md`
- [ ] 选一个小功能，走一遍：需求 → 设计 → 编码 → 测试
- [ ] 写一条 AI 辅助开发过程记录

### Day 4（2026-05-30）— Debug 与重构

- [ ] 完成 `prompts/debug.md` 和 `prompts/refactor.md`
- [ ] 找一个真实 Bug 或构造失败测试，用 AI 辅助定位
- [ ] 记录 Debug 过程

### Day 5（2026-05-31）— 工具脚本

- [x] 实现 `scripts/ai_commit_review.py` DeepSeek 版（Day 1 提前完成）
- [x] 测试：读取 git diff → 生成审查报告

### Day 6（2026-06-01）— 整合

- [ ] 完善 `docs/workflow.md`
- [ ] 更新 README
- [ ] 写概念笔记：Agent / MCP / Skill 各 1 条（预习）

### Day 7（2026-06-02）— 周复盘

- [ ] 写 `2026-W22.md` 周复盘
- [ ] 更新 `project_matrix.md` 状态
- [ ] 确定下周 Phase 1 收尾任务

---

## 本周阅读

- [ ] Cursor 官方文档：Rules、Skills、MCP 概览
- [ ] Anthropic MCP 介绍页（预习 Phase 3）
- [ ] 路线图 §1.2 关键词定位（Agent / MCP / Skill / OpenHands / HNSW）

---

## 验收标准（Week 1 结束）

- 学习管理系统可正常使用，至少 5 篇 Daily Log
- AI Dev Workflow Kit 有 README + 5 个 prompt 模板 + workflow 文档
- 至少 3 条真实 AI 辅助开发使用记录
- 能口头讲清楚：AI 在你开发流程中的 3 个具体作用点
