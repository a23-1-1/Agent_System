# AI 开发能力与科研能力提升路线图

> 适用对象：资深程序员、准研究生，希望用 LLM/Agent 技术提升求职竞争力、科研效率和工程创新能力。  
> 学习方式：项目驱动 + 工程复现 + 论文阅读 + 自研组件沉淀。  
> 时间跨度：6-12 个月，可持续迭代。

---

## 0. 总目标

你不应该只把 AI 当成“更强的搜索引擎”或“代码补全工具”，而应该把它当成一个新的软件工程平台来学习。

最终目标是形成三类核心竞争力：

1. **AI Native 开发能力**
   - 能熟练使用 LLM 辅助需求分析、架构设计、编码、测试、重构、文档和调试。
   - 能把 AI 工具集成进自己的开发工作流，而不是零散聊天式使用。

2. **Agent 工程能力**
   - 能独立设计、实现、评估和部署 Agent 系统。
   - 不只会用 LangGraph、AutoGen、CrewAI、OpenHands、OpenAI Agents SDK 等框架，还能理解底层架构。

3. **科研增强能力**
   - 能用 LLM 构建论文阅读、文献综述、实验设计、代码复现、数据分析和写作辅助系统。
   - 能围绕 Agent、RAG、MCP、Tool Use、Memory、Multi-Agent、Evaluation 等方向形成可发表或可展示的研究型项目。

---

## 1. 技术地图

### 1.1 必须掌握的核心方向

| 方向 | 你要达到的水平 | 代表技术/关键词 |
|---|---|---|
| LLM 基础 | 理解模型能力边界、上下文、推理、幻觉、对齐、工具调用 | Transformer、Instruction Tuning、RLHF、DPO、Reasoning Model |
| Prompt Engineering | 从“写提示词”升级到“设计任务协议” | System Prompt、Few-shot、CoT、Structured Output、Prompt Evaluation |
| RAG | 能构建可靠知识库问答与科研助手 | Embedding、Chunking、Rerank、Hybrid Search、HNSW、GraphRAG |
| Tool Use | 能让模型稳定调用真实工具 | Function Calling、JSON Schema、Tool Router、Error Recovery |
| Agent | 能构建可规划、可执行、可反思的任务系统 | ReAct、Plan-and-Execute、Reflection、Workflow Agent |
| MCP | 能为 Agent 构建标准化上下文与工具接口 | Model Context Protocol、MCP Server、MCP Client、Resource、Tool |
| Skill | 能把重复能力沉淀成可复用技能模块 | Codex Skill、Claude Skill、Task Skill、Workflow Skill |
| Multi-Agent | 能设计角色分工、协作和冲突解决机制 | Supervisor、Swarm、Debate、Critic、Specialist Agents |
| Agent Memory | 能设计短期、长期、情景和用户记忆 | Vector Memory、Episodic Memory、Semantic Memory、Reflection Memory |
| Agent Evaluation | 能评估 Agent 是否真的可靠 | Task Success Rate、Trajectory Eval、LLM-as-Judge、Human Eval |
| Coding Agent | 能构建或改造软件工程 Agent | OpenHands、SWE-agent、Aider、Codex、Cursor、Repo Map |
| Research Agent | 能构建科研工作流自动化系统 | Paper QA、Literature Review、Experiment Agent、Benchmark Agent |

### 1.2 你提到的关键词定位

| 关键词 | 建议理解方式 |
|---|---|
| Agent | LLM 从“回答器”变成“任务执行系统”的核心形态 |
| MCP | Agent 连接外部工具、文件、数据库、浏览器、代码仓库的标准协议之一 |
| Skill | 把经验、流程、工具调用封装成可复用能力单元 |
| OpenHands | 面向软件工程任务的开源 Coding Agent，可研究其规划、文件编辑、执行和反馈机制 |
| HNSW | 向量数据库中常见近似最近邻索引，是 RAG 检索性能的重要基础 |
| OpenCL / CUDA / 推理加速 | 如果你说的 “openclow” 指底层计算方向，可作为模型部署与推理优化扩展线 |
| Hermes / function-calling models | 如果你说的 “herns” 指模型或工具调用相关项目，可归入开源模型与 Agent Tool Use 方向 |

---

## 2. 分阶段路线

## Phase 1：AI 辅助开发工作流升级

**周期：2-4 周**

### 目标

把 AI 变成你的日常开发外挂，而不是偶尔问答工具。

### 学习内容

- Cursor / Codex / Claude Code / Aider 等 AI 编程工具的高级用法。
- 使用 AI 做代码阅读、重构、测试生成、Bug 定位、接口设计。
- 建立个人开发协议：
  - 需求澄清模板
  - 架构设计模板
  - Code Review 模板
  - 测试补全模板
  - Debug 复盘模板

### 项目 1：AI Dev Workflow Kit

做一个自己的 AI 开发工作流仓库，包含：

- `prompts/requirements.md`：需求分析提示模板
- `prompts/architecture.md`：架构设计提示模板
- `prompts/code_review.md`：代码审查提示模板
- `prompts/debug.md`：调试提示模板
- `prompts/refactor.md`：重构提示模板
- `scripts/ai_commit_review.py`：自动读取 git diff 并生成审查报告
- `docs/workflow.md`：你的 AI 编程流程规范

### 输出物

- 一个可展示的 GitHub 仓库。
- 一篇文章：《我是如何把 AI 接入日常开发流程的》。
- 面试表达能力：能讲清楚 AI 如何提升你的工程效率，而不是只说“我会用 ChatGPT”。

---

## Phase 2：LLM 应用基础与 RAG

**周期：4-6 周**

### 目标

掌握 LLM 应用开发基本功，尤其是 RAG。RAG 是科研助手、企业知识库、代码问答、论文问答的基础。

### 学习内容

- LLM API 调用与流式输出。
- Structured Output / JSON Schema。
- Embedding 模型。
- 向量数据库：FAISS、Chroma、Qdrant、Milvus。
- 检索算法：
  - BM25
  - Dense Retrieval
  - Hybrid Search
  - Rerank
  - HNSW
- 文档解析：
  - PDF
  - Markdown
  - HTML
  - 代码仓库
- RAG 评估：
  - Recall
  - Faithfulness
  - Context Precision
  - Answer Relevance

### 项目 2：Research Paper RAG Assistant

构建一个论文阅读助手：

- 上传 PDF 论文。
- 自动解析标题、摘要、方法、实验、结论。
- 支持按章节问答。
- 支持引用原文位置。
- 支持生成论文卡片。
- 支持多篇论文对比。
- 支持导出 Markdown 笔记。

### 深入研究点

- 不同 chunk 策略对问答质量的影响。
- HNSW 参数对检索速度和召回率的影响。
- Reranker 对幻觉率的影响。
- 长上下文模型与 RAG 的取舍。

### 输出物

- 一个论文 RAG 系统。
- 一个小型实验报告：《Chunk Size、Rerank 与 HNSW 参数对论文问答质量的影响》。
- 面试亮点：你不仅会搭 RAG，还能做评估和优化。

---

## Phase 3：Tool Use 与 MCP

**周期：4-6 周**

### 目标

从“模型回答问题”升级到“模型调用工具完成任务”。

### 学习内容

- Function Calling / Tool Calling。
- JSON Schema 设计。
- 工具调用错误处理。
- 工具权限控制。
- 工具调用日志与可观测性。
- MCP 基础：
  - MCP Server
  - MCP Client
  - Tools
  - Resources
  - Prompts
  - Sampling
- 常见 MCP 场景：
  - 文件系统
  - Git
  - 数据库
  - 浏览器
  - 搜索
  - 代码执行
  - 文档系统

### 项目 3：Personal MCP Tool Server

开发一个个人 MCP Server，提供以下工具：

- `search_files`：搜索本地文件。
- `read_file`：读取文件。
- `write_patch`：生成补丁。
- `run_tests`：运行测试。
- `query_papers`：查询论文库。
- `save_note`：保存科研笔记。
- `git_diff_summary`：总结当前代码变更。

### 深入研究点

- MCP 和普通 HTTP API Tool Calling 的差异。
- MCP Server 的权限边界设计。
- Agent 调用工具时如何避免危险操作。
- 工具描述如何影响模型选择工具的准确率。

### 输出物

- 一个可被 Claude Desktop / Codex / 自研 Agent 使用的 MCP Server。
- 一份 MCP 工具设计规范。
- 面试亮点：你能自己扩展 Agent 的工具生态。

---

## Phase 4：Agent 核心工程

**周期：6-8 周**

### 目标

理解并实现 Agent 系统，而不是只会套框架。

### 学习内容

- Agent 基本循环：
  - Observe
  - Think
  - Plan
  - Act
  - Reflect
  - Evaluate
- ReAct。
- Plan-and-Execute。
- Reflexion。
- Self-Ask。
- Tree of Thoughts / Graph of Thoughts。
- LangGraph 状态机式 Agent。
- OpenAI Agents SDK。
- AutoGen / CrewAI 多角色 Agent。
- OpenHands / SWE-agent 软件工程 Agent。

### 项目 4：Mini Agent Framework

自己实现一个最小 Agent 框架，包含：

- `Agent`
- `Tool`
- `Memory`
- `Planner`
- `Executor`
- `Critic`
- `Trace`
- `Evaluation`

建议目录：

```text
mini-agent/
  agent/
    core.py
    planner.py
    executor.py
    memory.py
    tools.py
    critic.py
    trace.py
  examples/
    code_agent.py
    research_agent.py
    data_agent.py
  tests/
  docs/
```

### 项目 5：Coding Agent for Real Repos

构建一个能处理真实代码仓库任务的 Coding Agent：

- 读取 issue。
- 搜索相关代码。
- 制定修改计划。
- 编辑文件。
- 运行测试。
- 失败后自动分析错误。
- 生成 PR 描述。

### 深入研究点

- Agent 为什么容易陷入循环。
- Agent 如何做任务分解。
- Agent 如何选择工具。
- Agent 如何处理长上下文。
- Agent 如何压缩历史轨迹。
- Coding Agent 如何构建 repo map。
- SWE-bench 类型任务的评估方法。

### 输出物

- 一个自研 Agent 框架。
- 一个 Coding Agent Demo。
- 一篇技术文章：《从零实现一个可执行任务的 Agent 框架》。
- 面试亮点：你不是 Agent 框架使用者，而是能解释和实现 Agent 架构的人。

---

## Phase 5：Agent Memory 与 Skill 系统

**周期：4-6 周**

### 目标

让 Agent 从一次性执行器升级为可积累经验的长期系统。

### 学习内容

- Memory 类型：
  - Working Memory
  - Short-term Memory
  - Long-term Memory
  - Episodic Memory
  - Semantic Memory
  - Procedural Memory
- Skill 类型：
  - Prompt Skill
  - Tool Skill
  - Workflow Skill
  - Domain Skill
  - Debug Skill
  - Research Skill
- Skill 触发：
  - 关键词触发
  - 任务分类触发
  - Embedding 检索触发
  - Planner 主动选择
- Skill 评价：
  - 成功率
  - 复用率
  - 调用成本
  - 任务完成时间

### 项目 6：Self-Improving Skill Agent

构建一个能沉淀技能的 Agent：

- 每次任务完成后生成任务复盘。
- 从复盘中提取可复用 Skill。
- 将 Skill 保存为 Markdown 或 JSON。
- 新任务开始时检索相关 Skill。
- 记录 Skill 使用效果。
- 定期合并、删除、升级 Skill。

### 深入研究点

- Skill 与 Prompt Template 的区别。
- Skill 如何避免污染和过拟合。
- Memory 如何遗忘。
- Agent 经验是否真的提升任务成功率。

### 输出物

- 一个 Skill 管理系统。
- 一个 Memory + Skill 实验报告。
- 面试亮点：你能解释 Agent 如何从“执行任务”走向“积累经验”。

---

## Phase 6：科研增强系统

**周期：6-8 周**

### 目标

用 Agent 技术系统性提升科研能力。

### 学习内容

- 文献检索自动化。
- 论文结构化阅读。
- 研究问题发现。
- Related Work 自动整理。
- 实验代码复现。
- 数据分析自动化。
- LaTeX / Markdown 写作辅助。
- Citation 管理。
- 研究日志系统。

### 项目 7：AI Research Copilot

构建一个完整科研助手：

- 输入研究方向。
- 自动检索相关论文。
- 生成论文阅读队列。
- 对每篇论文生成结构化卡片。
- 归纳方法演进脉络。
- 生成 Related Work 草稿。
- 提出可实验的研究问题。
- 管理实验计划。
- 跟踪实验结果。
- 生成周报。

### 建议聚焦研究方向

你可以从下面几个方向选择一个长期深挖：

1. **Software Engineering Agent**
   - Coding Agent
   - Debug Agent
   - Test Generation Agent
   - Repository Understanding

2. **Agent Evaluation**
   - 如何评估 Agent 的可靠性、成本、成功率和轨迹质量。
   - 适合做科研，也适合做工程平台。

3. **Memory-Augmented Agent**
   - Agent 如何记忆、遗忘、迁移经验。
   - 有研究潜力。

4. **RAG for Research**
   - 面向科研文献的高质量 RAG。
   - 可结合 GraphRAG、Citation Graph、Claim Verification。

5. **MCP Tool Ecosystem**
   - 面向开发者和科研人员的标准工具协议层。
   - 工程价值高。

### 输出物

- 一个完整科研 Agent 系统。
- 一个可作为毕业设计/科研方向的题目。
- 一篇综述或实验报告。
- 面试亮点：你能把 AI 用于真实科研流程，不只是做玩具 Demo。

---

## Phase 7：创新与个人竞争力包装

**周期：持续进行**

### 目标

把学习成果转化为求职和科研竞争力。

### 你要形成的资产

1. **GitHub 项目矩阵**
   - `ai-dev-workflow-kit`
   - `paper-rag-assistant`
   - `personal-mcp-server`
   - `mini-agent-framework`
   - `coding-agent`
   - `skill-memory-agent`
   - `ai-research-copilot`

2. **技术文章矩阵**
   - 《LLM 应用开发基础：从 Prompt 到 Tool Calling》
   - 《RAG 系统的检索、重排与评估》
   - 《MCP 是什么：为什么它会成为 Agent 工具协议》
   - 《从零实现一个 Agent 框架》
   - 《Coding Agent 如何理解代码仓库》
   - 《Agent Memory 与 Skill 系统设计》
   - 《AI 如何增强研究生科研工作流》

3. **面试故事线**
   - 我不是简单使用 AI 工具，而是把 AI 工程化接入开发流程。
   - 我理解 RAG、Agent、MCP、Memory、Evaluation 的底层机制。
   - 我能独立实现 Agent 框架和工具协议。
   - 我能把 AI 用于科研任务，并形成系统化方法。
   - 我有真实项目、实验报告和可复现代码。

4. **研究故事线**
   - 当前 Agent 系统的问题是可靠性、评估、长程任务和经验积累。
   - 我的研究关注 Agent 在软件工程或科研场景中的长期任务能力。
   - 我通过自研框架、基准任务和实验评估提出改进方法。

---

## 3. 12 个月执行计划

| 月份 | 主线 | 项目 | 输出 |
|---|---|---|---|
| 第 1 月 | AI 开发工作流 | AI Dev Workflow Kit | 工作流仓库 + 文章 |
| 第 2 月 | LLM API + RAG | Paper RAG Assistant v1 | PDF 问答系统 |
| 第 3 月 | RAG 优化 | Paper RAG Assistant v2 | RAG 评估报告 |
| 第 4 月 | Tool Use + MCP | Personal MCP Server | MCP 工具服务 |
| 第 5 月 | Agent 基础 | Mini Agent Framework | 自研 Agent 框架 |
| 第 6 月 | Coding Agent | Coding Agent Demo | 真实仓库任务 Demo |
| 第 7 月 | Memory | Agent Memory System | 长期记忆实验 |
| 第 8 月 | Skill | Self-Improving Skill Agent | Skill 管理系统 |
| 第 9 月 | Research Agent | AI Research Copilot v1 | 文献综述助手 |
| 第 10 月 | 科研实验 | Agent Evaluation / Memory 实验 | 实验报告 |
| 第 11 月 | 项目整合 | Portfolio 整理 | GitHub + 文档 + Demo |
| 第 12 月 | 求职/科研包装 | 简历、博客、论文草稿 | 面试材料 + 研究计划 |

---

## 4. 每周学习节奏

### 每周固定安排

| 时间 | 内容 |
|---|---|
| 2 小时 | 阅读论文或官方文档 |
| 4 小时 | 写项目代码 |
| 2 小时 | 做实验和评估 |
| 1 小时 | 写技术笔记 |
| 1 小时 | 整理 GitHub 和 README |

### 每周交付标准

每周至少交付一个可见成果：

- 一个功能。
- 一个实验。
- 一篇笔记。
- 一个 Demo 视频。
- 一个 README 更新。
- 一个 benchmark 结果。

---

## 5. 推荐学习顺序

不要一开始就追所有热点。推荐顺序如下：

1. **先掌握 AI 辅助开发工作流**
2. **再掌握 RAG**
3. **再掌握 Tool Use**
4. **再学习 MCP**
5. **再实现 Agent**
6. **再加入 Memory**
7. **再加入 Skill**
8. **最后做 Multi-Agent 和科研系统**

这个顺序的原因是：

- RAG 解决知识问题。
- Tool Use 解决行动问题。
- MCP 解决工具标准化问题。
- Agent 解决任务闭环问题。
- Memory 和 Skill 解决长期积累问题。
- Evaluation 贯穿所有阶段，决定系统是否真的可用。

---

## 6. 必读资料方向

### 官方文档

- OpenAI API / Agents / Tools 文档
- Anthropic MCP 文档
- LangGraph 文档
- Hugging Face Agents / smolagents 文档
- Qdrant / Milvus / FAISS 文档
- OpenHands 文档

### 论文关键词

- ReAct
- Reflexion
- Toolformer
- Tree of Thoughts
- Graph of Thoughts
- Retrieval-Augmented Generation
- GraphRAG
- SWE-bench
- Voyager
- Generative Agents
- MemGPT / Letta
- AgentBench
- RAGAS

### 开源项目

- LangGraph
- AutoGen
- CrewAI
- OpenHands
- SWE-agent
- Aider
- Letta
- LlamaIndex
- Haystack
- RAGAS

---

## 7. 项目评价标准

每个项目都要避免“能跑就行”，要按下面标准打磨：

| 维度 | 要求 |
|---|---|
| 可运行 | 新用户能按 README 跑起来 |
| 可解释 | 架构图、模块说明、设计取舍清楚 |
| 可评估 | 有 benchmark、测试集或人工评估标准 |
| 可扩展 | 工具、模型、存储可替换 |
| 可复现 | 有样例数据、配置和结果 |
| 可展示 | 有截图、Demo 视频或交互界面 |
| 可面试 | 能讲清楚难点、优化和失败案例 |

---

## 8. 你应该重点打造的差异化能力

### 8.1 工程方向差异化

你可以把自己定位成：

> 熟悉 LLM 应用、Agent 架构、MCP 工具协议和 AI 辅助软件工程的开发者。

关键证明：

- 自研 Agent 框架。
- 自研 MCP Server。
- Coding Agent 项目。
- RAG 评估报告。
- 项目 README 和 Demo 完整。

### 8.2 科研方向差异化

你可以把自己定位成：

> 研究 Agent 在软件工程和科研自动化中的可靠执行、记忆增强与评估方法。

潜在研究题目：

- 面向真实代码仓库的 Coding Agent 任务分解与上下文选择方法研究。
- 基于长期记忆的 Agent 自我改进机制研究。
- 面向科研文献综述的 RAG + Agent 混合系统研究。
- Agent 工具调用轨迹的自动评估方法研究。
- 基于 MCP 的可扩展科研 Agent 工具生态设计。

---

## 9. 最小可行执行版本（3 个月版：6 项目 × 2 周）

当前执行计划已更新为 **6 个项目各 2 周**（共 12 周），详见 `00_Roadmap/3month_plan.md`：

| # | 项目 | 周 |
|---|---|---|
| 1 | **DB Demo Studio** — AI 原生数据库教学演示平台 | W1-W2 |
| 2 | **Paper RAG Assistant** — 论文 RAG 问答系统 | W3-W4 |
| 3 | **Personal MCP Server** — 个人 MCP 工具服务 | W5-W6 |
| 4 | **Mini Agent Framework** — 自研 Agent 框架 | W7-W8 |
| 5 | **Coding Agent Demo** — 软件工程 Agent | W9-W10 |
| 6 | **Portfolio + 扩展** — 作品集 + Skill/Multi-Agent/Research Copilot | W11-W12 |

**技术栈：** React 18 + TypeScript + Vite + Tailwind CSS + React Flow（前端）；Python Flask + DeepSeek + Docker（后端）

---

## 10. 当前仓库实际结构（2026-06-02 更新）

```text
Agent_System/
  00_Roadmap/          计划、看板、Git 工作流
  00_Learning_Logs/    每日/每周/每月日志
  00_Notes/            概念笔记、论文笔记、实验记录
  00_Portfolio/        简历、面试故事、Demo 索引
  01_AI_Dev_Workflow_Kit/    AI 工作流工具包（prompts, workflow, 审查脚本）
  02_DB_Demo_Studio/         数据库课演示工具（W1-W2 主项目）
    ├── apps/web/            React 18 + TS + Vite + Tailwind（AI Studio 对话 UI）
    ├── apps/api/            Flask 后端（SSE 对话, 工具调度）
    ├── packages/demo-schema/  DemoPackage JSON Schema + 校验
    ├── packages/db-engine/   Docker MySQL 8 + PG 16 沙箱
    ├── packages/ai-tools/    8 个 LLM 可调工具（含 DeepSeek Function Calling）
    ├── packages/execution-workflow/  SQL 解析 → 6 步 DAG 引擎
    ├── packages/ai-orchestrator/    Agent Loop（占位，W1 D6-D7）
    └── docs/                架构设计 + AI 工作流 + 课纲映射
  06_RAG_Research_Assistant/   (W3 创建)
  07_MCP_Server/              (W5 创建)
  08_Mini_Agent_Framework/    (W7 创建)
  09_Coding_Agent/            (W9 创建)
```

---

## 11. 第一周行动清单（2026-05-27 已完成，以下为历史记录）

> ✅ **W1 D1-D4 已完成**：学习管理系统 + DB Demo Studio PoC #1（schema/样例/Player/db-engine/ai-tools）。
> 当前进度见 `02_DB_Demo_Studio/README.md` 及 `00_Learning_Logs/daily/2026-06-02.md`。

### 历史记录（原始 Day 1-7 计划）

### Day 1

- 整理当前仓库结构。
- 建立 `00_Roadmap`。
- 写 `weekly_plan.md`。
- 明确 12 个月主线。

### Day 2

- 选定第一个项目：`Paper RAG Assistant`。
- 确定技术栈：
  - Python
  - Flask
  - Streamlit 或 Next.js
  - Qdrant 或 Chroma
  - OpenAI / Claude / 本地模型

### Day 3

- 实现 PDF 解析。
- 生成论文结构化元数据。

### Day 4

- 实现 Embedding 和向量入库。

### Day 5

- 实现基础问答。

### Day 6

- 加入引用片段和来源定位。

### Day 7

- 写 README。
- 记录第一个实验结果。
- 写一篇短笔记：《我为什么从 Paper RAG 开始学习 AI 工程》。

---

## 12. 长期原则

1. **每个项目都要有真实使用场景**
   - 不做纯 Demo。

2. **每个系统都要有评估**
   - AI 项目没有评估，就很难证明价值。

3. **每个阶段都要写文章**
   - 写作会倒逼你真正理解。

4. **不要只调用 API**
   - 要研究系统结构、失败模式和优化方法。

5. **不要只追热点**
   - Agent、MCP、RAG、Memory、Evaluation 是长期主线。

6. **把自己当成 AI 系统工程师培养**
   - 你要能设计系统、实现系统、评估系统、解释系统。

---

## 13. 最终能力画像

完成这条路线后，你应该能做到：

- 用 AI 高效完成日常开发。
- 构建 RAG 系统并评估质量。
- 开发 MCP Server 扩展 Agent 能力。
- 自研 Agent 框架。
- 构建 Coding Agent。
- 设计 Agent Memory 和 Skill 系统。
- 用 Agent 支撑科研阅读、实验和写作。
- 在面试中系统讲清楚 LLM 应用工程。
- 在研究中找到 Agent 相关问题并设计实验。

最终你的竞争力不是“会用 AI”，而是：

> 能把 AI 变成可靠的软件系统，并能围绕这个系统做工程优化和科研创新。

