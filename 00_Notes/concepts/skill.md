# Concept: Skill

## 一句话解释

Skill 是把重复任务的经验、流程、工具调用封装成可复用、可触发、可版本管理的能力单元。

## 解决的问题

- Agent 每次从零开始，无法积累任务经验
- Prompt 模板散落，无法系统化管理和评估

## 核心机制

- **Skill 文件结构**：SKILL.md 定义触发条件、执行步骤、依赖工具
- **触发机制**：关键词 / 任务分类 / Embedding 检索 / Planner 主动选择
- **版本管理**：Skill 可升级、合并、淘汰
- **质量评估**：成功率、复用率、调用成本、完成时间

## 工程实现

- Cursor Skills（`.cursor/skills/`）
- Codex Skills
- 自研 Skill Manager + Skill Registry

## 典型应用

- Debug Skill：系统化调试流程
- Code Review Skill：审查 checklist
- Research Skill：论文结构化阅读流程
- MCP 集成 Skill：特定工具组合调用

## 常见失败模式

- Skill 与 Prompt Template 混淆（Skill 应有触发条件和评估）
- Skill 污染（低质量 Skill 被反复调用）
- 过拟合特定任务，泛化差

## 和其他概念的关系

- **Agent** → Agent 检索并执行 Skill
- **Memory** → Skill 是 Procedural Memory 的一种形式
- **MCP** → Skill 可编排 MCP 工具调用

## 我自己的理解

<!-- 学习过程中持续更新 -->

## 参考资料

- Cursor Agent Skills 文档
- 路线图：Phase 5 — Agent Memory 与 Skill
