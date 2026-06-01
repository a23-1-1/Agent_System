# Day 1 学习流程复盘 — Phase 1 启动

> 文件名：`day1_2026-05-27_workflow.md`  
> 日期：2026-05-27  
> 阶段：Phase 1 / W1 / Day 1  
> 主题：学习管理系统 + 首次 AI 辅助开发实战  
> 实际耗时：约 3 h  
> API 策略：仅 DeepSeek → 见 [`learning_constraints.md`](learning_constraints.md)

---

## 流程总览

```text
搭系统 → 定目标 → 个人化场景 → 需求澄清 → 编码实战 → 跑通审查 → 写记录 → commit
```

---

## Step 1 · 搭建学习管理系统（已完成）

**做了什么：**
- 创建 `00_Roadmap/`、`00_Learning_Logs/`、`00_Notes/`、`00_Portfolio/`
- 创建 `01_AI_Dev_Workflow_Kit/` 项目骨架
- Git 初始化并 push 到 GitHub

**产出文件：**
- `00_Roadmap/weekly_plan.md`
- `00_Roadmap/project_matrix.md`
- `00_Learning_Logs/daily/2026-05-27.md`
- `01_AI_Dev_Workflow_Kit/prompts/*.md`（5 个模板骨架）

**验收：** 目录结构完整，首次 commit 已 push

---

## Step 2 · 明确个人学习目标（已完成）

**在哪里写：** `00_Learning_Logs/daily/2026-05-27.md` → 「今日思考题」

**填写内容摘要：**
1. **AI 加速 3 场景**：Code Review、Debug、需求澄清
2. **12 个月目标**：独立设计 Agent 系统，RAG + MCP + Coding Agent 项目与实验记录
3. **兴趣方向**：Coding Agent（OpenHands 规划/改代码/跑测试）

**验收：** 3 道思考题均已填写

---

## Step 3 · 个人化 AI 编程场景（已完成）

**在哪里写：** `01_AI_Dev_Workflow_Kit/docs/scenarios.md`

**5 个场景真实案例：**
| 场景 | 个人案例 |
|---|---|
| 需求澄清 | 智能课堂助手 — 智能备课功能 |
| 架构设计 | 智慧课堂助手功能架构 |
| Code Review | ai_commit_review.py 提交前自查 |
| Debug | 页面点击失效 |
| 重构 | 原生 HTML/JS/CSS → Vue |

**验收：** 5 个场景均有「真实案例 / 预期 AI 帮助 / 人工校验点」

---

## Step 4 · 需求澄清实战（已完成）

**怎么用 Prompt：**
1. 打开 `01_AI_Dev_Workflow_Kit/prompts/requirements.md`
2. 复制模板到 Cursor Chat
3. 填入任务：「给 ai_commit_review.py 接入 DeepSeek API，读取 git diff 生成 Code Review 报告」

**产出文件：**
- `01_AI_Dev_Workflow_Kit/logs/2026-05-27_ai_commit_review_requirements.md`

**验收：** 含需求摘要、功能清单 P0/P1、验收标准、技术约束（DeepSeek）

---

## Step 5 · 编码实战 — ai_commit_review 接入 DeepSeek（已完成）

**改了什么：**
- `01_AI_Dev_Workflow_Kit/scripts/ai_commit_review.py` — 接入 DeepSeek API
- `01_AI_Dev_Workflow_Kit/.env.example` — 环境变量模板
- `01_AI_Dev_Workflow_Kit/requirements.txt` — openai + python-dotenv
- `01_AI_Dev_Workflow_Kit/Dockerfile` + `docker-compose.yml` — 可选 Docker 运行

**核心能力：**
- 读取 staged / unstaged / 指定 commit 的 git diff
- 用 `prompts/code_review.md` 作 system prompt
- 调用 DeepSeek 生成 P0-P3 分级审查报告
- 报告写入 `logs/review_*.md`

**测试命令：**
```powershell
cd d:\AI_Projects\01_Research\Agent_System\01_AI_Dev_Workflow_Kit
copy .env.example .env   # 本地填入 Key，不进 git
pip install -r requirements.txt
python scripts/ai_commit_review.py --unstaged
```

**验收：**
- [x] 脚本跑通，生成真实 LLM 报告
- [x] 报告含 P0-P3 分级
- [x] `.env` 未被 git 跟踪

---

## Step 6 · 使用记录（已完成）

**在哪里写：**
- `01_AI_Dev_Workflow_Kit/logs/2026-05-27_ai_commit_review.md` — 过程复盘
- `01_AI_Dev_Workflow_Kit/logs/review_20260601_012246.md` — 脚本自动生成的审查报告

**验收：** logs/ 下有 ≥ 1 条完整使用记录 + 1 份审查报告

---

## Step 7 · 概念预习（部分完成）

**在哪里写：** `00_Notes/concepts/agent.md`、`mcp.md`、`skill.md` → 「我自己的理解」

**Day 1 关联：**
- Agent：`ai_commit_review` = 读 diff → 调 DeepSeek → 写报告（Agent 雏形）
- MCP：Phase 3 再做，Day 1 仅概念预习
- Skill：Cursor SKILL.md 是可复用流程单元

---

## Day 1 验收对照

| 验收项 | 状态 |
|---|---|
| Daily Log 思考题已填 | ✅ |
| scenarios.md 有个人案例 | ✅（5 个） |
| logs/ 有使用记录 | ✅（1 条 + 1 报告） |
| ai_commit_review.py 可运行 | ✅（DeepSeek） |
| git commit | ✅（本次提交） |
| 概念卡有个人理解 | 🔄 Day 2 补充完善 |

**Phase 1 总进度：** 使用记录 1/5 · Prompt 实战 1/5 · workflow 文档 v0.1

---

## 可复用经验（Day 1 总结）

1. **先需求澄清再编码** — requirements 模板帮你想全边界条件，少返工
2. **模板写在哪、填什么要事先约定** — 避免「不知道写在哪」
3. **API Key 只放 .env** — `.env.example` 用占位符
4. **每条实战都要有 logs/** — 这是 Phase 1 验收硬指标

---

## 相关文件索引

| 类型 | 路径 |
|---|---|
| 今日日志 | `00_Learning_Logs/daily/2026-05-27.md` |
| 场景分析 | `01_AI_Dev_Workflow_Kit/docs/scenarios.md` |
| 需求澄清 | `01_AI_Dev_Workflow_Kit/logs/2026-05-27_ai_commit_review_requirements.md` |
| 使用记录 | `01_AI_Dev_Workflow_Kit/logs/2026-05-27_ai_commit_review.md` |
| 审查报告 | `01_AI_Dev_Workflow_Kit/logs/review_20260601_012246.md` |
| 学习约束 | `00_Roadmap/learning_constraints.md` |
| 明日指南 | `00_Roadmap/day2_2026-05-28_guide.md` |
