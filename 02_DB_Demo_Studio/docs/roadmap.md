# DB Demo Studio — 规格驱动开发流程

> 来源：`docs/requirements-spec.md` v5（AI 协作对话版）  
> 当前代码快照：`docs/project-snapshot.md`  
> 阶段快照目录：`docs/stage-snapshots/`  
> 下一阶段提示词目录：`docs/prompts/`  
> 当前阶段：**阶段 4 — B+树与事务模拟器**

---

## 0. 开发原则

1. **规格先行**：所有阶段从 `requirements-spec.md` 的功能需求与验收标准反推任务。
2. **对话即产品主线**：任何功能都优先考虑如何被 AI 对话触发、修改、反馈。
3. **每阶段必须可演示**：阶段结束要有可运行路径，而不是只完成代码片段。
4. **每阶段保存快照**：更新 `project-snapshot.md`，并复制一份阶段快照到 `docs/stage-snapshots/`。
5. **每阶段输出下一阶段提示词**：保存到 `docs/prompts/next-stage-prompt.md`，方便新 Cursor 会话继续。
6. **先 MVP 后扩展**：优先完成教师能生成、编辑、播放、保存一节知识点演示的闭环。

---

## 1. 阶段总览

| 阶段 | 名称 | 对应需求 | 状态 | 核心验收 |
|---|---|---|---|---|
| Stage 0 | 基线收口与契约稳定 | 全局 | ✅ 已完成 | FastAPI + WebSocket + React 工作台可构建 |
| Stage 1 | 多对话基础设施 | F0.1-F0.4 | ✅ 已完成 | 创建/切换/删除对话，WS 自动重连 |
| Stage 2 | 对话式即时演示 P0/P1 | F1.1-F1.6, F2 | ✅ 基本完成 | SQL/概念输入后生成步骤预览和演示 |
| Stage 3 | SQL 过程模拟器 | F3.1, F3.6, SQL 场景 | ✅ 已完成 | FROM/JOIN/ON/SELECT 中间结果可逐步展示 |
| **Stage 4** | **B+树与事务模拟器** | F3.2-F3.3 | 🔄 当前 | B+树插入/查找动画；事务隔离双会话演示 |
| Stage 5 | 课堂广播与学生端闭环 | F4, F6, 三场景 | ⏳ 待做 | 教师端播放同步学生端，学生答题形成掌握度 |
| Stage 6 | 导出、快照、复用 | F0.5, F5 | ⏳ 待做 | 导出 HTML/JSON/Mermaid，版本快照可回滚 |
| Stage 7 | 持久化、性能、审计 | F0.2-F0.6, 非功能 | ⏳ 待做 | PG 持久化、LLM cache、审计日志、错误恢复 |
| Stage 8 | 教学试点与作品化 | V1 交付 | ⏳ 待做 | 真实教学案例、README、Demo 视频、面试材料 |

---

## 2. 当前阶段：Stage 4 — B+树与事务模拟器

> Stage 3 已完成，快照见 `docs/stage-snapshots/2026-06-02-stage-3-sql-simulator.md`。

### 目标

实现 B+树索引动画与事务隔离双会话演示，复用 Stage 3 的 `simulationData` + Player 嵌入模式。

### 用户故事

- 作为教师，我输入一条 JOIN SQL，系统能拆成 FROM、JOIN、WHERE、SELECT 等可播放步骤。
- 作为学生，我能看到每一步的中间表，而不只是听文字解释。
- 作为开发者，我能将模拟器结果嵌入现有 DemoPackage / Player，不破坏 P0/P1 演示。

### 任务拆分

| 优先级 | 任务 | 文件 |
|---|---|---|
| P0 | 定义 SQL 模拟器数据结构 | `apps/web/src/lib/types.ts` |
| P0 | 后端生成 `simulationData.sqlSimulator.steps` | `packages/execution-workflow/` 或 `apps/api/main.py` |
| P0 | 新增 `SqlSimulator.tsx` 渲染中间结果表 | `apps/web/src/features/animation/SqlSimulator.tsx` |
| P0 | Player 根据 `visuals.type === "sql-simulator"` 条件渲染 | `apps/web/src/features/execution-player/Player.tsx` |
| P1 | JOIN 示例数据覆盖 FROM/JOIN/ON/SELECT | `apps/web/src/data/join-query.json` |
| P1 | 后端 WS 推送时携带模拟器配置 | `apps/api/main.py` |
| P1 | 前端空态/错误态 | `SqlSimulator.tsx`, `Player.tsx` |

### 验收标准

- 输入 JOIN 示例 SQL 后，DemoPackage 中包含 `simulationData.sqlSimulator`。
- Player 至少展示 4 步：FROM students、JOIN courses、ON 过滤、SELECT 投影。
- 每一步展示中间结果行数与表格数据。
- `npm run build` 通过。
- `python -m py_compile apps/api/main.py` 通过。

### 阶段完成后必须保存

1. 更新 `docs/project-snapshot.md` 的“下一步开发”和数据流。
2. 新增 `docs/stage-snapshots/YYYY-MM-DD-stage-3-sql-simulator.md`。
3. 更新 `docs/prompts/next-stage-prompt.md` 为 Stage 4 提示词。
4. Git commit：`feat(db-demo): stage 3 sql simulator baseline`。

---

## 3. 后续阶段规划

### Stage 4 — B+树动画 + 事务演示器

**目标：** 覆盖数据库课程中最适合可视化的非 SQL / 半 SQL 内容。

| 模块 | 任务 |
|---|---|
| B+树 | 节点、阶数、插入、查找、分裂动画配置 |
| 事务 | 双会话时间线，隔离级别切换，异常现象标注 |
| Player | 根据 `demoType` / `visuals.type` 选择不同模拟器 |
| Prompt | 对话中说“演示 B+树插入 42”即可生成配置 |

**验收：** 至少 1 个 B+树案例 + 1 个事务隔离案例能播放。

### Stage 5 — 课堂广播 + 学生端闭环

**目标：** 把教师端 Player 变成课堂同步控制器。

| 模块 | 任务 |
|---|---|
| 后端 | Redis Pub/Sub room 广播 |
| ClassroomPage | 教师全屏播放、发起同步 |
| StudentPage | 只读跟随、测验、掌握度上报 |
| WS 协议 | `player:seek` → `player:sync` 多端广播 |

**验收：** 教师端切换步骤后，学生端同步更新。

### Stage 6 — 导出、快照、复用

**目标：** 让演示成为可保存、可复用、可分享的教学资产。

| 模块 | 任务 |
|---|---|
| 快照 | 每轮 AI 响应生成 DemoPackage 版本 |
| 导出 | JSON、Mermaid、HTML bundle，MP4 先占位 |
| 复用 | 基于旧演示复制新对话 |
| 对比 | 版本 A/B 差异展示 |

**验收：** 用户能保存当前演示并导出 JSON/HTML。

### Stage 7 — 持久化、性能、审计

**目标：** 从 PoC 进入可试点状态。

| 模块 | 任务 |
|---|---|
| PG | conversations/messages/demos 持久化 |
| Redis | LLM cache、room、recent messages |
| 安全 | API key 不出前端，基础权限边界 |
| 审计 | token、latency、工具调用摘要 |

**验收：** 服务重启后对话与演示仍可恢复。

### Stage 8 — 教学试点与作品化

**目标：** 形成求职/科研展示材料。

| 产物 | 要求 |
|---|---|
| README | 架构图、运行方式、功能截图 |
| Demo | 3 个教学案例：JOIN、B+树、事务隔离 |
| 文章 | AI 对话式教学演示系统设计复盘 |
| 简历 | 提炼 Agent/RAG/Tool Use/教学产品能力 |

---

## 4. 阶段快照规范

每阶段完成后创建：

```text
docs/stage-snapshots/YYYY-MM-DD-stage-N-name.md
```

模板：

```markdown
# Stage N Snapshot — 名称

## 阶段目标

## 完成内容

## 关键文件

## 运行与验证

## 已知问题

## 下一阶段入口

## 下一阶段提示词
```

同时更新：

- `docs/project-snapshot.md`
- `docs/roadmap.md`
- `docs/prompts/next-stage-prompt.md`

---

## 5. Cursor 新会话工作流

每个阶段开始时，新会话引用：

- `@02_DB_Demo_Studio/docs/requirements-spec.md`
- `@02_DB_Demo_Studio/docs/roadmap.md`
- `@02_DB_Demo_Studio/docs/project-snapshot.md`
- `@02_DB_Demo_Studio/docs/prompts/next-stage-prompt.md`

然后粘贴 `next-stage-prompt.md`。

---

## 6. 当前下一步

立即进入 **Stage 3 SQL 过程模拟器**。

推荐第一天任务：

1. 在 `types.ts` 中确认 `sqlSimulator` 数据结构。
2. 新增 `SqlSimulator.tsx`，先用静态数据渲染中间结果表。
3. 在 `Player.tsx` 根据 step.visuals.type 嵌入模拟器。
4. 用 JOIN 示例验证播放联动。
