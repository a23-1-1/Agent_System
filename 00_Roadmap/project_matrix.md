# Project Matrix

> 最后更新：2026-06-01  
> API 策略：仅 DeepSeek → [`learning_constraints.md`](learning_constraints.md)  
> 时间线：**3 个月**（2026-05-27 → 2026-08-27）  
> 详细计划：[`3month_plan.md`](3month_plan.md) · 加速版：[`3month_full_plan.md`](3month_full_plan.md)

| 项目 | Phase | 状态 | 当前任务 | 下一个里程碑 | 产出物 |
|---|---|---|---|---|---|
| **DB Demo Studio** | Phase 1 实战代码库 | **Building** | PoC #1：DemoPackage Schema + 样例 JSON + 校验 | Runner Player 骨架 | 演示工具 monorepo |
| AI Dev Workflow Kit | Phase 1 工具包 | Building | Prompt 模板 + workflow 定稿 | 5 条使用记录 + workflow v1 | 模板 + 可选审查脚本 |
| Paper RAG Assistant | Phase 2 | Not Started | — | PDF 解析模块 | Demo |
| Personal MCP Server | Phase 3 | Not Started | — | 实现第一个 tool | MCP Server |
| Mini Agent Framework | Phase 4 | Not Started | — | Agent Loop | 框架代码 |
| Skill Memory Agent | Phase 5 | Not Started | — | Skill 格式设计 | 实验报告 |
| AI Research Copilot | Phase 6 | Not Started | — | 论文卡片系统 | Research Demo |

## 状态说明

- `Not Started` — 未开始
- `Learning` — 概念学习阶段
- `Building` — 编码实现中
- `Testing` — 测试与评估
- `Writing` — 文档与文章
- `Done` — 阶段完成
- `Paused` — 暂停

## Phase 1 双项目分工

| 目录 | 角色 |
|---|---|
| `02_DB_Demo_Studio/` | **主代码库**：需求、架构、PoC、功能实现、测试、调试、重构 |
| `01_AI_Dev_Workflow_Kit/` | **工作流工具包**：`prompts/`、`workflow.md`、`ai_commit_review.py`（可选提交前审查） |

## 3 个月主线

| 月份 | 周 | 主线项目 | 关键产出 |
|---|---|---|---|
| **M1** | W1 | **DB Demo Studio** PoC + AI 工作流沉淀 | DemoPackage 样例 + Player PoC + 5 条使用记录 |
| M1 | W2 | Paper RAG v1 | PDF 解析 + 向量入库 |
| M1 | W3 | Paper RAG v2 | 引用定位 + chunk 实验 |
| M1 | W4 | Paper RAG 打磨 | Demo + 评估报告 + 文章 |
| **M2** | W5 | MCP Server 基础 | 3 tools + 可连接 |
| M2 | W6 | MCP 完善 | 6 tools + Agent 架构设计 |
| M2 | W7 | Mini Agent 核心 | Loop + Tools + Trace |
| M2 | W8 | Agent + MCP 集成 | 端到端 Demo + Memory lite |
| **M3** | W9 | Coding Agent | issue→改代码→测试闭环 |
| M3 | W10 | Skill lite + Research 入口 | Skill 库 + 论文卡片 |
| M3 | W11 | 项目整合 | 简历 + 面试故事 + 评估汇总 |
| M3 | W12 | 作品集 | GitHub + tag v1.0-portfolio |
