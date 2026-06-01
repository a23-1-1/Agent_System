# Weekly Plan - 2026-W22

> 周期：2026-05-26 ~ 2026-06-01（W1 可延续至 2026-06-02 周复盘）  
> 总目标：**6 项目 × 2 周** → [`3month_plan.md`](3month_plan.md)  
> **Phase 1 实战代码库：** [`02_DB_Demo_Studio/`](../02_DB_Demo_Studio/)  
> **工作流工具包：** [`01_AI_Dev_Workflow_Kit/`](../01_AI_Dev_Workflow_Kit/)  
> API 约束 / 命名规范 → [`learning_constraints.md`](learning_constraints.md)

---

## 本周目标

1. DB Demo Studio **Step 1 完成**（✅ schema + Player + 6 步 JSON + 校验）
2. DB Demo Studio **Step 2 启动**（db-engine Docker 沙箱 + execution-workflow 基础）

---

## 当前进度

### Day 1-3 ✅ 已完成

| D | 任务 | 状态 |
|---|---|---|
| D1 | 学习管理系统 + scenarios.md + 首次 AI 实战 | ✅ |
| D2 | 架构 Prompt 实战（ai-orchestrator 模块细化）| ✅ |
| D3 | schema.json / join-query.json / validate.py / player.html / 使用记录 #3 #4 | ✅ |

### Day 4 — Step 2 启动：db-engine

> 详细流程：[`day4_2026-06-02_guide.md`](day4_2026-06-02_guide.md)

- [ ] db-engine：Docker MySQL 8 + PG 16 沙箱
- [ ] Python 连接脚本 + .env 配置
- [ ] 第 5 条使用记录
- [ ] Daily Log + 周复盘草稿

### Day 5 — Step 2 下半：execution-workflow

- [ ] SQL 解析（node-sql-parser / Python 替代方案）
- [ ] 步骤 DAG + 状态机
- [ ] 第 使用记录

### Day 6 — Step 3：ai-tools

- [ ] explain_mysql + explain_pg 工具函数
- [ ] validate_demo_package

### Day 7 — 周复盘

- [ ] `2026-W22.md` 周复盘
- [ ] 更新 project_matrix

---

## 验收标准（Week 1-2 结束）

- DB Demo Studio Step 1-8 全部完成
- Player 接真实 EXPLAIN 数据
- 使用记录 **≥5 条**
- 5 个 Prompt 模板 + workflow 文档
- 能口头讲清楚 AI 在 DB Demo Studio 开发中的作用
