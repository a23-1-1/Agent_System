# Concept: MCP (Model Context Protocol)

## 一句话解释

MCP 是 Anthropic 提出的开放协议，让 AI 应用（Client）以标准化方式连接外部工具、资源和数据源（Server）。

## 解决的问题

- 每个 AI 工具各自实现文件/数据库/Git 集成，重复且不可复用
- Agent 需要统一的工具发现、调用、权限边界

## 核心机制

- **MCP Server**：暴露 Tools、Resources、Prompts
- **MCP Client**：AI 应用（Cursor、Claude Desktop、自研 Agent）连接 Server
- **Tools**：可执行操作（读文件、跑测试、查数据库）
- **Resources**：只读上下文（文件内容、配置）
- **Prompts**：预定义提示模板

## 工程实现

- Python/TypeScript SDK 实现 Server
- Cursor / Claude Desktop 作为 Client 连接
- 与 Function Calling 的区别：MCP 是协议层，Function Calling 是模型能力层

## 典型应用

- 文件系统 MCP Server
- Git / 数据库 / 浏览器 MCP Server
- 个人科研笔记 MCP Server

## 常见失败模式

- 工具描述不清晰导致模型选错工具
- 权限边界设计不当（危险操作未限制）
- Server 无错误处理，Agent 无法恢复

## 和其他概念的关系

- **Tool Use** → MCP 是 Tool 的标准化协议
- **Agent** → Agent 通过 MCP Client 调用 MCP Server
- **Skill** → Skill 可触发特定 MCP 工具组合

## 我自己的理解

MCP 像 USB 接口：Agent 不用为每个工具单独写对接代码，按 MCP 协议连上就能用。
Phase 3 会自己做 MCP Server；Day 1 先理解它和 Tool Calling 的关系即可。

## 参考资料

- Anthropic MCP 官方文档
- 路线图：Phase 3 — Tool Use 与 MCP
