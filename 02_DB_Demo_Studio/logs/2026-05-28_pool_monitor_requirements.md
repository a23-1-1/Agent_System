# 需求澄清：连接池监控 API

| 字段 | 值 |
|---|---|
| **日期** | 2026-05-28 |
| **项目** | DB Demo Studio (`02_DB_Demo_Studio`) |
| **模块** | `apps/api` — 运维可观测性（增量需求） |
| **方法** | `01_AI_Dev_Workflow_Kit/prompts/requirements.md` 模板 |
| **状态** | 已澄清，待架构设计（Day 2 architecture prompt） |
| **关联** | 架构 § Phase 1「API 用量可观测」；课纲节点「连接管理/连接池」可复用为演示模板 |

---

## 原始需求（口头描述）

> 在 DB Demo Studio 的 Fastify API 中新增**连接池监控 API**，让运维/开发者在 Phase 1 开发阶段能实时查看 PostgreSQL 业务库与 Redis（BullMQ）连接池状态，并保留最近一段时间的采样历史，用于排查连接泄漏、池耗尽、慢查询堆积等问题。

**增量背景：** 主产品需求见 [`db_demo_video_requirements.md`](../../00_Notes/requirements/db_demo_video_requirements.md)；本需求是 **apps/api 基础设施**，不面向课堂教师 UI，Phase 1 仅内部/管理员使用。

**现有上下文：**

- 技术栈：Node.js + Fastify；PostgreSQL 16 业务库；Redis + BullMQ 任务队列
- 架构：[`docs/architecture.md`](../docs/architecture.md) — `apps/api` REST 端点、`db-engine` 沙箱 Docker
- 约束：敏感 SQL 不出境；API Key 服务端；Phase 1 需「用量可观测与失败降级」

---

## 1. 需求摘要

为 `apps/api` 提供一组 **只读 REST 端点**，暴露 PostgreSQL 与 Redis 连接池的实时指标（活跃/空闲/等待/上限）及可配置时间窗口内的历史采样，供开发与运维在 PoC/Phase 1 阶段诊断连接问题；默认仅 **管理员/开发环境** 可访问，不暴露给学生/教师课堂路径。

---

## 2. 用户故事

### US-1 开发排查

- **As a** DB Demo Studio 后端开发者  
- **I want** 调用 `GET /api/pool/status` 查看当前 PG/Redis 池状态  
- **So that** 本地或 staging 出现 503/超时我能快速判断是否为连接池耗尽

### US-2 趋势观察

- **As a** 运维/开发者  
- **I want** 查询最近 N 分钟的池指标历史  
- **So that** 我能发现缓慢泄漏（active 持续上升、idle 持续下降）

### US-3 测试后重置（可选）

- **As a** 开发者  
- **I want** 在开发环境重置内存中的统计计数器  
- **So that** 每次集成测试前从干净基线开始（**生产环境禁用**）

### US-4 未来课纲演示（Out of Phase 1 实现，In Scope 设计预留）

- **As a** 数据库课教师（未来）  
- **I want** 将「连接池原理」作为 `curriculum` 模板的一种可视化演示  
- **So that** 学生理解客户端连接池与数据库 `max_connections` 的关系  

→ Phase 1 仅保证 API 返回的数据结构 **可被未来 DemoPackage 引用**，本迭代不做 Player UI。

---

## 3. 功能点清单

| # | 功能 | 优先级 | 说明 |
|---|---|:---:|---|
| F1 | `GET /api/pool/status` 返回 PG + Redis 实时快照 | **P0** | JSON；含 timestamp、各池指标 |
| F2 | PostgreSQL 池指标：total / idle / active / waiting / max | **P0** | 基于 `pg`/`postgres.js` pool 或等价客户端 |
| F3 | Redis 池指标：connected / ready / blocked / max | **P0** | 基于 ioredis 或 node-redis 连接状态 |
| F4 | `GET /api/pool/history?window=15m&interval=30s` 历史序列 | **P0** | 内存环形缓冲即可；默认 window=15m |
| F5 | 后台定时采样（默认 30s）写入 history | **P0** | 进程内；可配置 interval |
| F6 | 管理员鉴权：非 dev 环境需 `Authorization` 或 internal token | **P0** | 学生/教师 JWT **不可**访问 |
| F7 | 健康联动：`status` 中 `healthy: boolean` + `issues[]` | **P1** | 如 active/max > 0.9 → warning |
| F8 | `POST /api/pool/reset` 重置统计（仅 `NODE_ENV=development`） | **P1** | 生产返回 403 |
| F9 | OpenAPI / 路由文档注释 | **P1** | 对齐 Fastify schema |
| F10 | `db-engine` 沙箱池状态（MySQL/PG Docker） | **P2** | Phase 1 可返回 `not_implemented` |
| F11 | Prometheus `/metrics` 导出 | **P2** | Phase 2 运维 |

---

## 4. 边界条件与异常场景

| 场景 | 期望行为 |
|---|---|
| PostgreSQL 尚未连接 / 启动中 | `status.postgres.state = "disconnected"`；`healthy=false`；issues 含原因 |
| Redis 不可用 | 同上；history 仍保留 PG 侧数据 |
| 池已满，新请求等待 | `waiting > 0`；`issues` 含 `pool_exhaustion` |
| 非 admin 访问 | `401 Unauthorized` 或 `403 Forbidden` |
| `window` 超过上限（如 >24h） | `400` + 错误信息；默认 cap=24h |
| 生产环境调用 `POST /reset` | `403 Forbidden` |
| 高并发采样 | 采样器单线程；history 写锁；不阻塞业务连接 |
| API 进程多实例 | Phase 1 **单实例**；history 为进程本地（文档注明）；Phase 2 可迁 Redis |

---

## 5. 验收标准（可测试）

| # | 条件 | 验证方式 |
|---|---|---|
| AC-1 | 服务启动后 60s 内 `GET /api/pool/status` 返回 200 | curl + 集成测试 |
| AC-2 | 响应含 `postgres` 与 `redis` 两对象，各含 `active`/`idle`/`max` 数值字段 | JSON schema 测试 |
| AC-3 | 运行 5 分钟后 `GET /api/pool/history?window=5m` 返回 ≥9 个采样点（30s 间隔） | 自动化测试或手动 |
| AC-4 | 无 token 访问 staging 返回 401/403 | 安全测试 |
| AC-5 | 模拟 10 个并发 DB 查询后 `active` 上升、`idle` 下降 | 负载脚本 + status 对比 |
| AC-6 | dev 环境 `POST /api/pool/reset` 后 history 清空；production 403 | 环境变量切换测试 |
| AC-7 | OpenAPI 或 README 列出请求/响应示例 | 文档审查 |

---

## 6. 不在范围内（Phase 1 明确排除）

- ❌ 教师/学生 Web UI 仪表盘
- ❌ `db-engine` Docker 沙箱内 MySQL/PG 池监控（P2）
- ❌ 告警推送（邮件/钉钉/Slack）
- ❌ 跨实例聚合、Prometheus/Grafana 集成
- ❌ 连接池参数动态调整（仅监控，不改配置）
- ❌ 作为课纲 DemoPackage 的可视化 Player（仅数据结构预留）

---

## 7. 技术约束与依赖

| 项 | 说明 |
|---|---|
| 运行时 | Node.js 20+；Fastify 4.x |
| PG 客户端 | 与 `apps/api` 现有选型一致（`pg` pool 或 Prisma/Drizzle 底层 pool） |
| Redis | BullMQ 共用连接；ioredis `status` 字段 |
| 存储 | history 进程内存环形队列；默认 1440 点（24h @ 30s） |
| 鉴权 | 复用 api 已有 admin middleware；dev 可 `POOL_MONITOR_PUBLIC=true` 跳过 |
| 配置 | 环境变量：`POOL_SAMPLE_INTERVAL_MS`、`POOL_HISTORY_MAX_POINTS` |
| 测试 | vitest 或 tap；需 mock pool 或 testcontainers |
| 目录建议 | `apps/api/src/routes/pool/` + `apps/api/src/services/pool-monitor.ts` |

### 响应结构草案（供架构 Prompt 细化）

```json
{
  "timestamp": "2026-05-28T10:00:00.000Z",
  "healthy": true,
  "issues": [],
  "postgres": {
    "state": "connected",
    "active": 2,
    "idle": 8,
    "waiting": 0,
    "max": 10
  },
  "redis": {
    "state": "ready",
    "connected": 1,
    "max": 10
  }
}
```

---

## 8. 待确认问题

| # | 问题 | 建议默认 | 需谁确认 |
|---|---|---|---|
| Q1 | PG 客户端最终选型是否已定为 `pg` Pool？ | 是 | 架构 Day 2 |
| Q2 | admin 鉴权复用现有 JWT role 还是独立 internal token？ | 复用 `role=admin` | 你 |
| Q3 | history 是否 Phase 1 必须持久化到 PG？ | 否，内存即可 | 你 |
| Q4 | 是否需要 `/api/pool/status` 纳入 LMS/公开路由白名单？ | **否** | 安全 |
| Q5 | 采样 30s 是否满足排查需求？ | 30s 默认，可配置 | 你 |
| Q6 | 是否与「课纲连接池演示」共用数据模型？ | Phase 1 否，预留字段 | 产品远期 |

---

## 9. 三种理解方向（模板要求）

| 方向 | 描述 | 是否采用 |
|---|---|---|
| **A. 运维可观测 API** | 仅 apps/api 内部诊断 PG/Redis 池 | ✅ **Phase 1 采用** |
| **B. 课纲可视化演示** | 教师课堂演示连接池原理动画 | ⏳ 远期；本 API 可_feed 数据 |
| **C. db-engine 沙箱监控** | 监控 Docker 内 MySQL/PG 教学沙箱 | ⏳ P2；Phase 1 返回 not_implemented |

---

## 10. AI 辅助开发过程记录

| 步骤 | 人工做法 | AI 辅助 | 校验点 |
|---|---|---|---|
| 读原始需求 | 自己列 bullet | 对齐 architecture 中 api/infra 约束 | 是否偏离主产品 |
| 写用户故事 | 从教师场景出发 | 提醒区分 ops vs 课堂用户 | US-4 标为远期 |
| 功能优先级 | 全做 P0 | 拆 P0/P1/P2，沙箱/Prometheus 后置 | Phase 1 可交付 |
| 验收标准 | 模糊「能看就行」 | 量化采样点数、并发测试 | 必须可自动化 |
| 待确认 | 跳过 | 列出 Q1–Q6 | **你逐项确认** |

### 哪些地方有效

- 快速对齐 architecture 已有模块名（Fastify、BullMQ、PostgreSQL）
- 自动区分 Phase 1 vs 远期课纲演示，避免范围膨胀
- 验收标准可直接变成 Day 3 测试用例

### 哪些地方需人工修正

- **Q2 鉴权策略** — 必须你定，AI 不能假设学校环境
- **PG 客户端选型** — 取决于 monorepo 初始化时的实际选择
- 「连接池监控」名称易与课纲演示混淆 — 文档中已用 US-4 和三种理解方向澄清

### 可复用经验

> 增量 API 需求澄清时，先写 **「不在范围内」** 和 **「三种理解方向」**，再写功能清单，能有效防止 DB Demo Studio 这类大项目范围膨胀。

---

## 11. 下一步（Day 2 → Day 3）

1. **Day 2**：用 `prompts/architecture.md` 细化路由、采样器、鉴权 middleware 设计  
2. **Day 3**：在 `apps/api` 脚手架中实现 `GET /status` + 采样器 + 测试  
3. **Git**：`git add` 本文件 → `commit -m "docs: 连接池监控 API 需求澄清"`

---

## 参考资料

- [`02_DB_Demo_Studio/docs/architecture.md`](../docs/architecture.md)
- [`00_Notes/requirements/db_demo_video_requirements.md`](../../00_Notes/requirements/db_demo_video_requirements.md)
- [`01_AI_Dev_Workflow_Kit/prompts/requirements.md`](../../01_AI_Dev_Workflow_Kit/prompts/requirements.md)
