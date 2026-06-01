# 课纲 — 模板映射表

| 字段 | 值 |
|---|---|
| **日期** | 2026-06-01 |
| **状态** | 初稿，随 PoC 迭代 |
| **关联** | [需求文档](../../00_Notes/requirements/db_demo_video_requirements.md) · [架构设计](./architecture.md) |

> 将数据库课程常见章节映射到 `DemoPackage.templateType` 与 Phase 实现顺序。

---

## 8 大类课纲节点

| # | 课纲章节 | templateType | Phase 1 | Phase 2 | 可视化要点 |
|:---:|---|---|:---:|:---:|---|
| 1 | 关系模型与 SQL 基础（单表 SELECT） | `sql-explain` | ✅ | — | 解析 → 计划 → 结果集 |
| 2 | 多表查询（JOIN / 子查询） | `sql-explain` | ✅ | — | Join 算法、Nested Loop / Hash |
| 3 | 聚合与分组（GROUP BY / HAVING） | `sql-explain` | ✅ | — | 聚合节点、临时表 |
| 4 | ER 建模与概念设计 | `er-model` | ✅ | — | 实体、关系、基数 |
| 5 | 范式与模式设计 | `normalization` | ✅ | — | 1NF→3NF 分解步骤 |
| 6 | 事务与 ACID / 并发控制 | `transaction` | ✅ | — | 时间线、锁、隔离级别示意 |
| 7 | 索引与 B+ 树 | `bplus-tree` | 占位 | ✅ | B+ 树查找/插入动画 |
| 8 | 查询优化与执行计划 | `sql-explain` | ✅ | — | MySQL vs PG 计划对照 |
| 9 | 存储、日志与恢复 | `storage-recovery` | 占位 | ✅ | WAL / Checkpoint 示意 |

**Phase 1 验收：** 上表 ✅ 行各至少 1 个可生成演示；⏳ 行可用 `concept-generic` 占位。

---

## Phase 1 优先实现顺序

1. 单表 SELECT（`sql-explain`）
2. INNER JOIN（`sql-explain` + MySQL EXPLAIN）
3. ER 建模（`er-model`）
4. 范式分解（`normalization`）
5. 事务 ACID 时间线（`transaction`）
6. GROUP BY（`sql-explain`）
7. PostgreSQL 对照（JOIN 类 SQL）

---

## 变更记录

| 日期 | 变更 |
|---|---|
| 2026-06-01 | 初稿：8 大类 + Phase 1/2 标记 |
