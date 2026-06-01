# Project Matrix

> 最后更新：2026-06-02  
> API 策略：仅 DeepSeek → [`learning_constraints.md`](learning_constraints.md)  
> 时间线：**12 周**（2026-05-27 → 2026-08-27）  
> 详细计划：[`3month_plan.md`](3month_plan.md)

| 项目 | 周次 | 状态 | 当前任务 | 交付标准 |
|---|---|---|---|---|
| **DB Demo Studio** | W1-W2 | **Building** | Step 2: db-engine 沙箱 | Phase 1 Step 1-8 全部完成，Player 接真实 EXPLAIN |
| AI Dev Workflow Kit | W1-W2（并行）| Building | workflow 定稿 + prompts 实战 | 5 个模板 + workflow 文档 + 审查脚本 |
| Paper RAG Assistant | W3-W4 | Not Started | — | PDF 问答 + 引用定位 + 评估报告 |
| Personal MCP Server | W5-W6 | Not Started | — | 6 tools 可被 Claude Desktop 连接 |
| Mini Agent Framework | W7-W8 | Not Started | — | Agent Loop + Trace + Critic |
| Coding Agent Demo | W9-W10 | Not Started | — | 真实仓库任务闭环 |
| Portfolio + 扩展 | W11-W12 | Not Started | — | README + 3 文章 + Skill/Multi-Agent/Research Copilot |

## 状态说明

- `Not Started` — 未开始
- `Learning` — 概念学习阶段
- `Building` — 编码实现中
- `Testing` — 测试与评估
- `Writing` — 文档与文章
- `Done` — 阶段完成
- `Paused` — 暂停

## 双项目体系

| 目录 | 角色 |
|---|---|
| `02_DB_Demo_Studio/` | **主代码库**：需求、架构、PoC、全部 8 步实现 |
| `01_AI_Dev_Workflow_Kit/` | **工作流工具包**：`prompts/`、`workflow.md`、审查脚本 |

## 12 周总览

| 周 | 项目 | 关键产出 |
|---|---|---|
| **W1-W2** | DB Demo Studio | Phase 1 Step 1-8 可端到端演示 |
| **W3-W4** | Paper RAG | PDF 问答 + chunk 对比 + 文章 #1 |
| **W5-W6** | MCP Server | 6 tools + 工具规范 |
| **W7-W8** | Mini Agent | Loop + Trace + Critic + 框架对比 |
| **W9-W10** | Coding Agent | Repo Map + 真实仓库任务 |
| **W11-W12** | Portfolio + 扩展 | 6 README + 3 文章 + Skill/Multi-Agent/Research |

## 周复盘说明

每周结束时写 `00_Learning_Logs/weekly/2026-WXX.md`。
