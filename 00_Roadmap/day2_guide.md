# Day 2 学习指南 — 场景打磨 + 架构 Prompt 实战

> 日期：2026-05-28  
> 阶段：Phase 1 / W1 / Day 2  
> 今日主题：**完善场景文档 + 架构设计 Prompt 实战 + 第 2 条使用记录**  
> 预计总时长：**2.5-3 小时**  
> API 策略：仅 DeepSeek → 见 [`learning_constraints.md`](learning_constraints.md)  
> 昨日复盘：[`day1_workflow.md`](day1_workflow.md)

---

## 开始前（2 分钟）

```powershell
cd d:\AI_Projects\01_Research\Agent_System
git pull
```

打开文件：
1. `00_Learning_Logs/daily/2026-05-28.md` — 今日日志（新建）
2. `01_AI_Dev_Workflow_Kit/docs/scenarios.md` — 检查格式
3. `01_AI_Dev_Workflow_Kit/prompts/architecture.md` — 今日主 Prompt
4. `00_Roadmap/weekly_plan.md` — Day 2 任务

---

## Day 1 遗留（如有空先补）

- [ ] `00_Notes/concepts/agent.md` / `mcp.md` / `skill.md` — 「我自己的理解」各 2-3 句
- [ ] `01_AI_Dev_Workflow_Kit/docs/scenarios.md` — 清理多余 markdown 代码块，统一格式
- [ ] `01_AI_Dev_Workflow_Kit/docs/workflow.md` — 更新 v0.2（ai_commit_review 已接入 DeepSeek）

---

## 时间块 1（30 min）— 整理 scenarios.md 格式

**文件：** `01_AI_Dev_Workflow_Kit/docs/scenarios.md`

**任务：** 把 Day 1 填写的 5 个场景统一成下面格式（内容已有，主要是排版）：

```markdown
**我的真实案例**：……
**预期 AI 帮助**：……
**人工校验点**：……

**使用记录**：
- 2026-05-27：需求澄清 + Code Review → logs/2026-05-27_ai_commit_review*.md
```

**验收：** 5 个场景格式一致，无嵌套 ```markdown 代码块

---

## 时间块 2（45 min）— 架构设计 Prompt 实战 ⭐

**今日主任务：** 用 `prompts/architecture.md` 为「智慧课堂助手」或 Workflow Kit 下一功能做架构设计。

### 推荐任务（二选一）

| 选项 | 任务 | 适合原因 |
|---|---|---|
| **A（推荐）** | 为 Workflow Kit 设计「Debug 辅助脚本」架构 | 仍在 Phase 1 项目内，Day 4 可编码 |
| B | 为智慧课堂助手智能备课模块做架构 | 你的真实项目，面试故事更强 |

### 实战步骤

**Step 1 — 打开 Prompt（5 min）**

1. 打开 `01_AI_Dev_Workflow_Kit/prompts/architecture.md`
2. 复制模板到 Cursor Chat
3. 填入：现有 `01_AI_Dev_Workflow_Kit/` 目录结构 + 新功能描述

**Step 2 — 生成并保存（25 min）**

保存 AI 输出到：
```
01_AI_Dev_Workflow_Kit/logs/2026-05-28_architecture_debug_helper.md
```

**Step 3 — 人工校验（15 min）**

对照 checklist 标记：
- [ ] 模块划分是否合理
- [ ] 是否复用了现有 prompts/ 和 scripts/ 结构
- [ ] 是否考虑了 DeepSeek API 约束（见 learning_constraints.md）
- [ ] 是否有可测试的接口定义

**验收：** logs/ 下有架构设计文档，scenarios.md 场景 2 追加使用记录

---

## 时间块 3（45 min）— 完善 Prompt 模板 + workflow 文档

**文件 1：** `01_AI_Dev_Workflow_Kit/prompts/requirements.md`

在「使用记录」表格追加 Day 1 一行：

| 日期 | 任务 | 效果 | 改进 |
|---|---|---|---|
| 2026-05-27 | ai_commit_review 需求澄清 | 有效，帮想全验收标准 | 下次先填现有上下文 |

**文件 2：** `01_AI_Dev_Workflow_Kit/prompts/architecture.md`

同样在「使用记录」表格追加 Day 2 实战行。

**文件 3：** `01_AI_Dev_Workflow_Kit/docs/workflow.md`

更新到 v0.2：
- ai_commit_review 已接入 DeepSeek ✅
- 真实使用记录：1 条 → 目标 5 条
- Git + AI 工作流中补充 DeepSeek 配置步骤

**验收：** workflow.md 反映当前真实状态

---

## 时间块 4（30 min）— 用 ai_commit_review 审查今日变更

**任务：** 把 Day 2 写的文档改动走一遍 Code Review 闭环。

```powershell
cd d:\AI_Projects\01_Research\Agent_System
git add -A
git status   # 确认 .env 不在列表中
cd 01_AI_Dev_Workflow_Kit
python scripts/ai_commit_review.py --unstaged
```

**产出：**
- `logs/review_YYYYMMDD_HHMMSS.md` — 第 2 份审查报告
- 在 Daily Log 写 3 行摘要

**验收：** 第 2 次成功运行 ai_commit_review（使用记录 2/5）

---

## 时间块 5（20 min）— Daily Log + 概念卡 + 收尾

**文件：**
- `00_Learning_Logs/daily/2026-05-28.md` — 勾选目标、写产出、明日计划
- `00_Notes/concepts/agent.md` — 补「我自己的理解」（如 Day 1 未写）

**明日预览（Day 3）：** 编码闭环 — 需求 → 设计 → 编码 → 测试，完成 debug prompt 实战

---

## Day 2 验收清单

今天结束前确认：

- [ ] `scenarios.md` 格式统一，5 场景完整
- [ ] `logs/2026-05-28_architecture_*.md` 架构设计产出
- [ ] `prompts/requirements.md` 和 `prompts/architecture.md` 有使用记录
- [ ] `workflow.md` 更新到 v0.2
- [ ] ai_commit_review 第 2 次运行成功
- [ ] Daily Log `2026-05-28.md` 完整
- [ ] ≥ 1 次 git commit（你确认后提交）

**Phase 1 进度目标：** 使用记录 2/5 · Prompt 实战 2/5

---

## 需要帮助时

在 Cursor 里说：

> 「按 day2_guide.md 选项 A，帮我用 architecture.md 设计 Debug 辅助脚本，输出保存到 logs/」

或：

> 「帮我整理 scenarios.md 格式，并更新 workflow.md 到 v0.2」

---

## 今天不要做的事

- ❌ 不要开始 RAG / MCP / Agent 编码（W2+）
- ❌ 不要换 OpenAI/Claude API — 统一 DeepSeek
- ❌ 不要把 API Key 写进任何 md 文件或 .env.example
