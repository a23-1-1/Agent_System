# Day 1 学习指南 — Phase 1 启动（DB Demo Studio 主线）

> **当前主线项目：** [`02_DB_Demo_Studio/`](../02_DB_Demo_Studio/) — 数据库课演示生产工具  
> **工作流工具包：** [`01_AI_Dev_Workflow_Kit/`](../01_AI_Dev_Workflow_Kit/) — Prompt 模板 + 可选 `ai_commit_review.py`  
> 历史 Day 1（2026-05-27，含 ai_commit_review 实战）：[`day1_2026-05-27_guide.md`](day1_2026-05-27_guide.md)  
> 阶段：Phase 1 / W1 / Day 1  
> 预计总时长：**2.5-3 小时**

---

## 开始前（2 分钟）

```powershell
cd d:\AI_Projects\01_Research\Agent_System
git pull
```

打开文件：

1. `00_Learning_Logs/daily/{今天日期}.md` — 今日日志
2. `02_DB_Demo_Studio/README.md` — 产品目标与 Phase 1 路线图
3. `00_Notes/requirements/db_demo_video_requirements.md` — 需求澄清（Q1–Q10 已确认）
4. `AI_Developer_Research_Roadmap.md` — § Phase 1

---

## 时间块 1（30 min）— 读懂 Phase 1 + 产品上下文

**阅读：**

- `02_DB_Demo_Studio/README.md`
- `00_Notes/requirements/db_demo_video_requirements.md`（§ 产品方向、验收标准）
- `AI_Developer_Research_Roadmap.md` Phase 1 部分

Phase 1 学习双轨：

| 轨道 | 目录 | 作用 |
|---|---|---|
| **实战代码库** | `02_DB_Demo_Studio/` | 需求 → 架构 → PoC → 编码 → 测试 → 审查 |
| **工作流工具包** | `01_AI_Dev_Workflow_Kit/` | `prompts/*.md` 模板、`workflow.md`、可选审查脚本 |

**任务：** 在 Daily Log 填写：

1. 3 条个人学习目标（针对 Phase 1 + DB Demo Studio）
2. 3 个最想 AI 加速的开发场景（对应 scenarios.md 五类）
3. Phase 1 PoC 第一步你是否理解（手写 DemoPackage → Player）

**产出：** Daily Log 思考题已填写

---

## 时间块 2（45 min）— 个人化 5 个 AI 编程场景

**编辑** `01_AI_Dev_Workflow_Kit/docs/scenarios.md`

把 5 个场景的 **我的真实案例** 尽量指向 **DB Demo Studio**（或你并行的真实项目），例如：

- 场景 1：对 `db_demo_video` 做需求澄清（已有 requirements 文档，可练习「增量需求」）
- 场景 2：阅读 `02_DB_Demo_Studio/docs/architecture.md` 并补充模块边界
- 场景 3：PoC 代码提交前 Code Review

**产出：** `scenarios.md` 有 3+ 个与 DB Demo Studio 相关的真实案例

---

## 时间块 3（60 min）— 第一次 AI 辅助开发实战 ⭐

### 推荐任务（三选一）

| 选项 | 任务 | 为什么适合 Day 1 |
|---|---|---|
| **A（推荐）** | 用 `prompts/requirements.md` 为 **PoC #1** 写结构化需求（DemoPackage + Player） | 零代码也能产出；对齐架构实施步骤 #1 |
| B | 用 `prompts/architecture.md` 细化 `packages/demo-schema` 字段与 1 个示例 JSON | 直接推进单一真相源 |
| C | 你手头任意小功能，但 log 写在 `02_DB_Demo_Studio/logs/` | 保持记录路径一致 |

### 实战步骤（选项 A 示例）

**Step 1 — 需求澄清（15 min）**

1. 打开 `01_AI_Dev_Workflow_Kit/prompts/requirements.md`
2. 填入任务大意：「Phase 1 PoC：手写 DemoPackage JSON，React Player 支持 3 步逐步播放（←/→/空格），验收见 architecture 实施步骤 #1」
3. 附上 `@02_DB_Demo_Studio/docs/architecture.md` 中 `DemoPackage` 接口片段
4. 保存到 `02_DB_Demo_Studio/logs/{日期}_poc_player_requirements.md`

**Step 2 — 编码或样例数据（30 min）**

1. 在 `02_DB_Demo_Studio/packages/demo-schema/`（或 `docs/samples/`）创建 **1 个** 手写 `demo-sample.json`（≥3 步，含中英 narration 占位）
2. 或让 Cursor Agent 生成 schema 草案 + 样例 JSON（你逐字段校验）

**Step 3 — 记录（10 min）**

在 log 中填写：原本怎么做 / AI 做了什么 / 有效无效 / 修正方式 / 可复用经验

**Step 4 — Git commit（5 min，可选）**

```powershell
git add 02_DB_Demo_Studio/
git commit -m "docs: DB Demo Studio PoC player requirements + sample DemoPackage"
```

**产出：** 1 条 `02_DB_Demo_Studio/logs/` 使用记录 + 可见文件变更

---

## 时间块 4（20 min）— 概念预习 + 收尾

- `00_Notes/concepts/agent.md` / `mcp.md` / `skill.md` — 各写 2-3 句「我自己的理解」
- 更新 Daily Log：产出、经验、明日计划（见 [`weekly_plan.md`](weekly_plan.md) Day 2）

---

## Day 1 验收清单

- [ ] Daily Log 思考题已填写
- [ ] `scenarios.md` 有 3+ 个案例（优先 DB Demo Studio）
- [ ] `02_DB_Demo_Studio/logs/` 有 1 条 AI 辅助开发记录
- [ ] 读懂 PoC 顺序 #1（DemoPackage + Player）
- [ ] 至少 1 次 `git commit`（若已有文件变更）

---

## W1 预览（DB Demo Studio 主线）

| 天 | 重点 |
|---|---|
| Day 1 | 产品上下文 + PoC #1 需求/样例 JSON |
| Day 2 | `architecture.md` Prompt 实战 → 细化 demo-schema |
| Day 3 | 编码闭环：最小 Player 或 schema 校验脚本 |
| Day 4 | Debug：Player 步进/边界问题 |
| Day 5 | 可选 `ai_commit_review.py` 审查 Studio 变更 |
| Day 6 | `workflow.md` 定稿 + Kit/Studio README |
| Day 7 | 周复盘 + Phase 1 自评 |

---

## 需要帮助时

在 Cursor 中说：

> 「按 day1_guide.md 选项 A，帮我对 DB Demo Studio PoC Player 做需求澄清，并生成一份 demo-sample.json 草案」
