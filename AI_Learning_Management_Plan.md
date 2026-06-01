# AI 学习管理方案

> 目标：把 AI 学习过程项目化、可追踪、可复盘、可展示。  
> 适用路线：LLM 应用、RAG、Tool Use、MCP、Agent、Memory、Skill、Coding Agent、Research Agent。  
> 核心原则：每一阶段都必须有学习记录、项目产出、实验结果、复盘总结。

---

## 1. 管理目标

这份方案用于管理你的完整 AI 学习历程，避免出现下面几类问题：

- 学了很多资料，但没有沉淀。
- 做了很多 Demo，但没有形成项目资产。
- 会用工具，但讲不清底层机制。
- 项目能跑，但没有评估、文档和复盘。
- 学习过程分散，后续无法整理成简历、博客、论文或面试材料。

最终你要形成四类资产：

1. **学习记录资产**
   - 每日学习日志
   - 每周复盘
   - 论文笔记
   - 技术概念卡片

2. **项目资产**
   - 可运行代码
   - README
   - 架构图
   - Demo 截图或视频
   - 测试与评估结果

3. **研究资产**
   - 实验设计
   - 对比结果
   - 失败案例分析
   - 技术报告

4. **求职资产**
   - 项目介绍
   - 简历条目
   - 面试讲述稿
   - 技术博客

---

## 2. 推荐目录结构

建议在当前仓库中使用下面结构管理学习过程：

```text
Agent_System/
  AI_Developer_Research_Roadmap.md
  AI_Learning_Management_Plan.md

  00_Roadmap/
    weekly_plan.md
    monthly_review.md
    reading_list.md
    project_matrix.md

  00_Learning_Logs/
    daily/
      2026-05-27.md
    weekly/
      2026-W22.md
    monthly/
      2026-05.md

  00_Notes/
    concepts/
    papers/
    frameworks/
    experiments/

  00_Portfolio/
    resume_items.md
    interview_stories.md
    blog_ideas.md
    demo_index.md

  01_LangGraph_Basics/
  02_Tool_Use_Agent/
  03_Agent_Memory_System/
  04_Multi_Agent_Team/
  05_Self_Improving_Agent/
  06_RAG_Research_Assistant/
  07_MCP_Server/
  08_Mini_Agent_Framework/
  09_Coding_Agent/
  10_AI_Research_Copilot/
```

---

## 3. 总体学习节奏

## 3.1 每日节奏

每天至少完成一项可记录动作：

| 类型 | 内容 | 最小产出 |
|---|---|---|
| 学概念 | 阅读文档、论文、源码、教程 | 1 条概念笔记 |
| 写代码 | 完成项目中的一个小功能 | 1 次 commit 或代码片段 |
| 做实验 | 对比参数、模型、框架、方案 | 1 条实验记录 |
| 写总结 | 复盘问题、踩坑、设计取舍 | 1 段学习日志 |

每日记录不要追求长，重点是连续。

## 3.2 每周节奏

每周固定产出：

| 周产出 | 要求 |
|---|---|
| 周学习总结 | 本周学了什么、解决了什么、卡在哪里 |
| 项目进度 | 至少完成一个明确功能 |
| 技术笔记 | 至少整理一个核心概念 |
| 实验记录 | 至少做一次可复现对比 |
| 下周计划 | 只列 3-5 个重点任务 |

## 3.3 每月节奏

每月固定产出：

| 月产出 | 要求 |
|---|---|
| 月度复盘 | 阶段目标是否完成 |
| 项目 Demo | 至少一个可展示版本 |
| 技术文章草稿 | 至少一篇 |
| 简历素材 | 提炼 1-2 条项目经历 |
| 研究问题 | 形成 1 个可继续探索的问题 |

---

## 4. 阶段学习管理

## Phase 1：AI 辅助开发工作流

**周期：2-4 周**

### 学习内容

- AI 编程工具使用：
  - Codex
  - Cursor
  - Claude Code
  - Aider
- AI 辅助开发任务：
  - 需求澄清
  - 架构设计
  - 代码生成
  - 测试生成
  - Debug
  - 重构
  - Code Review
- Git + AI 工作流：
  - 基于 diff 做审查
  - 基于 issue 生成计划
  - 基于测试失败定位问题

### 学习历程记录

每次使用 AI 辅助开发时记录：

```markdown
## 日期

## 任务

## 我自己原本会怎么做

## AI 帮我做了什么

## 哪些地方有效

## 哪些地方无效

## 我如何修正 AI 输出

## 可复用经验
```

### 阶段成果

- `AI Dev Workflow Kit`
- 个人 AI 编程提示词模板
- Code Review 模板
- Debug 模板
- 一篇总结：《我的 AI 辅助开发工作流》

### 阶段验收标准

- 能用 AI 完成一个真实小功能的开发闭环。
- 能讲清楚 AI 在需求、设计、编码、测试、审查中的作用。
- 有至少 5 条真实使用记录。

---

## Phase 2：LLM 应用基础与 RAG

**周期：4-6 周**

### 学习内容

- LLM API 调用
- Streaming 输出
- Structured Output
- Embedding
- 向量数据库
- Chunking
- BM25
- Hybrid Search
- HNSW
- Rerank
- RAG Evaluation

### 学习历程记录

每学一个概念，按下面格式记录：

```markdown
## 概念

## 它解决什么问题

## 核心原理

## 工程实现方式

## 常见坑

## 我在项目中如何使用

## 参考资料
```

每做一次 RAG 实验，按下面格式记录：

```markdown
## 实验名称

## 实验目的

## 数据集

## 参数设置

## 对比方案

## 结果

## 结论

## 下一步
```

### 阶段成果

- `Paper RAG Assistant`
- PDF 解析模块
- 向量检索模块
- 问答模块
- 引用来源定位
- RAG 实验报告

### 阶段验收标准

- 能上传论文并问答。
- 回答能给出来源片段。
- 至少对比 3 种 chunk 策略。
- 至少记录 1 次 HNSW 或 rerank 实验。

---

## Phase 3：Tool Use 与 MCP

**周期：4-6 周**

### 学习内容

- Function Calling
- Tool Schema 设计
- Tool Router
- Tool Error Recovery
- MCP Server
- MCP Client
- MCP Tool
- MCP Resource
- MCP Prompt
- 工具权限与安全边界

### 学习历程记录

每开发一个工具，记录：

```markdown
## 工具名称

## 工具用途

## 输入 Schema

## 输出 Schema

## 权限风险

## 错误处理

## Agent 何时应该调用它

## 测试样例
```

### 阶段成果

- `Personal MCP Server`
- 文件搜索工具
- 文件读取工具
- Git diff 总结工具
- 测试运行工具
- 科研笔记保存工具
- MCP 工具设计规范

### 阶段验收标准

- MCP Server 能被客户端连接。
- 至少实现 5 个工具。
- 每个工具都有 schema、测试和安全说明。
- 能解释 MCP 和普通 API 工具调用的区别。

---

## Phase 4：Agent 核心工程

**周期：6-8 周**

### 学习内容

- ReAct
- Plan-and-Execute
- Reflection
- Critic
- Agent State
- Agent Trace
- LangGraph
- OpenAI Agents SDK
- AutoGen
- CrewAI
- OpenHands
- SWE-agent

### 学习历程记录

每实现一个 Agent 能力，记录：

```markdown
## 能力名称

## 它在 Agent 中的位置

## 输入

## 输出

## 状态变化

## 失败模式

## 测试任务

## 改进想法
```

### 阶段成果

- `Mini Agent Framework`
- Agent 主循环
- Planner
- Executor
- Tool Registry
- Memory 接口
- Trace 记录
- Critic 模块
- Coding Agent Demo

### 阶段验收标准

- 能用自研 Agent 完成一个多步骤任务。
- 能记录完整执行轨迹。
- 能在失败后重试或调整计划。
- 能说明 LangGraph 和自研框架的设计差异。

---

## Phase 5：Agent Memory 与 Skill

**周期：4-6 周**

### 学习内容

- Working Memory
- Long-term Memory
- Episodic Memory
- Semantic Memory
- Procedural Memory
- Skill 文件结构
- Skill 触发机制
- Skill 版本管理
- Skill 质量评估

### 学习历程记录

每沉淀一个 Skill，记录：

```markdown
## Skill 名称

## 适用任务

## 触发条件

## 执行步骤

## 依赖工具

## 成功案例

## 失败案例

## 版本更新记录
```

每记录一条 Memory，记录：

```markdown
## Memory 类型

## 内容

## 来源任务

## 可复用场景

## 过期条件

## 是否验证有效
```

### 阶段成果

- `Agent Memory System`
- `Self-Improving Skill Agent`
- Skill 管理器
- Memory 检索器
- 任务复盘提取 Skill 的流程
- Memory + Skill 实验报告

### 阶段验收标准

- Agent 能保存任务经验。
- Agent 能在新任务中检索历史经验。
- 至少沉淀 10 个 Skill。
- 至少做一次有无 Memory/Skill 的对比实验。

---

## Phase 6：科研增强系统

**周期：6-8 周**

### 学习内容

- 文献检索
- 论文结构化阅读
- Citation Graph
- Related Work 生成
- 实验计划管理
- 代码复现辅助
- 数据分析辅助
- 科研写作辅助

### 学习历程记录

每读一篇论文，记录：

```markdown
## 论文标题

## 研究问题

## 核心方法

## 实验设置

## 主要结论

## 局限性

## 和我方向的关系

## 可复现点

## 可改进点
```

每形成一个研究问题，记录：

```markdown
## 研究问题

## 背景

## 为什么重要

## 现有方法不足

## 我的假设

## 实验设计

## 需要的数据

## 预期贡献
```

### 阶段成果

- `AI Research Copilot`
- 论文卡片系统
- Related Work 草稿生成器
- 实验计划管理器
- 研究周报生成器
- 一个可继续深入的研究题目

### 阶段验收标准

- 能管理至少 20 篇论文。
- 能自动生成结构化论文卡片。
- 能生成一个方向的 Related Work 初稿。
- 能提出 3 个可实验研究问题。

---

## Phase 7：作品集与求职科研包装

**周期：持续进行**

### 学习内容

- 项目 README 写作
- Demo 展示
- 技术博客写作
- 简历项目描述
- 面试讲述
- 科研计划书

### 学习历程记录

每个项目完成后记录：

```markdown
## 项目名称

## 项目解决的问题

## 技术架构

## 我的核心贡献

## 难点

## 失败与优化

## 评估结果

## 可以如何继续扩展

## 简历描述

## 面试讲述版本
```

### 阶段成果

- GitHub 项目矩阵
- Portfolio 首页
- 简历项目经历
- 3-5 篇技术文章
- 1 个研究计划
- 面试问答库

### 阶段验收标准

- 每个项目都有 README。
- 每个项目都有截图、Demo 或运行说明。
- 每个项目都有设计取舍和评估结果。
- 能用 3 分钟讲清楚任意一个项目。

---

## 5. 文件模板

## 5.1 每日学习日志模板

文件位置：

```text
00_Learning_Logs/daily/YYYY-MM-DD.md
```

模板：

```markdown
# Daily Log - YYYY-MM-DD

## 今日目标

- 

## 学习内容

- 

## 项目进展

- 

## 遇到的问题

- 

## 解决方式

- 

## 今日产出

- 

## 可复用经验

- 

## 明日计划

- 
```

## 5.2 每周复盘模板

文件位置：

```text
00_Learning_Logs/weekly/YYYY-WXX.md
```

模板：

```markdown
# Weekly Review - YYYY-WXX

## 本周目标

- 

## 完成情况

- 

## 关键学习

- 

## 项目进展

- 

## 实验记录

- 

## 问题与阻塞

- 

## 下周计划

- 

## 本周产出链接

- 
```

## 5.3 概念笔记模板

文件位置：

```text
00_Notes/concepts/topic.md
```

模板：

```markdown
# Concept: 名称

## 一句话解释

## 解决的问题

## 核心机制

## 工程实现

## 典型应用

## 常见失败模式

## 和其他概念的关系

## 我自己的理解

## 参考资料
```

## 5.4 论文笔记模板

文件位置：

```text
00_Notes/papers/paper-title.md
```

模板：

```markdown
# Paper: 标题

## 基本信息

- Title:
- Authors:
- Year:
- Link:
- Tags:

## 研究问题

## 方法

## 实验

## 结果

## 创新点

## 局限性

## 对我的启发

## 可复现计划

## 可改进方向
```

## 5.5 实验记录模板

文件位置：

```text
00_Notes/experiments/experiment-name.md
```

模板：

```markdown
# Experiment: 名称

## 背景

## 假设

## 实验设置

## 数据

## 方法 A

## 方法 B

## 指标

## 结果

## 分析

## 结论

## 后续实验
```

## 5.6 项目 README 模板

每个项目目录都应该有：

```markdown
# Project Name

## 1. 项目目标

## 2. 核心功能

## 3. 技术架构

## 4. 快速开始

## 5. 使用示例

## 6. 关键设计

## 7. 实验与评估

## 8. 已知问题

## 9. 后续计划

## 10. 学习记录
```

---

## 6. 阶段看板

建议维护文件：

```text
00_Roadmap/project_matrix.md
```

内容格式：

```markdown
# Project Matrix

| 项目 | 阶段 | 状态 | 当前任务 | 下一个里程碑 | 产出物 |
|---|---|---|---|---|---|
| AI Dev Workflow Kit | Phase 1 | Not Started | 设计模板 | 完成第一版 prompts | README + 模板 |
| Paper RAG Assistant | Phase 2 | Not Started | 技术选型 | PDF 解析 | Demo |
| Personal MCP Server | Phase 3 | Not Started | 学 MCP | 实现第一个 tool | MCP Server |
| Mini Agent Framework | Phase 4 | Not Started | 设计架构 | Agent Loop | 框架代码 |
| Skill Memory Agent | Phase 5 | Not Started | Skill 格式 | Skill 检索 | 实验报告 |
| AI Research Copilot | Phase 6 | Not Started | 需求设计 | 论文卡片 | Research Demo |
```

状态建议使用：

- `Not Started`
- `Learning`
- `Building`
- `Testing`
- `Writing`
- `Done`
- `Paused`

---

## 7. 学习成果评分表

每个阶段结束后，用 1-5 分自评：

| 维度 | 评分 | 说明 |
|---|---:|---|
| 理论理解 |  | 是否能讲清楚原理 |
| 工程实现 |  | 是否能独立实现 |
| 项目完整度 |  | 是否能运行、可展示 |
| 实验评估 |  | 是否有对比和指标 |
| 文档质量 |  | README、笔记是否清楚 |
| 面试表达 |  | 是否能 3 分钟讲清楚 |
| 创新潜力 |  | 是否能形成研究问题 |

阶段通过标准：

- 平均分 >= 3.5：可以进入下一阶段。
- 平均分 < 3.5：先补齐短板。
- 工程实现或项目完整度低于 3：不建议进入下一阶段。

---

## 8. 每阶段必须回答的问题

每个阶段结束后，必须写一段复盘，回答下面问题：

1. 这个阶段的核心问题是什么？
2. 这个技术解决了什么实际需求？
3. 它的底层机制是什么？
4. 工程实现中最容易失败的地方是什么？
5. 我做了什么项目来验证它？
6. 我的项目和普通 Demo 有什么区别？
7. 我做了什么评估？
8. 如果面试官问我这个方向，我怎么讲？
9. 如果做科研，这个方向还有什么问题值得研究？
10. 下一阶段应该如何衔接？

---

## 9. 第一阶段启动计划（已归档）

> 以下 Week 1-4 为原始模板，实际执行请参照 [`00_Roadmap/3month_plan.md`](00_Roadmap/3month_plan.md) 的 W1-W12 加速路线。

## Week 1：建立 AI 学习管理系统

### 学习目标

- 建立记录体系。
- 明确 AI 辅助开发工作流。
- 开始收集自己的提示词和实践记录。

### 任务清单

- 创建 `00_Roadmap`
- 创建 `00_Learning_Logs`
- 创建 `00_Notes`
- 创建 `00_Portfolio`
- 创建 `weekly_plan.md`
- 创建第一篇每日学习日志
- 整理 5 个 AI 编程常用场景
- 写第一版 AI 开发工作流

### 产出

- 学习管理目录
- 第一周计划
- 第一篇 Daily Log
- AI 编程工作流草稿

## Week 2：AI 辅助编码闭环

### 学习目标

- 用 AI 完成一个小功能从需求到测试的闭环。

### 任务清单

- 选择一个小项目或仓库功能。
- 用 AI 辅助写需求说明。
- 用 AI 辅助做设计。
- 用 AI 辅助编码。
- 用 AI 生成测试。
- 用 AI 做 Code Review。
- 记录完整过程。

### 产出

- 一个完整功能 commit。
- 一份 AI 辅助开发过程记录。
- 一份 Code Review 模板。

## Week 3：AI 辅助调试与重构

### 学习目标

- 掌握 AI 在 Debug 和 Refactor 中的高质量使用方式。

### 任务清单

- 找一个真实 Bug 或构造一个失败测试。
- 让 AI 分析错误日志。
- 对比 AI 方案和自己方案。
- 完成一次重构。
- 总结 AI 调试流程。

### 产出

- Debug 记录。
- Refactor 记录。
- Debug Prompt 模板。

## Week 4：阶段总结与作品化

### 学习目标

- 把第一阶段整理成可展示资产。

### 任务清单

- 整理所有 prompt 模板。
- 整理 AI Dev Workflow Kit。
- 写 README。
- 写阶段复盘。
- 提炼简历项目描述。

### 产出

- `AI Dev Workflow Kit`
- 阶段复盘
- 简历条目
- 技术文章草稿

---

## 10. 每天怎么开始

每天学习前先打开当天日志，写下：

```markdown
## 今日目标

- 今天只完成 1-3 件事。
```

每天结束前补充：

```markdown
## 今日产出

- 文件、代码、笔记、实验或文章链接。

## 明日计划

- 下一步最小动作。
```

不要让学习停留在“我看了资料”。每天必须留下一个可以被追踪的产出。

---

## 11. 每周怎么复盘

每周结束时问自己：

- 我这周是否完成了一个可见产出？
- 哪个概念我能讲清楚了？
- 哪个概念我还只是会用，不理解？
- 项目有没有变得更完整？
- 有没有记录失败案例？
- 下周最重要的一件事是什么？

复盘不是写流水账，而是提炼：

- 可复用方法
- 技术判断
- 失败原因
- 下一步策略

---

## 12. 如何把学习转成竞争力

每个阶段都要把成果转成下面三种表达：

## 12.1 简历表达

格式：

```text
基于 XXX 技术构建 XXX 系统，实现 XXX 功能，通过 XXX 指标评估，优化 XXX，提升 XXX。
```

示例：

```text
基于 RAG 和向量数据库构建论文问答助手，实现 PDF 解析、语义检索、引用定位和多论文对比，并通过 chunk size、rerank 策略对比实验优化问答准确性。
```

## 12.2 面试表达

每个项目准备 3 分钟版本：

```text
这个项目解决什么问题？
为什么普通方案不够？
我怎么设计系统？
关键难点是什么？
我怎么验证效果？
如果继续做，我会怎么扩展？
```

## 12.3 科研表达

每个项目尝试提炼研究问题：

```text
现有方法的问题是什么？
我的观察是什么？
是否可以做实验验证？
是否有可量化指标？
是否能形成小论文、报告或毕业设计方向？
```

---

## 13. 建议立即执行

下一步建议直接做下面 5 件事：

1. 创建学习管理目录。
2. 创建今天的 Daily Log。
3. 创建本周 Weekly Plan。
4. 创建 `project_matrix.md`。
5. 开始 Phase 1：AI 辅助开发工作流。

第一天不要急着写复杂代码，先把记录系统搭起来。之后所有学习、实验和项目都进入这个系统。

