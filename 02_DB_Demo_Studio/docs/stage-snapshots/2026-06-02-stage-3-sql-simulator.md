# Stage 3 Snapshot — SQL 过程模拟器

> 日期：2026-06-02  
> 阶段：Stage 3 完成，进入 Stage 4  
> 来源：`docs/requirements-spec.md` v5 — F3.1 SQL/过程模拟器

---

## 阶段目标

JOIN 类 SQL 演示除 6 阶段工作流讲解外，在 Player 中展示 FROM → JOIN → ON → SELECT 的中间结果表，并与工作流步骤进度联动。

---

## 完成内容

| 模块 | 说明 |
|---|---|
| `packages/execution-workflow/sql_simulator.py` | 根据 SQL 生成 `simulationData.sqlSimulator.steps`（JOIN / 简单 SELECT） |
| `apps/api/main.py` | `_build_demo_from_sql` 挂载 `simulationData`，execute/result 步标记 `visuals.type=simulator-step` |
| `apps/web/src/features/animation/SqlSimulator.tsx` | 步骤条 + 中间表 + 行数说明 |
| `apps/web/src/features/execution-player/Player.tsx` | 工作流索引映射到模拟器步骤，有数据时渲染 SqlSimulator |
| `apps/web/src/data/join-query.json` | 离线示例含完整 4 步模拟数据 |
| `apps/web/src/lib/types.ts` | `sqlSimulator.steps[].rows` 类型补充 |

---

## 验收

```bash
python -m py_compile apps/api/main.py
python packages/execution-workflow/sql_simulator.py
cd apps/web && npm run build
```

- 教师工作台发送含 JOIN 的 SELECT → `demo:complete` 包内含 `simulationData.sqlSimulator`。
- Player 播放时模拟器步骤随 6 阶段进度推进（0→3 映射）。
- 课堂/学生页 fallback `join-query.json` 可直接看到模拟器。

---

## 示例 SQL

```sql
SELECT s.name, c.course_name
FROM students s
INNER JOIN courses c ON s.id = c.student_id
```

---

## 已知限制

- 中间表数据为教学用静态样本，非真实引擎执行结果。
- 未实现 WHERE 独立步骤（可在 Stage 3.x 扩展）。
- `visuals.type` 使用 `simulator-step`，与规格中的 `sql-simulator` 命名略有差异，前端以 `simulationData` 存在为准。

---

## 下一阶段

见 `docs/prompts/next-stage-prompt.md` — Stage 4：B+树动画 + 事务隔离演示器。
