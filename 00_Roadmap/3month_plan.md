# 3 个月压缩学习路线

> 目标：3 个月内完成 4 个核心项目 + 1 个整合项目，形成求职/科研可用的作品集。  
> 前提：资深程序员背景，每天可投入 2-4 小时，周末可加量。  
> 原则：**深度优先于广度**，每个项目必须有评估和 README。

---

## 与 12 个月版的差异

| 12 个月版 | 3 个月版 |
|---|---|
| 7 个 Phase 全做 | 聚焦 4+1 个项目 |
| 每个概念深挖 + 多篇论文 | 核心论文 + 官方文档 |
| Memory/Skill 独立 4-6 周 | 合并进 Agent 项目（lite 版） |
| 6-8 篇技术文章 | 2-3 篇 + 完整 README |
| Multi-Agent 独立项目 | 作为 Agent 项目扩展（可选） |

**3 个月后你应该有的能力：**
- 用 AI 高效开发（Workflow Kit 模板 + DB Demo Studio 实战）
- 构建并评估 RAG 系统
- 自研 MCP Server
- **自研 Mini Agent 框架**（核心竞争力）
- Coding Agent Demo
- 能系统讲清楚 Agent / MCP / RAG / Tool Use

---

## 总览

```text
M1 (W1-W4)   AI工作流 → RAG 论文助手
M2 (W5-W8)   MCP Server → Mini Agent 框架
M3 (W9-W12)  Coding Agent → 整合 + 作品集
```

---

## Month 1：AI 工作流 + RAG（W1-W4）

### Week 1 — AI 工作流 + DB Demo Studio PoC

| 天 | 任务 | 产出 |
|---|---|---|
| D1-D2 | Prompt 实战（需求/架构）+ `scenarios.md` | 模板验证 + Studio `logs/` |
| **D3-D4** | **PoC #1**：DemoPackage JSON Schema + 样例 + 校验 | `02_DB_Demo_Studio/packages/demo-schema/` |
| D5 | 可选 `ai_commit_review.py` 审查 Studio diff | 审查报告 |
| D6-D7 | Player 骨架 / `workflow.md` + README + 阶段复盘 | Studio PoC 可演示 |

**验收**：5 条使用记录 + PoC #1 可演示 + 3 分钟能讲 AI 在 Studio 开发中的作用

详见 [`weekly_plan.md`](weekly_plan.md) Week 1 分解。

### Week 2 — Paper RAG v1（解析 + 入库）

| 任务 | 产出 |
|---|---|
| 技术选型：Python + FastAPI/Streamlit + Chroma/Qdrant | ADR 笔记 |
| PDF 解析（PyMuPDF / pdfplumber） | 解析模块 |
| Chunk + Embedding + 向量入库 | 检索模块 |
| 基础问答 API | 能问能答 |

### Week 3 — Paper RAG v2（引用 + 评估）

| 任务 | 产出 |
|---|---|
| 引用来源定位（返回 chunk + 页码） | 引用功能 |
| 对比 3 种 chunk 策略 | 实验记录 |
| RAGAS 或人工评估 10 个问题 | 评估报告 |

### Week 4 — Paper RAG 打磨 + 文章

| 任务 | 产出 |
|---|---|
| Streamlit/前端 Demo | 可展示 |
| README 完善 | 项目可复现 |
| 技术笔记：《Chunk 策略对论文问答的影响》 | 文章草稿 |
| 月复盘 M1 | monthly review |

**M1 里程碑**：2 个完整项目（Workflow Kit + Paper RAG）

---

## Month 2：MCP + Agent 框架（W5-W8）

### Week 5 — MCP 基础 + 前 3 个 Tool

| 任务 | 产出 |
|---|---|
| 读 MCP 官方文档 + 概念笔记 | `mcp.md` 更新 |
| Python MCP Server 脚手架 | 可连接 |
| 实现：search_files, read_file, save_note | 3 tools |

### Week 6 — MCP 完善 + Agent 预习

| 任务 | 产出 |
|---|---|
| 实现：git_diff_summary, run_tests, query_papers | 6 tools 完成 |
| MCP 工具设计规范文档 | 规范 |
| 读 ReAct 论文 + LangGraph 文档 | agent.md 更新 |
| 设计 Mini Agent 架构 | 架构图 |

### Week 7 — Mini Agent Framework 核心

| 任务 | 产出 |
|---|---|
| Agent Loop（Observe → Think → Act） | `core.py` |
| Tool Registry + Function Calling | `tools.py` |
| Planner + Executor | 多步任务可跑 |
| Trace 记录 | 完整轨迹 |

### Week 8 — Agent 框架完善 + MCP 集成

| 任务 | 产出 |
|---|---|
| Critic / 失败重试 | 容错能力 |
| Agent 连接自研 MCP Server | 端到端 Demo |
| Memory 接口（lite：向量检索历史任务） | memory.py |
| 对比：LangGraph vs 自研框架 | 设计笔记 |
| 月复盘 M2 | monthly review |

**M2 里程碑**：MCP Server（6 tools）+ 自研 Agent 框架（核心竞争力）

---

## Month 3：Coding Agent + 整合（W9-W12）

### Week 9 — Coding Agent Demo

| 任务 | 产出 |
|---|---|
| 研究 OpenHands / SWE-agent 架构 | 源码笔记 |
| Repo Map：文件树 + 符号索引 | repo_map 模块 |
| Agent 任务：读 issue → 搜代码 → 改文件 → 跑测试 | Demo |
| 失败自动分析 + 重试 | 1 个完整任务闭环 |

### Week 10 — Skill 系统（lite）+ Research 入口

| 任务 | 产出 |
|---|---|
| Skill 文件格式 + 检索触发 | skill_manager |
| 从任务复盘提取 Skill（3-5 个） | 初始 Skill 库 |
| 论文卡片生成（接 Paper RAG） | Research 入口 |
| Related Work 草稿生成（lite） | Copilot v0.1 |

### Week 11 — 项目整合 + 评估

| 任务 | 产出 |
|---|---|
| 统一 README / Demo 索引 | `00_Portfolio/demo_index.md` |
| 每个项目补评估结果 | 评估汇总 |
| 简历条目 4 条 | `resume_items.md` |
| 面试故事 3 个 | `interview_stories.md` |

### Week 12 — 作品集 + 复盘

| 任务 | 产出 |
|---|---|
| GitHub 整理（pin 4 个项目） | 公开仓库 |
| 技术文章第 2 篇（Agent 框架） | 文章 |
| 3 个月总复盘 | `00_Learning_Logs/monthly/2026-08.md` |
| 研究问题提炼（1 个可继续的方向） | 研究计划草稿 |

**M3 里程碑**：Coding Agent Demo + 完整作品集

---

## 项目优先级（时间不够时砍什么）

**必做（P0）：**
1. AI Dev Workflow Kit
2. Paper RAG Assistant（含评估）
3. Personal MCP Server
4. Mini Agent Framework

**强烈建议（P1）：**
5. Coding Agent Demo

**有余力再做（P2）：**
6. Skill lite 版
7. AI Research Copilot lite
8. Multi-Agent

**可以砍掉：**
- 独立 Memory 系统（合并进 Agent）
- 独立 Multi-Agent 项目
- 多篇技术文章（保 2 篇高质量的）

---

## 每周时间分配（建议）

| 活动 | 小时/周 |
|---|---:|
| 写项目代码 | 8-12 |
| 读文档/论文 | 2-3 |
| 实验与评估 | 2-3 |
| 写笔记/日志 | 1-2 |
| Git 提交与整理 | 0.5-1 |
| **合计** | **14-20** |

---

## 3 个月成果清单

完成后你应有：

- [ ] 4-5 个 GitHub 项目（每个有 README + Demo）
- [ ] 30+ Daily Log
- [ ] 12 Weekly Review
- [ ] 3 Monthly Review
- [ ] 2-3 篇技术文章
- [ ] 4 条简历项目描述
- [ ] 3 个面试 3 分钟故事
- [ ] 1 个可继续的研究方向

---

## 能力自评时间表

| 时间 | 自评重点 |
|---|---|
| M1 末 | RAG 能讲清楚 + 有评估数据 |
| M2 末 | Agent 框架能画图讲架构 + MCP 能演示 |
| M3 末 | Coding Agent 能跑 + 作品集完整 |

每月末用 `AI_Learning_Management_Plan.md` §7 评分表自评，平均分 < 3.5 则下月先补短板。
