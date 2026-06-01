# Day 1 学习指南 — Phase 1 启动

> 日期：2026-05-27  
> 阶段：Phase 1 / W1 / Day 1  
> 今日主题：**建立学习节奏 + 完成 Phase 1 的个人化启动**  
> 预计总时长：**2.5-3 小时**

---

## 开始前（2 分钟）

```powershell
cd d:\AI_Projects\01_Research\Agent_System
git pull
```

打开文件：
1. `00_Learning_Logs/daily/2026-05-27.md` — 今日日志
2. `01_AI_Dev_Workflow_Kit/docs/scenarios.md` — 场景分析
3. `AI_Developer_Research_Roadmap.md` — § Phase 1（第 64-100 行）

---

## 时间块 1（30 min）— 读懂 Phase 1 要学什么

**阅读** `AI_Developer_Research_Roadmap.md` Phase 1 部分。

Phase 1 完整内容（12 个月版，3 个月内 W1 全部完成）：

| 类别 | 具体项 |
|---|---|
| AI 编程工具 | Cursor、Codex、Claude Code、Aider |
| AI 辅助任务 | 需求澄清、架构设计、代码生成、测试、Debug、重构、Code Review |
| Git + AI | diff 审查、issue 生成计划、测试失败定位 |
| 项目产出 | Workflow Kit、5 个 prompt、审查脚本、5 条使用记录 |
| 文章 | 《我是如何把 AI 接入日常开发流程的》 |

**任务：** 在 Daily Log 的「今日思考题」填写：

1. 3 条个人学习目标（针对 Phase 1）
2. 3 个最想 AI 加速的开发场景
3. 最感兴趣的 Agent 方向（Coding / Research / Memory / Evaluation）

**产出：** Daily Log 思考题已填写

---

## 时间块 2（45 min）— 个人化 5 个 AI 编程场景

**编辑** `01_AI_Dev_Workflow_Kit/docs/scenarios.md`

把 5 个场景改成**你自己的真实场景**，每个场景补充：

```markdown
**我的真实案例**：（举一个你最近做过的具体任务）
**预期 AI 帮助**：（AI 应该帮你做什么）
**人工校验点**：（哪里必须自己把关）
```

5 个场景模板已在文件中，重点填：
- 场景 1 需求澄清
- 场景 3 Code Review（最容易今天实战）
- 场景 4 Debug

**产出：** `scenarios.md` 有个人真实案例

---

## 时间块 3（60 min）— 第一次 AI 辅助开发实战 ⭐

这是 Day 1 最重要的环节：**用 AI 完成一个真实小任务并记录。**

### 推荐任务（三选一）

| 选项 | 任务 | 为什么适合 Day 1 |
|---|---|---|
| **A（推荐）** | 给 `ai_commit_review.py` 接入 LLM API | 就在本仓库，立刻有 commit |
| B | 用 Code Review prompt 审查本仓库最新 diff | 纯 prompt 实战，0 代码 |
| C | 你手头任意一个小功能/Bug | 最真实 |

### 实战步骤（选项 A 示例）

**Step 1 — 需求澄清（10 min）**

1. 打开 `01_AI_Dev_Workflow_Kit/prompts/requirements.md`
2. 复制模板到 Cursor Chat
3. 填入任务：「给 ai_commit_review.py 接入 OpenAI API，读取 git diff 生成 Code Review 报告」
4. 保存 AI 输出到 `01_AI_Dev_Workflow_Kit/logs/2026-05-27_ai_commit_review.md`

**Step 2 — 编码（30 min）**

1. 让 Cursor Agent 实现（或自己写）
2. 创建 `.env.example`（不要提交 `.env`）
3. 跑通：`python scripts/ai_commit_review.py`

**Step 3 — 记录（10 min）**

在 log 文件中填写：

```markdown
## 日期：2026-05-27
## 任务：ai_commit_review 接入 LLM

## 我自己原本会怎么做
（写 2-3 句）

## AI 帮我做了什么
（写 2-3 句）

## 哪些地方有效
## 哪些地方无效
## 我如何修正 AI 输出
## 可复用经验
```

**Step 4 — Git commit（5 min）**

```powershell
git add .
git commit -m "feat: ai_commit_review 接入 LLM — Day1 首次 AI 实战"
git commit -m "log: 2026-05-27 daily — Phase1 Day1 场景分析 + 首次实战"  # 如果分开提交
git push
```

**产出：** 1 条 logs/ 使用记录 + 1-2 个 commit

---

## 时间块 4（20 min）— 概念预习 + 收尾

**阅读并补充**（每个写 2-3 句「我自己的理解」）：

- `00_Notes/concepts/agent.md`
- `00_Notes/concepts/mcp.md`
- `00_Notes/concepts/skill.md`

**更新 Daily Log：**
- 勾选今日目标
- 填写「今日产出」「可复用经验」
- 写明日计划

**产出：** 3 张概念卡有个人理解 + Daily Log 完整

---

## Day 1 验收清单

今天结束前，确认以下各项：

- [ ] Daily Log 思考题已填写
- [ ] `scenarios.md` 有 3+ 个个人真实案例
- [ ] `logs/` 有 1 条 AI 辅助开发使用记录
- [ ] 至少 1 次 `git commit` + `git push`
- [ ] 3 张概念卡有「我自己的理解」

**Phase 1 总进度：** Day 1/7（W1 内要完成 Phase 1 全部验收）

---

## W1 剩余 Day 2-7 预览

| 天 | 重点 |
|---|---|
| Day 2 | 5 个 prompt 模板实战 + 第 2 条使用记录 |
| Day 3 | 编码闭环：需求→设计→编码→测试 |
| Day 4 | Debug + Refactor 模板实战 |
| Day 5 | `ai_commit_review.py` 完善（如 Day1 未做完） |
| Day 6 | workflow.md 定稿 + README |
| Day 7 | 周复盘 + Phase 1 自评（7 项验收） |

---

## 今天不要做的事

- ❌ 不要开始 RAG / Agent / MCP 编码（那是 W2+）
- ❌ 不要花超过 30 min 看无关教程
- ❌ 不要追求 prompt 完美——先实战再迭代
- ❌ 不要跳过 log 记录

---

## 需要帮助时

在 Cursor 里直接说：

> 「按 day1_guide.md 选项 A，帮我给 ai_commit_review.py 接入 LLM API」

我会按 Phase 1 的学习目标带你走完整闭环。
