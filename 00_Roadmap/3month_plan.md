# 3 个月学习路线 — 完整加速版

> 目标：12 个月完整路线图的内容不减、验收不降，12 周内完成。  
> 时间：2026-05-27 → 2026-08-27（12 周，溢出缓冲至 09-07）  
> 强度：工作日 3-4h/天，周末 6-8h/天  
> 完整路线图：[`AI_Developer_Research_Roadmap.md`](../AI_Developer_Research_Roadmap.md)  
> 管理规范：[`AI_Learning_Management_Plan.md`](../AI_Learning_Management_Plan.md)  
> 项目矩阵：[`project_matrix.md`](project_matrix.md)

---

## 与 12 个月版的差异

| 12 个月版 | 3 个月版 | 做法 |
|---|---|---|
| 7 个 Phase 顺序推进 | 6 个 Phase 加速推进 | W1-W12 周周有产出 |
| 每周 10-15h | 每周 25-35h | 概念 + 项目同日并行 |
| 7 篇技术文章分散全年 | 3 篇（W4/W9/W12）**固定排期** | 其他标记「长期」|
| 每阶段结束才评估 | **周周有验收清单** | 防止积压 |
| 论文阅读穿插 | **每周固定 2h** 论文/文档阅读 | 排入周节奏 |
| 多 Phase 可溢出 | **每 Phase 预留 3-5 天缓冲** | 验收 < 3.5 分则顺延 |

---

## 总览

```text
W1        AI 工作流 + DB Demo Studio PoC
W2-W4     Paper RAG（完整：解析→检索→评估→文章）
W5-W6     MCP Server（6 tools 完成）
W7-W9     Agent 框架 + Coding Agent Demo
W10       Skill 系统 + Multi-Agent 入门
W11       Research Copilot v1
W12       Portfolio + 3 篇技术文章定稿
```

---

## Week 1 — AI 工作流 + DB Demo Studio PoC

**日期：** 2026-05-27 ~ 2026-06-01  
**对应 Phase 1：** AI 辅助开发工作流  
**主代码库：** `02_DB_Demo_Studio/` · `01_AI_Dev_Workflow_Kit/`

| 天 | 任务 | 交付 |
|---|---|---|
| D1 | 学习管理系统搭建 + 场景分析 + 首次 AI 实战 | 目录结构 + scenarios.md |
| D2 | 架构设计 Prompt 实战（ai-orchestrator 模块细化） | architecture.md 实战 + 使用记录 #2 |
| D3 | **PoC #1**：DemoPackage JSON Schema + 样例编码 | `packages/demo-schema/` |
| D4 | Debug / Player 骨架 | 步进播放 |
| D5 | 可选 `ai_commit_review.py` 审查 Studio diff | 审查报告 |
| D6 | workflow.md 定稿 + README 对齐 | Kit v1 |
| D7 | 周复盘 + Phase 1 自评 | `2026-W22.md` |

**阅读：** DB Demo Studio 架构、Phase 1 路线图目标  
**技术文章：** 不打草稿，仅收集素材  
**验收：** PoC #1 可演示 + 5 条使用记录 + 能 3 分钟讲清 AI 在 DB Demo Studio 开发中的作用

---

## Week 2 — LLM API + RAG v1（解析 + 入库）

**日期：** 2026-06-02 ~ 2026-06-08  
**对应 Phase 2：** LLM 应用基础与 RAG

### 学习内容

- LLM API 调用（Streaming、Structured Output）
- Embedding 模型选型
- 向量数据库（Chroma / Qdrant）
- 文档解析（PyMuPDF / pdfplumber）
- Chunk 策略基础

### 每日安排

| 天 | 任务 |
|---|---|
| D1 | 技术选型：Python + FastAPI + Chroma + DeepSeek，写 ADR 笔记 |
| D2 | PDF 解析模块：提取标题/摘要/章节/正文 |
| D3 | Chunk + Embedding 入库 |
| D4 | 基础问答 API |
| D5 | 概念卡片：RAG / Embedding / Chunking |
| D6 | 可选：Week 1 遗留 + 集成测试 |
| D7 | 周复盘 `2026-W23.md` |

**阅读：** RAG 论文、Chroma/Qdrant 文档  
**项目交付：** Paper RAG v1 — PDF 上传 + 问答可跑通  
**验收：** 能上传论文并回答问题（回答无需引用来源，v2 加）

---

## Week 3 — RAG v2（检索优化 + 引用）

**日期：** 2026-06-09 ~ 2026-06-15  
**对应 Phase 2 中段**

### 学习内容

- BM25 + Dense Retrieval + Hybrid Search
- Rerank
- HNSW 参数与索引优化
- 引用来源定位
- 多论文对比

| 天 | 任务 |
|---|---|
| D1 | BM25 + Hybrid Search 实现 |
| D2 | Reranker 集成 |
| D3 | 引用片段 + 来源定位功能 |
| D4 | 多论文对比（切换上下文） |
| D5 | HNSW 参数实验（efConstruction / M） |
| D6 | 可选：前端 Streamlit 初步对接 |
| D7 | 周复盘 `2026-W24.md` |

**阅读：** HNSW 论文、Rerank 相关文档  
**验收：** 回答给出准确来源 + 支持多篇论文切换 + 1 次 HNSW 实验记录

---

## Week 4 — RAG v3（评估 + 文章）

**日期：** 2026-06-16 ~ 2026-06-22  
**对应 Phase 2 收尾**

### 学习内容

- RAG Evaluation（RAGAS / 人工评估集）
- 3 种 chunk 策略对比实验
- RAG 系统的常见失败模式

| 天 | 任务 |
|---|---|
| D1 | 构建评估集（10 个问题 + 标准答案） |
| D2 | 3 种 chunk 策略对比（fixed / recursive / semantic） |
| D3 | RAGAS 评估 + 结果分析 |
| D4 | Streamlit / 前端 Demo 完善 |
| D5 | 写 Phase 2 文章草稿：《RAG 系统的检索、重排与评估》 |
| D6 | README + 项目整理 |
| D7 | 月复盘 `2026-06.md` + Phase 2 自评 |

**阅读：** RAGAS 论文、GraphRAG 简介  
**技术文章 #1：** 《RAG 系统的检索、重排与评估》（W4 定稿）  
**项目交付：** Paper RAG Assistant v2 — 可展示、有评估

---

## Week 5 — Tool Use + MCP v1

**日期：** 2026-06-23 ~ 2026-06-29  
**对应 Phase 3：** Tool Use 与 MCP

### 学习内容

- Function Calling / Tool Calling
- JSON Schema 设计
- Tool Router + Error Recovery
- MCP 协议基础（Server/Client/Tool/Resource/Prompt）

| 天 | 任务 |
|---|---|
| D1 | Function Calling 入门 + JSON Schema 设计练习 |
| D2 | MCP 官方文档通读 + 概念笔记 |
| D3 | Python MCP Server 脚手架：可连接 |
| D4 | 实现工具：`search_files` + `read_file` |
| D5 | 实现工具：`save_note` |
| D6 | 概念卡片：MCP / Tool Use / Function Calling |
| D7 | 周复盘 `2026-W26.md` |

**阅读：** MCP 官方文档、Function Calling 相关  
**验收：** MCP Server 可连接 + 3 个工具可用

---

## Week 6 — MCP v2（完整 6 tools）

**日期：** 2026-06-30 ~ 2026-07-06  
**对应 Phase 3 收尾**

### 学习内容

- 工具权限与安全边界
- 工具描述对模型选择的影响
- MCP vs 普通 HTTP API Tool Calling 差异

| 天 | 任务 |
|---|---|
| D1 | 实现工具：`run_tests` |
| D2 | 实现工具：`query_papers`（接 Paper RAG） |
| D3 | 实现工具：`git_diff_summary` |
| D4 | 工具权限 + 安全说明 + 错误处理完善 |
| D5 | MCP 工具设计规范文档 |
| D6 | 工具描述实验（不同描述如何影响模型选工具） |
| D7 | 周复盘 `2026-W27.md` + Phase 3 自评 |

**阅读：** 工具调用相关论文、MCP 最佳实践  
**技术文章：** 收集素材  
**验收：** 6 个工具完整 + 规范文档 + 能解释 MCP 差异

---

## Week 7 — Mini Agent Framework（核心 Loop）

**日期：** 2026-07-07 ~ 2026-07-13  
**对应 Phase 4 上段：** Agent 核心工程

### 学习内容

- ReAct 论文精读
- Agent 基本循环：Observe → Think → Plan → Act → Reflect
- Agent State / Trace
- LangGraph 学习（状态机式 Agent）

| 天 | 任务 |
|---|---|
| D1 | 读 ReAct 论文 + 概念笔记 |
| D2 | Agent Loop 核心实现：`core.py`（Observe → Think → Act） |
| D3 | Tool Registry + Tool Calling 集成 |
| D4 | Planner（Plan-and-Execute 模式） |
| D5 | Executor + State 管理 |
| D6 | Trace 记录模块 |
| D7 | 周复盘 `2026-W28.md` |

**阅读：** ReAct 论文、LangGraph 官方文档  
**验收：** Agent Loop 可运行 + 能调用工具 + Trace 记录完整

---

## Week 8 — Agent 框架完善 + 框架对比

**日期：** 2026-07-14 ~ 2026-07-20  
**对应 Phase 4 中段**

### 学习内容

- Critic / Reflection 模块
- 错误恢复与重试
- Memory 接口（lite：向量检索历史）
- OpenAI Agents SDK
- AutoGen / CrewAI 了解

| 天 | 任务 |
|---|---|
| D1 | Critic 模块（LLM-as-Judge 自我评估） |
| D2 | 失败重试 + 调整计划机制 |
| D3 | Memory 接口（检索历史任务，lite 版） |
| D4 | OpenAI Agents SDK 对比实验 |
| D5 | LangGraph / AutoGen / 自研框架对比笔记 |
| D6 | 集成测试：Agent 完成多步骤任务 |
| D7 | 周复盘 `2026-W29.md` |

**阅读：** Reflexion 论文、OpenAI Agents SDK 文档  
**验收：** 自研 Agent 可完成多步骤任务 + 失败恢复 + 框架对比清晰

---

## Week 9 — Coding Agent Demo

**日期：** 2026-07-21 ~ 2026-07-27  
**对应 Phase 4 下段：** Coding Agent

### 学习内容

- OpenHands / SWE-agent 架构研究
- Repo Map：文件树 + 符号索引
- Code Edit + Test Run + 错误分析

| 天 | 任务 |
|---|---|
| D1 | 读 OpenHands / SWE-agent 源码笔记 |
| D2 | Repo Map 模块实现 |
| D3 | Coding Agent 核心：读 issue → 搜代码 → 计划 |
| D4 | Coding Agent 核心：改文件 → 跑测试 |
| D5 | 失败自动分析 + 重试闭环 |
| D6 | 端到端 Demo：1 个真实仓库任务 |
| D7 | 周复盘 `2026-W30.md` + Phase 4 自评 |

**阅读：** SWE-bench 论文、OpenHands 源码  
**技术文章 #2：** 《从零实现一个 Agent 框架》（W9 定稿）  
**验收：** Coding Agent 完成 1 个真实仓库任务 + 完整轨迹

---

## Week 10 — Skill 系统 + Multi-Agent 入门

**日期：** 2026-07-28 ~ 2026-08-03  
**对应 Phase 5：** Agent Memory 与 Skill

### 学习内容

- Skill 文件结构、触发机制、版本管理、质量评估
- Agent Memory 类型：Working/Short-term/Long-term/Episodic/Semantic/Procedural
- Multi-Agent 概念入门（Supervisor、Debate）

| 天 | 任务 |
|---|---|
| D1 | Skill 格式设计 + SKILL.md 模板 |
| D2 | Skill Manager：注册 + 检索 + 触发 |
| D3 | 从 W1-W9 任务复盘中提取 5 个 Skill（Debug / Code Review / RAG / MCP / Agent 测试） |
| D4 | Memory 模块完善：短期 + 长期记忆接口 |
| D5 | 有无 Memory/Skill 的对比实验 |
| D6 | Multi-Agent 概念入门：Supervisor + Specialist 模式 |
| D7 | 周复盘 `2026-W31.md` + Phase 5 自评 |

**阅读：** Voyager 论文、Generative Agents 论文、Multi-Agent 相关  
**验收：** 5-8 个 Skill 沉淀 + 对比实验 + 概念卡片完整

---

## Week 11 — Research Copilot v1

**日期：** 2026-08-04 ~ 2026-08-10  
**对应 Phase 6：** 科研增强系统

### 学习内容

- 文献检索自动化
- 论文结构化卡片
- Related Work 生成
- 实验计划管理

| 天 | 任务 |
|---|---|
| D1 | 需求设计：Research Copilot 功能清单（P0/P1） |
| D2 | 论文卡片系统：上传 → 解析 → 结构化存储 |
| D3 | Related Work 草稿生成（接 Paper RAG + 自研 Agent） |
| D4 | 实验计划管理器（实验模板 + 进度追踪） |
| D5 | 研究周报生成器 |
| D6 | 端到端测试：输入研究方向 → 输出论文卡片 + RW 草稿 |
| D7 | 周复盘 `2026-W32.md` + Phase 6 自评 |

**阅读：** 你的目标领域的论文 5-10 篇  
**验收：** 管理 15+ 篇论文 + 自动生成卡片 + RW 草稿可读

---

## Week 12 — Portfolio + 技术文章定稿

**日期：** 2026-08-11 ~ 2026-08-27（可溢出至 09-07）  
**对应 Phase 7：** 作品集与求职包装

### 学习内容

- README 写作规范
- Demo 录制与展示
- 简历提炼、面试故事、技术文章

| 天 | 任务 |
|---|---|
| D1-D2 | 6 个项目 README 统一对齐（架构图 + 评估结果 + 快速开始） |
| D3 | 技术文章 #3 定稿：《我是如何把 AI 接入日常开发流程的》（或另一篇） |
| D4 | 简历条目提炼（4-6 条）+ 面试故事（3-5 个） |
| D5 | Demo 录制 / 截图整理 / `demo_index.md` |
| D6 | 月复盘 `2026-08.md` + 3 个月总复盘 |
| D7 | GitHub pin 项目 + tag v1.0-portfolio |

**技术文章 #3：** 《从 RAG 到 Agent：我的 3 个月 AI 工程学习之路》（W12 定稿）  
**文章候选清单（全年目标 7 篇，3 个月内至少 3 篇）：**  
- [ ] W4：《RAG 系统的检索、重排与评估》
- [ ] W9：《从零实现一个 Agent 框架》
- [ ] W12：《从 RAG 到 Agent：我的 3 个月 AI 工程学习之路》
- [ ] 长期：《MCP 是什么：为什么它会成为 Agent 工具协议》
- [ ] 长期：《Agent Memory 与 Skill 系统设计》
- [ ] 长期：《Coding Agent 如何理解代码仓库》
- [ ] 长期：《AI 如何增强研究生科研工作流》

**验收：** 6 个项目都有 README + Demo + 简历 4 条 + 面试故事 3 个 + 3 篇文章定稿

---

## 每周固定节奏

| 时段 | 时长 | 内容 |
|---|---|---|
| 上午 | 1-1.5h | 读文档/论文/官方教程 → 写概念笔记 `00_Notes/concepts/` |
| 下午 | 2-2.5h | 项目编码 → 至少 1 个可见产出 |
| 晚上 | 0.5-1h | Daily Log + 预习明天 |

**每天最低产出：** 1 条笔记 OR 1 次代码提交 OR 1 条实验记录  
**每周阅读：** 固定 2h 论文/文档（排入周末）  
**每周复盘：** 周日写 `00_Learning_Logs/weekly/2026-WXX.md`  
**每月复盘：** 最后一天写 `00_Learning_Logs/monthly/2026-0X.md` + 自评打分

---

## Phase 验收清单（保持不变）

### Phase 1 验收（W1 末）
- [ ] DB Demo Studio PoC #1 可演示（DemoPackage + Player）
- [ ] 5 条真实 AI 使用记录
- [ ] 5 个 Prompt 模板 + workflow 文档
- [ ] 可选：`ai_commit_review.py` 可运行
- [ ] 能 3 分钟讲清 AI 在 DB Demo Studio 中的作用

### Phase 2 验收（W4 末）
- [ ] 上传论文可问答，回答带来源片段
- [ ] 对比 3 种 chunk 策略
- [ ] 至少 1 次 HNSW 或 rerank 实验
- [ ] RAG 评估报告

### Phase 3 验收（W6 末）
- [ ] MCP Server 可被客户端连接
- [ ] 至少 5 个 tool（含 schema、测试、安全说明）
- [ ] 能解释 MCP vs 普通 API Tool Calling

### Phase 4 验收（W9 末）
- [ ] 自研 Agent 完成多步骤任务
- [ ] 完整执行轨迹 Trace
- [ ] 失败后可重试/调整计划
- [ ] 能说明 LangGraph vs 自研框架差异
- [ ] Coding Agent 处理 1 个真实仓库任务

### Phase 5 验收（W10 末）
- [ ] Agent 保存并检索任务经验
- [ ] 至少 5 个 Skill
- [ ] 有无 Memory/Skill 的对比实验

### Phase 6 验收（W11 末）
- [ ] 管理 15+ 篇论文
- [ ] 自动生成论文卡片
- [ ] Related Work 初稿

### Phase 7（贯穿 W1-W12，W12 集中整理）
- [ ] 6 个项目 README 完整
- [ ] 每个项目有 Demo/截图/评估
- [ ] 简历 4-6 条 + 面试故事 3-5 个
- [ ] 技术文章 >= 3 篇

---

## 能力自评时间表

| 时间 | 自评重点 |
|---|---|
| W4 末 | RAG 能讲清楚 + 有评估数据 |
| W6 末 | MCP 能演示 + 能讲协议差异 |
| W9 末 | Agent 能画架构图 + Coding Agent 可跑 |
| W12 末 | 完整作品集 + 3 分钟讲任意项目 |

每阶段末用 `AI_Learning_Management_Plan.md` §7 评分表自评：平均分 < 3.5 则该阶段溢出 3-5 天补短板。

---

## 溢出策略

如果某阶段验收不通过：

| 情况 | 措施 |
|---|---|
| Phase 1 未过 | W2 前补完，RAG 压缩 1 周 |
| Phase 2 未过 | W5 前补 3 天，MCP 顺延 |
| Phase 3 未过 | W7 前补 3 天，Agent 顺延 |
| Phase 4 未过 | 优先补 Agent，Skill/Multi-Agent 减为概念了解 |
| Phase 5 未过 | 合并进 W12，Skill 数量降到 3 个 |
| Phase 6 未过 | W12 溢出到 09-07 |

**最大溢出期限：** 2026-09-07（12 周 + 2 周缓冲）

---

## 当前位置

**Today = 2026-06-01 = W1 Day 3 — PoC #1 编码中**

见 [`day3_2026-06-01_guide.md`](day3_2026-06-01_guide.md)
