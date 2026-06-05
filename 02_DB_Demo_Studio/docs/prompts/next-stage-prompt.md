# 下一阶段提示词 — Stage 4 B+树与事务模拟器

你是 DB Demo Studio 的开发助手。请基于当前项目状态继续开发 Stage 4：B+树索引动画 + 事务隔离演示器。

## 必读上下文

- `02_DB_Demo_Studio/docs/requirements-spec.md` — v5 需求规格，重点 F3.2（B+树）、F3.3（事务）。
- `02_DB_Demo_Studio/docs/roadmap.md` — Stage 4 任务拆分。
- `02_DB_Demo_Studio/docs/project-snapshot.md` — 当前代码快照。
- `02_DB_Demo_Studio/docs/stage-snapshots/2026-06-02-stage-3-sql-simulator.md` — 上阶段完成快照。

## 当前阶段

Stage 4 — B+树与事务模拟器。

目标：概念类演示可播放 B+树插入/查找动画，以及 2～4 种隔离级别下的脏读/不可重复读/幻读对比。

## 任务范围

1. **类型**（`apps/web/src/lib/types.ts`）  
   - 确认 `simulationData.indexAnimation`、`simulationData.transactionDemo` 结构。

2. **B+树组件**（`apps/web/src/features/animation/BPlusTreeCanvas.tsx`）  
   - 轻量实现：节点、分裂、查找高亮；可用 SVG/Canvas，避免过重依赖。  
   - Player 在 `demoType === 'bplus-tree'` 或存在 `indexAnimation` 时渲染。

3. **事务演示**（`apps/web/src/features/animation/TransactionDemo.tsx`）  
   - 双会话时间线 + 隔离级别切换。  
   - 预设 READ UNCOMMITTED / READ COMMITTED / REPEATABLE READ / SERIALIZABLE 教学剧本。

4. **后端/工具链**  
   - 对话识别「B+树」「事务隔离」等关键词时生成对应 `simulationData`（规则或 LLM 工具）。  
   - 可参考 Stage 3 的 `sql_simulator.py` 模式新增 `index_simulator.py` / `tx_simulator.py`。

5. **示例数据**  
   - `apps/web/src/data/bplus-tree-demo.json`、`transaction-demo.json`（可选）。

## 验收标准

- `npm run build` 与 `python -m py_compile apps/api/main.py` 通过。
- 教师端输入 B+树或事务相关知识点后，Player 能展示对应模拟器（非空态）。
- 不破坏 Stage 3 SQL 模拟器与现有 Chat/WebSocket 主链路。

## 完成后必须做

1. 更新 `docs/project-snapshot.md`。  
2. 新增 `docs/stage-snapshots/YYYY-MM-DD-stage-4-bplus-tx-simulator.md`。  
3. 更新本文件为 Stage 5（课堂广播）提示词。  
4. 建议 commit：`feat(db-demo): stage 4 bplus tree and transaction simulators`

## 注意

- 先 MVP：固定剧本 + 手动步骤，再接 AI 生成。  
- UI 文案简洁中文。  
- 不要大规模重构工作台布局。
