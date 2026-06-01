# Project Matrix

> 最后更新：2026-06-01  
> API 策略：仅 DeepSeek → [`learning_constraints.md`](learning_constraints.md)  
> 时间线：**12 周**（2026-05-27 → 2026-08-27，溢出至 09-07）  
> 详细计划：[`3month_plan.md`](3month_plan.md)

| 项目 | 周次 | 状态 | 当前任务 | 下一个里程碑 | 产出物 |
|---|---|---|---|---|---|
| **DB Demo Studio** | W1 | **Building** | PoC #1：DemoPackage Schema + 样例 JSON | Player 骨架 | 演示工具 monorepo |
| AI Dev Workflow Kit | W1 | Building | Prompt 模板 + workflow 定稿 | 5 条使用记录 + workflow v1 | 模板 + 审查脚本 |
| Paper RAG Assistant | W2-4 | Not Started | — | PDF 解析 + 问答 | RAG 系统 |
| Personal MCP Server | W5-6 | Not Started | — | 前 3 个 tools | MCP Server |
| Mini Agent Framework | W7-8 | Not Started | — | Agent Loop + Critic | 自研框架 |
| Coding Agent Demo | W9 | Not Started | — | 1 个真实仓库任务 | Coding Agent |
| Skill & Multi-Agent | W10 | Not Started | — | 5+ Skill 沉淀 | 实验报告 |
| AI Research Copilot | W11 | Not Started | — | 论文卡片系统 | Research Demo |
| Portfolio | W12 | Not Started | — | 6 项目 README + 3 文章 | 作品集 |

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
| `02_DB_Demo_Studio/` | **主代码库**：需求、架构、PoC、功能实现 |
| `01_AI_Dev_Workflow_Kit/` | **工作流工具包**：`prompts/`、`workflow.md`、审查脚本 |

## 12 周主线

| 周 | 主线项目 | 关键产出 |
|---|---|---|
| **W1** | DB Demo Studio PoC + AI 工作流 | demo-schema + Player + 5 条使用记录 |
| **W2** | Paper RAG v1 | PDF 解析 + 向量入库 + 基础问答 |
| **W3** | Paper RAG v2 | Hybrid Search + 引用定位 + HNSW 实验 |
| **W4** | Paper RAG v3 + 文章 | 评估报告 + chunk 对比 + 文章 #1 定稿 |
| **W5** | MCP v1 | MCP Server 脚手架 + 前 3 tools |
| **W6** | MCP v2 | 6 tools 完成 + 工具设计规范 |
| **W7** | Mini Agent 核心 | Agent Loop + Tool Registry + Trace |
| **W8** | Agent 框架完善 | Critic + Memory lite + 框架对比 |
| **W9** | Coding Agent Demo | Repo Map + 编辑文件 + 跑测试 |
| **W10** | Skill + Multi-Agent | 5+ Skill + 对比实验 |
| **W11** | Research Copilot v1 | 论文卡片 + Related Work 草稿 |
| **W12** | Portfolio | 6 README + 3 文章 + 简历 + Demo |

## 周复盘说明

每周结束时写 `00_Learning_Logs/weekly/2026-WXX.md`，每月末写 `00_Learning_Logs/monthly/` + 能力自评。
