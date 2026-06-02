# Weekly Plan - 2026-W22

> 周期：2026-05-26 ~ 2026-06-01（W1 延续至 2026-06-02）  
> 总目标：**DB Demo Studio 两周完整实现 → Phase 1 MVP 全量需求**  
> **需求文档：** [`db_demo_video_requirements.md`](../00_Notes/requirements/db_demo_video_requirements.md) §10 Phase 1 MVP  
> **架构文档：** [`02_DB_Demo_Studio/docs/architecture.md`](../02_DB_Demo_Studio/docs/architecture.md)  
> API 约束 / 命名规范 → [`learning_constraints.md`](learning_constraints.md)

---

## W1-W2 总目标

在 2 周内完成需求文档 Phase 1 MVP **全部要求**：AI Studio 对话生成、Execution Player、单步重写、MP4 导出、非 SQL 模板 ≥3 类、LMS 试嵌入、三场景 UX。

## W1 D1-D4 已完成

| D | 架构 Step | 交付 | 需求对应 |
|---|---|---|---|
| D1-D2 | — | 学习管理系统 + 场景分析 + 架构 Prompt 实战 | Phase 1 学习 |
| D3 | **Step 1** | schema.json / 6步JOIN样例 / validate.py / player.html | F5（逐步播放）✅ |
| D4 | **Step 2** | db-engine Docker沙箱 + execution-workflow SQL解析引擎 | F3, F9 ✅ |

---

## W1 D5-D7 + W2 新规划

### D5 — Step 3：ai-tools

> 详细指南：待创建 `day5_2026-06-02_guide.md`

- [ ] `packages/ai-tools/tools.py` — explain_mysql, explain_pg, validate_demo_package, assemble_execution_steps
- [ ] `packages/ai-tools/tests/` — 工具单元测试
- [ ] 工具注册机制（ToolRegistry）
- [ ] 使用记录

### D6 — Step 4 上半：ai-orchestrator

- [ ] `packages/ai-orchestrator/core.py` — Agent Loop (ReAct: Observe→Think→Act)
- [ ] `packages/ai-orchestrator/tools.py` — Tool Registry + DeepSeek Function Calling 集成
- [ ] `packages/ai-orchestrator/session.py` — SessionStore 会话管理
- [ ] `packages/ai-orchestrator/sse.py` — SSE 流式输出
- [ ] 使用记录

### D7 — Step 4 下半 + Step 5：AI Studio 后端 + 前端

- [ ] `apps/api/` — FastAPI 后端：POST /ai/chat (SSE), POST /ai/regenerate-step
- [ ] `apps/ai-studio.html` — AI Studio 对话 UI（纯 HTML + SSE EventSource）
- [ ] regenerate-step 接口与单步重写验证
- [ ] 第 使用记录

### W2 D1 — Step 6：Renderer（MP4 导出）

- [ ] Python moviepy 脚手架：DemoPackage → MP4 基础导出
- [ ] 中英双语字幕轨（SRT 生成 + 嵌入 MP4）
- [ ] 使用记录

### W2 D2 — Step 7 上半：非 SQL 工作流

- [ ] ER 建模演示 JSON：concept-progression 工作流
- [ ] 范式 1NF→3NF 演示 JSON
- [ ] 使用记录

### W2 D3 — Step 7 下半：非 SQL + 课纲库

- [ ] 事务/ACID 时间线演示 JSON
- [ ] 课纲章节模板索引（对应 8 大类）
- [ ] 使用记录

### W2 D4 — Step 8 上半：LMS 嵌入

- [ ] iframe 嵌入 demo（兼容 Moodle/超星）
- [ ] Share link 页面（包含只读 Player）
- [ ] 使用记录

### W2 D5 — Step 8 下半：三场景 UX

- [ ] 备课场景：AI Studio → 保存草稿
- [ ] 课堂场景：Player 全屏演示模式
- [ ] 学生场景：只读链接（无编辑、无对话框）
- [ ] 使用记录

### W2 D6 — 集成测试

- [ ] 端到端测试：教师「选 JOIN → 对话生成 → 编辑一步 → 发布网页 → 导出 MP4 → LMS 嵌入」全流程
- [ ] 验收标准对照需求文档 §6

### W2 D7 — 收尾

- [ ] README 更新 + 架构图
- [ ] W2 复盘 `2026-W23.md`
- [ ] 演示录屏 / 截图

---

## 与需求文档逐条对照

| # | 功能 | 完成日 | 状态 |
|---|---|---|---|
| F0 | AI Studio 对话界面 | W1 D7 | 🔲 |
| F0b | 执行演示工作流 | W1 D4 | ✅ |
| F0c | 单步 AI 重写 | W1 D7 | 🔲 |
| F1 | 课纲节点输入 | W2 D2 | 🔲 |
| F2 | Agent+LLM 讲解词 | W1 D5-D6 | 🔲 |
| F3 | SQL 分步执行 | W1 D5 | ✅ |
| F4 | 可视化表/索引/计划树 | W2 D1 | 🔲 |
| F5 | 逐步播放/暂停 | W1 D3 | ✅ |
| F6 | 教师编辑每步 | W1 D7 | 🔲 |
| F7 | 发布交互网页 | W2 D4 | 🔲 |
| F8 | 导出 MP4 | W2 D1 | 🔲 |
| F9 | MySQL/PG 对照 | W1 D4-D5 | ✅ |
| F10 | 课纲模板库 ≥8 类 | W2 D3 | 🔲 |
| F11 | 三场景 UX | W2 D5 | 🔲 |
| F12 | LMS 集成 | W2 D4 | 🔲 |
| F13 | 字幕+双语 | W2 D1-D2 | 🔲 |
| F14 | 非SQL可视化 | W2 D2-D3 | 🔲 |
| F15 | 付费API用量可见 | W1 D6 | 🔲 |

## 验收标准（W2 结束）

- [ ] 教师 AI Studio 对话 → SSE 生成 ≥3 步初稿 ≤60s
- [ ] 每步含 workflowPhase + groundingRef
- [ ] 「讲简单点」只改一步
- [ ] 教师可修改任一步
- [ ] 发布交互网页
- [ ] 导出中英双语字幕 MP4
- [ ] ≥8 类课纲模板
- [ ] MySQL + PG 双引擎对照
- [ ] 三场景 UX 可用
- [ ] LMS 试嵌入成功
