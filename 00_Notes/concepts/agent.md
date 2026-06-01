# Concept: Agent

## 一句话解释

Agent 是让 LLM 从「回答问题」升级为「观察 → 思考 → 规划 → 行动 → 反思 → 评估」的闭环任务执行系统。

## 解决的问题

- 单次 LLM 调用无法完成多步骤、需工具、需迭代的复杂任务
- 需要把 LLM 的输出连接到真实世界（文件、代码、数据库、API）

## 核心机制

- **ReAct**：Reasoning + Acting 交替循环
- **Plan-and-Execute**：先规划再逐步执行
- **Reflection / Critic**：执行后自我评估，失败则调整
- **Tool Use**：通过 Function Calling 调用外部工具
- **State / Trace**：记录每步状态，便于调试和评估

## 工程实现

- 框架：LangGraph、OpenAI Agents SDK、AutoGen、CrewAI
- 自研：Agent Loop + Planner + Executor + Tool Registry + Memory + Trace

## 典型应用

- Coding Agent（OpenHands、SWE-agent）
- Research Agent（论文阅读、文献综述）
- Data Agent（数据分析流水线）

## 常见失败模式

- 陷入循环（重复调用同一工具）
- 工具选择错误（schema 描述不清）
- 上下文爆炸（长轨迹未压缩）
- 幻觉行动（调用不存在的工具或参数）

## 和其他概念的关系

- **RAG** → 提供知识
- **Tool Use / MCP** → 提供行动能力
- **Memory / Skill** → 提供经验积累
- **Evaluation** → 验证是否真正可靠

## 我自己的理解

<!-- 写 2-3 句你自己的话，不要抄上面。示例：
Agent 对我来说就是「会自己查资料、调工具、多步完成任务」的程序，
不只是聊天。今天做的 ai_commit_review 算是 Agent 的雏形：读 diff → 调 LLM → 写报告。
-->
（待填写）
Agent是让LLM具有规划、执行的能力，对于使用者可以提出实际的任务需求，LLM可以进行观察、思考、规划、行动、反思、评估，闭环的完成用户提出的需求，与早期LLM只可以进行对话时交互，真正意义上让ai有了行动力。

## 参考资料

- 论文：ReAct、Reflexion、Toolformer
- 开源：LangGraph、OpenHands、SWE-agent
- 路线图：Phase 4 — Agent 核心工程
