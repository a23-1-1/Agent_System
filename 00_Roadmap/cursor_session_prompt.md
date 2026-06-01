# Cursor 学习对话管理

> 怎么用新对话继续学，而不丢失上下文。

---

## 1. Git 分支 vs Cursor 新对话

| 方式 | 要不要用 | 说明 |
|---|---|---|
| **Git 分支** | ❌ 日常学习不需要 | 继续用 `main`，每天 commit 即可 |
| **Git 分支** | ✅ 仅实验性重构时 | 如 `exp/db-demo-player-v2`，失败可删 |
| **Cursor 新对话** | ✅ 推荐 | 每 3-5 天或每个 Phase 开新对话 |

**结论：代码不用建分支，对话要定期新开。**

---

## 2. 什么时候开新对话

开新对话（复制下方提示词）：

- ✅ 每 3-5 天日常学习
- ✅ 每个 Phase / 每周开始（W1→W2…）
- ✅ 对话明显变慢、回答变散
- ✅ 切换大任务（如 Phase1→Phase2 RAG）

继续当前对话：

- ✅ 同一个 PoC/功能没做完（如 DB Demo Player 步进未验收）
- ✅ 需要引用刚才的错误/代码上下文

---

## 3. 在 Cursor 开新对话的步骤

1. `Ctrl+L` 或点击 **New Chat**
2. 在输入框 **@** 引用这些文件（按顺序）：
   - `@AI_Developer_Research_Roadmap.md`
   - `@AI_Learning_Management_Plan.md`
   - `@00_Roadmap/3month_plan.md`
   - `@00_Roadmap/weekly_plan.md`
   - `@02_DB_Demo_Studio/README.md`
   - `@00_Roadmap/day{N}_{YYYY-MM-DD}_guide.md` 或 `@00_Roadmap/day1_guide.md`
   - `@00_Learning_Logs/daily/` 最新一篇日志
3. 粘贴下方 **「新对话启动提示词」**
4. 补充一行：**「今天是 Phase X / WY / Day Z，当前任务是：___」**

---

## 4. 新对话启动提示词（复制整段）

```markdown
你是我的 AI 学习教练，帮我按项目驱动方式完成 Agent 学习路线。

## 背景
- 身份：资深程序员 + 准研究生
- 目标：求职竞争力 + 科研能力（Agent / RAG / MCP / Skill / Coding Agent）
- 仓库：d:\AI_Projects\01_Research\Agent_System（已 push 到 GitHub）
- 计划：12 周完成完整路线图（见 3month_plan.md）
- 原则：内容不砍、验收不降；项目驱动；每天必须有可追踪产出

## 当前进度
- Phase：Phase 1 — AI 辅助开发工作流
- 周次：W1
- 实战代码库：02_DB_Demo_Studio（DB 课演示工具，PoC #1 进行中）
- 工作流工具包：01_AI_Dev_Workflow_Kit（prompts、workflow.md、可选审查脚本）
- 已完成：学习管理体系、需求/架构文档、Kit 审查脚本
- 待完成：Studio PoC #1、5 条使用记录、Phase1 验收

## 学习规范
1. 先读 @00_Roadmap/weekly_plan.md 和最新 daily log，再给今日任务
2. 带我「学概念 → 在 02_DB_Demo_Studio 实战 → 写 log → git commit」，不要只给理论
3. Prompt 用 01_AI_Dev_Workflow_Kit/prompts/；代码改动在 02_DB_Demo_Studio/
4. 不擅自 commit，我确认后再提交
5. 每天结束帮我更新 daily log 要点和 commit message 建议
6. 未达标不进入下一 Phase（验收见 3month_plan.md）

## 今天请从这里开始
请先确认我最新的 daily log 和 git 状态，然后给出今天 2-3 小时的执行清单（含具体文件路径和验收标准）。

我今天的任务是：【例如：Day2 — 用 architecture.md 细化 demo-schema，产出 02_DB_Demo_Studio/logs/ 记录】
```

---

## 5. 各 Phase 切换时的补充句

**Phase 1 → Phase 2（W2 开始）**
```text
当前：Phase 2 / W2 / Day 1，项目 06_RAG_Research_Assistant
今天任务：技术选型 + PDF 解析模块
```

**Phase 2 → Phase 3（W5 开始）**
```text
当前：Phase 3 / W5 / Day 1，项目 07_MCP_Server
今天任务：读 MCP 文档 + Server 脚手架
```

**Phase 3 → Phase 4（W7 开始）**
```text
当前：Phase 4 / W7 / Day 1，项目 08_Mini_Agent_Framework
今天任务：Agent Loop 设计 + core.py
```

---

## 6. 快捷版提示词（日常续学用）

```markdown
继续 Agent_System 学习。请先读 @00_Learning_Logs/daily/ 最新日志、@02_DB_Demo_Studio/README.md 和 @00_Roadmap/weekly_plan.md。

今天：Phase 【】/ W【】/ Day【】，任务：【】。
实战目录：02_DB_Demo_Studio/；模板：01_AI_Dev_Workflow_Kit/prompts/。
带我完成：学概念 → 实战 → 写 log → 建议 commit message。不要 commit 除非我要求。
```

---

## 7. 对话 vs 仓库的分工

```text
Cursor 新对话  = 短期记忆（3-5 天）
Git commit     = 长期记忆（永久可追溯）
Daily Log      = 每日快照（新对话必读）
02_DB_Demo_Studio/logs/ = Phase 1 实战记录（新对话建议 @）
Roadmap 文件   = 总导航（新对话 @ 引用）
```

**对话可以换，仓库和 log 不能断。**
