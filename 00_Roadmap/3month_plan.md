# 3 个月学习路线 — 6 项目 × 2 周

> 目标：12 个月完整路线图的内容不减、验收不降，12 周内完成 6 个项目。  
> 时间：2026-05-27 → 2026-08-27（12 周，溢出缓冲至 09-07）  
> 强度：工作日 3-4h/天，周末 6-8h/天  
> 每个项目 2 周，全部深度完成  
> 完整路线图：[`AI_Developer_Research_Roadmap.md`](../AI_Developer_Research_Roadmap.md)  
> 管理规范：[`AI_Learning_Management_Plan.md`](../AI_Learning_Management_Plan.md)  
> 项目矩阵：[`project_matrix.md`](project_matrix.md)

---

## 总览

| 周 | 项目 | 验收标准 |
|---|---|---|
| **W1-W2** | **DB Demo Studio** | Phase 1 Step 1-8 全部完成，Player 接真实 EXPLAIN |
| **W3-W4** | **Paper RAG Assistant** | PDF 上传 → 问答 → 引用定位 → 评估报告 |
| **W5-W6** | **Personal MCP Server** | 6 tools，可被 Claude Desktop / 自研 Agent 连接 |
| **W7-W8** | **Mini Agent Framework** | Agent Loop + Tool Registry + Trace + Critic |
| **W9-W10** | **Coding Agent Demo** | 真实仓库：读 issue → 改代码 → 跑测试闭环 |
| **W11-W12** | **Portfolio + 扩展** | 6 README + 3 文章 + Skill/Multi-Agent/Research Copilot |

---

## Week 1-2 — DB Demo Studio

**日期：** 2026-05-27 ~ 2026-06-07  
**对应架构 Phase 1 Step 1-8**  
**主代码库：** `02_DB_Demo_Studio/`

### 目标

2 周内完成架构 Phase 1 全部 8 步，Player 可端到端演示。

### ✅ 已完成（W1 D1-D4）

| Step | 交付物 | 状态 |
|:---:|---|---|
| **1** | `schema.json` / `join-query.json` / `validate.py` / `player.html` + React Player 组件 | ✅ |
| **2** | `db-engine`（Docker MySQL 8 + PG 16）+ `execution-workflow`（SQL 6 步 DAG） | ✅ |
| **3** | `ai-tools`（8 个 LLM 工具，DeepSeek Function Calling 兼容） | ✅ |
| **4 上半** | `apps/web/`（React+TS+Vite+Tailwind 三页面）+ `apps/api/`（Flask SSE） | ✅ |

**技术栈已升级：** React 18 + TS + Vite + TailwindCSS (前端) · Python Flask (后端) · DeepSeek (LLM)

### W1 D5-D7

| 天 | Step | 任务 | 交付物 |
|---|---|---|---|
| D5 | **4 下半** | ai-orchestrator: ReAct Agent Loop + Tool Registry + SSE | `packages/ai-orchestrator/` |
| D6 | **5** | regenerate-step 单步重写 | 只改一步 narration |
| D7 | **6** | renderer: moviepy 脚手架 + MP4 导出 | `apps/renderer/` |

### W2 D1-D5

| 天 | Step | 任务 | 交付物 |
|---|---|---|---|
| D1 | **4 下半** | AI Studio SSE 对话接口 + 对话 UI | SSE 生成 ≥3 步初稿 ≤60s |
| D2 | **5** | regenerate-step 单步重写 | 「讲简单点」只改一步 |
| D3 | **6** | renderer：Remotion + MP4 + 字幕占位 | `apps/renderer/` |
| D4 | **7** | 非 SQL 工作流 ×3（ER / 范式 / 事务） | 3 个 concept-progression 示例 |
| D5 | **8** | LMS 嵌入 + 集成测试 + README | 端到端可演示 |

### W2 D6-D7 收尾

- W2 周复盘 `2026-W23.md`
- 更新 project_matrix / README

### 验收标准

- [ ] db-engine 沙箱可运行 EXPLAIN（MySQL + PG）
- [ ] execution-workflow 将 SQL 转为步骤 DAG（含 groundingRef）
- [ ] ai-tools 3 个工具可独立调用
- [ ] ai-orchestrator ReAct 循环可运行
- [ ] AI Studio 对话生成 ≥3 步初稿
- [ ] regenerate-step 只改一步
- [ ] Remotion 导出 MP4（步骤与 Player 一致）
- [ ] 3 个非 SQL 概念演示
- [ ] 使用记录 **≥5 条**
- [ ] 能 3 分钟讲清 AI 在 DB Demo Studio 开发中的作用

---

## Week 3-4 — Paper RAG Assistant

**日期：** 2026-06-08 ~ 2026-06-21  
**项目目录：** `06_RAG_Research_Assistant/`

### 目标

构建论文 RAG 系统：PDF 上传 → 问答 → 引用定位 → 评估报告。

### W3

| 天 | 任务 |
|---|---|
| D1 | 技术选型：Python + Flask + Chroma + DeepSeek + ADR 笔记 |
| D2 | PDF 解析模块（PyMuPDF）：提取标题/摘要/章节/正文 |
| D3 | Chunk 策略 + Embedding 入库 |
| D4 | 基础问答 API（检索 + LLM 回答） |
| D5 | 引用片段 + 来源定位功能 |
| D6 | 多论文切换上下文 |
| D7 | 周复盘 `2026-W24.md` |

### W4

| 天 | 任务 |
|---|---|
| D1 | BM25 + Hybrid Search 集成 |
| D2 | Reranker 集成 |
| D3 | 构建评估集（10 个问题）+ 3 种 chunk 策略对比 |
| D4 | RAGAS 评估 + 结果分析 |
| D5 | HNSW 参数实验 |
| D6 | Streamlit Demo + README |
| D7 | 周复盘 + 文章 #1 定稿 |

### 验收标准

- [ ] PDF 上传并问答
- [ ] 回答带准确来源片段
- [ ] 对比 3 种 chunk 策略
- [ ] 有 HNSW 或 rerank 实验记录
- [ ] 技术文章 #1：《RAG 系统的检索、重排与评估》定稿

---

## Week 5-6 — Personal MCP Server

**日期：** 2026-06-22 ~ 2026-07-05  
**项目目录：** `07_MCP_Server/`

### 目标

开发 Personal MCP Server，6 个工具可被 Claude Desktop / 自研 Agent 连接调用。

### W5

| 天 | 任务 |
|---|---|
| D1 | MCP 官方文档通读 + SDK 安装 + 概念笔记 |
| D2 | MCP Server 脚手架（Python SDK）：可连接 |
| D3 | 实现：`search_files` 文件搜索 |
| D4 | 实现：`read_file` 文件读取 |
| D5 | 实现：`save_note` 笔记保存 |
| D6 | 工具测试 + 错误处理 |
| D7 | 周复盘 `2026-W27.md` |

### W6

| 天 | 任务 |
|---|---|
| D1 | 实现：`run_tests` 运行测试 |
| D2 | 实现：`query_papers` 查询论文库（接 Paper RAG） |
| D3 | 实现：`git_diff_summary` 代码变更总结 |
| D4 | 工具权限 + 安全边界 + 错误处理完善 |
| D5 | MCP 工具设计规范文档 |
| D6 | 连接到 Claude Desktop + 端到端测试 |
| D7 | 周复盘 `2026-W28.md` |

### 验收标准

- [ ] MCP Server 可被 Claude Desktop 连接
- [ ] 6 个工具全部可用（schema + 测试 + 安全说明）
- [ ] 能解释 MCP vs 普通 API Tool Calling 的差异
- [ ] 工具设计规范文档

---

## Week 7-8 — Mini Agent Framework

**日期：** 2026-07-06 ~ 2026-07-19  
**项目目录：** `08_Mini_Agent_Framework/`

### 目标

自研最小 Agent 框架：Loop + Tool Registry + Trace + Critic，可完成多步任务。

### W7

| 天 | 任务 |
|---|---|
| D1 | ReAct 论文精读 + 概念笔记 |
| D2 | Agent Loop `core.py`（Observe → Think → Act） |
| D3 | Tool Registry + Function Calling 集成 |
| D4 | Planner（Plan-and-Execute 模式） |
| D5 | Executor + State 管理 |
| D6 | Trace 记录模块 |
| D7 | 周复盘 `2026-W29.md` |

### W8

| 天 | 任务 |
|---|---|
| D1 | Critic 模块（LLM-as-Judge 自我评估） |
| D2 | 失败重试 + 调整计划机制 |
| D3 | Memory 接口（lite：向量检索历史任务） |
| D4 | OpenAI Agents SDK 对比实验 |
| D5 | LangGraph / 自研框架对比笔记 |
| D6 | 集成测试：Agent 完成多步骤任务 |
| D7 | 周复盘 `2026-W30.md` + 框架对比文档 |

### 验收标准

- [ ] Agent Loop 可完成多步骤任务
- [ ] 完整执行轨迹 Trace 记录
- [ ] 失败后可重试 / 调整计划
- [ ] 能说明 LangGraph vs 自研框架差异
- [ ] 技术文章 #2：《从零实现一个 Agent 框架》定稿

---

## Week 9-10 — Coding Agent Demo

**日期：** 2026-07-20 ~ 2026-08-02  
**项目目录：** `09_Coding_Agent/`

### 目标

构建 coding agent：读 issue → 搜代码 → 改文件 → 跑测试，1 个真实仓库任务闭环。

### W9

| 天 | 任务 |
|---|---|
| D1 | OpenHands / SWE-agent 架构研究 + 源码笔记 |
| D2 | Repo Map 模块：文件树 + 符号索引 |
| D3 | Issue 解析 + 代码搜索 |
| D4 | 代码编辑模块（read → edit → write） |
| D5 | 测试运行 + 结果解析 |
| D6 | 失败自动分析 + 重试闭环 |
| D7 | 周复盘 `2026-W31.md` |

### W10

| 天 | 任务 |
|---|---|
| D1 | 选 1 个真实仓库任务（自己的项目或开源 issue）|
| D2 | Coding Agent 端到端执行 |
| D3 | 失败分析 + 修复 |
| D4 | Demo 准备 + 轨迹记录 |
| D5 | 概念卡片：Coding Agent 设计笔记 |
| D6 | README + 使用说明 |
| D7 | 周复盘 `2026-W32.md` |

### 验收标准

- [ ] Repo Map 可搜索代码符号
- [ ] 完成 1 个真实仓库任务（读 issue → 改代码 → 跑测试）
- [ ] 轨迹记录完整

---

## Week 11-12 — Portfolio + 扩展

**日期：** 2026-08-03 ~ 2026-08-27（可溢出至 09-07）  
**目录：** `00_Portfolio/` + 各项目 README

### 目标

整合全部 6 个项目 + 3 个扩展方向（Skill / Multi-Agent / Research Copilot）。

### W11 — 扩展：Skill + Multi-Agent + Research Copilot lite

| 天 | 任务 |
|---|---|
| D1 | Skill 格式设计 + 从 W1-W10 复盘提取 5 个 Skill |
| D2 | Skill Manager 注册 + 检索 + 触发 |
| D3 | Multi-Agent 概念入门（Supervisor + Specialist） |
| D4 | Research Copilot：论文卡片系统（接 Paper RAG） |
| D5 | 对比实验：有/无 Skill 的任务完成对比 |
| D6 | 端到端验证 |
| D7 | 周复盘 `2026-W33.md` |

### W12 — Portfolio 整合

| 天 | 任务 |
|---|---|
| D1-D2 | 6 个项目 README 统一对齐（架构图 + 评估 + 快速开始） |
| D3 | 文章 #3 定稿：《从 RAG 到 Agent：我的 3 个月 AI 工程学习之路》 |
| D4 | 简历提炼 4-6 条 + 面试故事 3-5 个 |
| D5 | Demo 录制 / 截图 / `demo_index.md` |
| D6-D7 | 总复盘 `2026-monthly-review.md` + GitHub pin + tag v1.0 |

### 验收标准

- [ ] 6 个项目 README 完整（架构图 + 评估 + 快速开始）
- [ ] 3 篇技术文章定稿
- [ ] 简历 4-6 条 + 面试故事 3-5 个
- [ ] 5 个 Skill + 对比实验
- [ ] Multi-Agent 概念笔记
- [ ] Research Copilot 论文卡片系统

---

## 每周固定节奏

| 时段 | 时长 | 内容 |
|---|---|---|
| 上午 | 1-1.5h | 读文档 / 论文 → 写概念笔记 `00_Notes/concepts/` |
| 下午 | 2-2.5h | 项目编码 → 至少 1 个可见产出 |
| 晚上 | 0.5-1h | Daily Log + 预习明天 |

**每天最低产出：** 1 条笔记 OR 1 次代码提交 OR 1 条使用记录  
**每周阅读：** 固定 2h 论文 / 文档（排入周末）  
**每周复盘：** 周日写 `00_Learning_Logs/weekly/2026-WXX.md`

---

## 技术文章排期

| 文章 | 期限 | 状态 |
|---|---|---|
| #1《RAG 系统的检索、重排与评估》| W4 末 | 📝 |
| #2《从零实现一个 Agent 框架》| W9 末 | 📝 |
| #3《从 RAG 到 Agent：我的 3 个月学习之路》| W12 末 | 📝 |
| 长期：MCP / Skill / Coding Agent | — | 待定 |

---

## 溢出策略

如果耗时不够，优先压缩 W11 扩展内容，不压缩核心项目时间：

| 情况 | 措施 |
|---|---|
| Phase 1 未完成 | W3 前补完，Paper RAG 合并到 1 周 |
| Phase 2 未完成 | MCP Server 工具从 6 减到 4 |
| Phase 3 未完成 | Agent 框架不写 Critic 模块 |
| Phase 4 未完成 | Coding Agent 只做框架，不做真实任务 |
| W11 扩展不够时间 | Skill 降到 3 个，Multi-Agent 做概念了解 |
| Portfolio 不够时间 | 文章降到 2 篇 |

**最大溢出：** 2026-09-07（12 周 + 2 周缓冲）

---

## 当前位置

**Today = 2026-06-02 = W1 Day 4 — Step 2 启动：db-engine**

见 [`day4_2026-06-02_guide.md`](day4_2026-06-02_guide.md)
