# 需求澄清实战记录 — 连接池监控 API

> 日期：2026-05-28  
> 模板：`01_AI_Dev_Workflow_Kit/prompts/requirements.md`  
> 产出：[`2026-05-28_pool_monitor_requirements.md`](./2026-05-28_pool_monitor_requirements.md)

---

## 日期 / 任务

2026-05-28 — 为 DB Demo Studio `apps/api` 增量功能「连接池监控 API」做结构化需求澄清。

---

## 我自己原本会怎么做

- 脑子里想几个 endpoint：`/status`、`/history`
- 直接开写 Fastify route，边写边补字段
- 容易把课纲「连接池演示」和运维监控混在一起，Scope 膨胀
- 没有量化验收标准，测试阶段才发现缺鉴权

---

## AI 帮我做了什么

- 对齐 `architecture.md` 里的 Fastify + PG + Redis + BullMQ 上下文
- 拆出 4 条用户故事，区分开发者 / 运维 / 未来课纲演示
- 功能清单 P0–P2 分级（沙箱监控、Prometheus 推到 P2）
- 7 条可自动化验收标准
- 「三种理解方向」表格：运维 API vs 课纲演示 vs 沙箱监控
- 6 条待确认问题，避免 AI 过度假设鉴权与持久化

---

## 哪些地方有效

- **范围控制**：「不在范围内」6 条，直接挡住 UI/Prometheus/课纲 Player
- **与主产品对齐**：明确这是 apps/api 基础设施，不是教师功能
- **验收可测**：「5 分钟后 ≥9 个采样点」可直接写 vitest
- **响应 JSON 草案**：Day 2 architecture prompt 可直接引用

---

## 哪些地方无效 / 需修正

- AI 默认假设 `pg` Pool — **需 Day 2 确认** monorepo 实际 ORM/客户端
- admin 鉴权方案标为待确认 Q2 — **请你拍板**
- 若你 Phase 1 不做 Redis（仅 PG），F3/F4 中 redis 段可降为 P2

---

## 我如何修正 AI 输出

1. 保留 US-4「课纲演示」为远期，Phase 1 不实现 Player
2. history 采用内存环形缓冲，不写 PG 表（降低 PoC 复杂度）
3. `POST /reset` 仅 development — 生产硬禁 403

---

## 可复用经验

1. **大项目增量需求**：先画三种理解方向，再写功能清单
2. **Prompt 技巧**：附上 `@architecture.md` 片段比空描述准确 10 倍
3. **需求文档末尾加「待确认」**：把决策权留给自己，AI 只列选项
4. **下一份文档接 architecture prompt**，不要需求未确认就编码

---

## 请你确认（5 分钟）

在 [`2026-05-28_pool_monitor_requirements.md`](./2026-05-28_pool_monitor_requirements.md) §8 中确认：

- [ ] **Q2** 鉴权：`role=admin` JWT 还是独立 internal token？
- [ ] **Q3** history 是否 Phase 1 只要内存？
- [ ] **Q5** 采样间隔 30s 是否 OK？
- [ ] Phase 1 是否必须同时监控 Redis，还是 PG 优先？

确认后在 Daily Log 打勾，进入 Day 2 架构设计。
