# 3 个月加速计划（12 个月内容完整版）

> **原则：学习内容不减、验收标准不降，只压缩时间。**  
> 时间：2026-05-27 → 2026-08-27（12 周）  
> 强度：工作日 3-4h/天，周末 6-8h/天  
> 完整路线图：[`AI_Developer_Research_Roadmap.md`](../AI_Developer_Research_Roadmap.md)  
> 管理规范：[`AI_Learning_Management_Plan.md`](../AI_Learning_Management_Plan.md)

---

## 压缩策略

| 12 个月版 | 3 个月版 | 做法 |
|---|---|---|
| 7 Phase 顺序推进 | 12 周逐 Phase 推进 | 每周聚焦 1 个 Phase 子目标 |
| 每周 10-15h | 每周 25-35h | 提高投入，减少空转 |
| 概念学完再做项目 | 概念 + 项目同日并行 | 上午学概念，下午写代码 |
| 7 篇技术文章 | 7 篇保留 | 每 Phase 结束写 1 篇 |
| 阶段评分 >= 3.5 才进下一阶段 | **不变** | 未达标则该 Phase 延长 3-5 天 |

**如果某 Phase 验收未通过，允许 3 个月计划溢出 1-2 周，但不砍内容。**

---

## 12 周 ↔ 7 Phase 对照

| 周 | Phase | 原版周期 | 本周必须完成的全部内容 | 项目产出 |
|---|---|---|---|---|
| **W1** | Phase 1 | 2-4 周 | AI 编程工具、7 类开发任务、Git+AI 工作流、5 条使用记录 | **DB Demo Studio**（代码）+ AI Dev Workflow Kit（模板/工具） |
| **W2** | Phase 2 上 | 4-6 周 | LLM API、Streaming、Structured Output、Embedding、向量库、Chunking | Paper RAG v1 |
| **W3** | Phase 2 中 | | BM25、Hybrid Search、HNSW、PDF 解析、基础问答 | Paper RAG 检索优化 |
| **W4** | Phase 2 下 | | Rerank、RAG Evaluation、3 种 chunk 对比实验、引用定位 | Paper RAG v2 + 实验报告 |
| **W5** | Phase 3 上 | 4-6 周 | Function Calling、Tool Schema、Tool Router、Error Recovery | MCP 前 3 tools |
| **W6** | Phase 3 下 | | MCP Server/Client/Tool/Resource/Prompt、权限安全、6 tools 全完成 | Personal MCP Server |
| **W7** | Phase 4 上 | 6-8 周 | ReAct、Plan-and-Execute、Agent State/Trace、LangGraph 学习 | Mini Agent Loop |
| **W8** | Phase 4 中 | | OpenAI Agents SDK、AutoGen/CrewAI 对比、Planner/Executor/Critic | Mini Agent Framework |
| **W9** | Phase 4 下 | | OpenHands/SWE-agent 研究、Coding Agent Demo、SWE-bench 了解 | Coding Agent Demo |
| **W10** | Phase 5 上 | 4-6 周 | 6 种 Memory 类型、Memory 接口、检索历史任务 | Agent Memory System |
| **W11** | Phase 5 下 | | Skill 结构/触发/版本/评估、10 个 Skill 沉淀、对比实验 | Self-Improving Skill Agent |
| **W12** | Phase 6+7 | 6-8 周 | 文献检索、论文卡片、Related Work、实验计划、Portfolio 整理 | AI Research Copilot v1 |

---

## 每个 Phase 的完整验收（与 12 个月版相同）

### Phase 1 验收（W1 末）
- [ ] 在 **DB Demo Studio** 上用 AI 完成真实开发闭环（至少 PoC #1：DemoPackage + Player）
- [ ] 5 条真实 AI 辅助开发使用记录（优先 `02_DB_Demo_Studio/logs/`）
- [ ] 5 个 Prompt 模板 + workflow 文档（`01_AI_Dev_Workflow_Kit/`）
- [ ] 可选：`ai_commit_review.py` 可运行，用于提交前审查 Studio 变更
- [ ] 能 3 分钟讲清 AI 在 **DB Demo Studio** 开发流程中的作用

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

### Phase 5 验收（W11 末）
- [ ] Agent 保存并检索任务经验
- [ ] 至少 10 个 Skill
- [ ] 有无 Memory/Skill 的对比实验

### Phase 6 验收（W12 末 + 可溢出 1 周）
- [ ] 管理 20 篇论文
- [ ] 自动生成论文卡片
- [ ] Related Work 初稿
- [ ] 3 个可实验研究问题

### Phase 7（贯穿 W1-W12，W12 集中整理）
- [ ] 7 个项目 README 完整
- [ ] 每个项目有 Demo/截图/评估
- [ ] 简历 4-6 条 + 面试故事 3-5 个
- [ ] 技术文章 >= 3 篇（3 个月内），7 篇为长期目标

---

## 每日标准节奏（3 个月版）

| 时段 | 时长 | 内容 |
|---|---|---|
| 上午 | 1-1.5h | 读文档/论文/官方教程 → 写概念笔记 |
| 下午 | 2-2.5h | 项目编码 → 至少 1 个可见功能 |
| 晚上 | 0.5-1h | Daily Log + Git commit + 预习明天 |

**每天最低产出：1 条笔记 OR 1 次代码 commit OR 1 条实验记录**

---

## 周末加成（Phase 冲刺）

- **周六**：项目编码主战场（4-6h）
- **周日**：实验 + 周复盘 + 写文章（3-4h）

---

## 与 12 个月版的关系

```text
12 个月版 = 本计划的「标准速度」
3 个月版 = 本计划的「4x 加速」，内容清单 100% 对齐

如果 W4 RAG 验收 < 3.5 分 → W5 前补 3 天，MCP 顺延
如果 W9 Agent 验收 < 3.5 分 → 优先补 Agent，Research Copilot 可 v0.5
```

Phase 6 完整版在 12 个月里占 6-8 周，3 个月内完成 **v1 核心功能**，剩余功能标记为「3 个月后继续」。

---

## 当前位置

**Today = Day 1 = W1 = Phase 1 启动**

见 [`day1_2026-05-27_guide.md`](day1_2026-05-27_guide.md)
