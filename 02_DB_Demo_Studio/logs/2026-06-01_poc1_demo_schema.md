# PoC #1 使用记录 — DemoPackage Schema + 样例 + 校验

> 日期：2026-06-01  
> 任务：PoC #1 编码 — DemoPackage JSON Schema 定义、JOIN 5 步样例手写、校验脚本  
> 项目：`02_DB_Demo_Studio/packages/demo-schema/`  
> 参考：`02_DB_Demo_Studio/docs/architecture.md`  
> AI 工具：Claude Code  
> 耗时：约 40 min

---

## 我自己原本会怎么做

手动定义 JSON 结构，直接在 TS 里写 interface，然后硬编码一个测试数据就跳过校验。不会想到做独立的 JSON Schema 和校验脚本。

## AI 帮我做了什么

1. **结构设计**：基于 architecture.md 中的 `DemoPackage` / `DemoStep` TypeScript 接口，生成了完整的 JSON Schema（含字段约束、枚举校验、pattern、description）
2. **样例填充**：生成 5 步 JOIN 教学讲解词，每步 100-200 字中英双语，覆盖 lex/parse/plan/execute/result 完整工作流
3. **校验脚本**：生成独立的 Python 校验器，包含：必填字段检查、order 连续性、workflowPhase 枚举、narration 非空、metadata 版本号校验、playback 值域检查、批量扫描功能

## 哪些地方有效

- **Schema 生成**：直接用 architecture.md 的接口定义做 reference，输出完全对齐，节省了手动翻译 TS → JSON Schema 的时间
- **校验脚本深度**：不是简单的 "is valid JSON"，而是逐字段检查业务规则（唯一 phase ≥3、step 数量上限 100、order 连续不跳号）
- **样例 JSON 的故事线**：5 步讲解词有从浅到深的递进，适合教学演示场景

## 哪些地方无效

- 校验脚本的 GBK 兼容性问题（Windows 终端打印 emoji 时报错），需要手动去除 ✅/❌ 字符改用 `[OK]/[ERR]`

## 我如何修正 AI 输出

- 将所有 emoji（✅ ❌）替换为纯文本 `[OK] [ERR]`
- 调整了 narration 讲解词的学术准确性（原文缺失 grounding 说明，补充了 grounding 约束的说明）

## 可复用经验

1. PoC 阶段纯 JSON 比 TS interface 更适合快速迭代——不需要编译工具链，可直接运行
2. JSON Schema 的 `description` 字段 + `example` 是重要的自文档手段，未来 AI 生成时会直接引用这些元数据
3. 校验脚本的批量扫描模式（`validate.py examples/*.json`）会让 Day 4-5 的 Player 开发调试更高效

---

## 产出文件

| 文件 | 说明 |
|---|---|
| `packages/demo-schema/schema.json` | DemoPackage JSON Schema（Draft-07） |
| `packages/demo-schema/examples/join-query.json` | INNER JOIN 5 步演示样例 |
| `packages/demo-schema/validate.py` | 独立校验脚本 |

## 校验结果

```text
[OK] join-query.json: 5 步, phases=[execute, lex, parse, plan, result]
结果: 1 OK, 0 FAILED
```

---

## Code Review 审查记录

> 方式：手动对照 architecture.md 约束 + code_review.md 模板  
> 审查范围：`schema.json` + `examples/join-query.json` + `validate.py`  
> 时间：2026-06-01

### P0 — 必须修复

**无。** 三个文件功能完整，无 Bug、安全漏洞或数据丢失风险。

### P1 — 强烈建议修复

| # | 问题 | 文件 | 说明 |
|---|---|---|---|
| 1 | **step_1 的 groundingRef 为 null**，但 SQL 类的 lex 步应该有 grounding | `join-query.json:54` | 虽然 lex 是词法分析阶段，但 schema 要求 SQL 类至少 plan/execute 步有 groundingRef，手动 JSON 可接受 null，但建议后面 Player 阶段增加「未 grounding 的 SQL 步骤标记」 |
| 2 | **schema 中的 `groundingRef` 为可选字段（无 required）** | `schema.json` | architecture.md 写明了"SQL 类 plan/execute 步须有 groundingRef"，但 schema 没有用 `if/then` 条件校验（Draft-07 不支持条件 required），PoC 阶段可接受，但 Phase 1 正式版需要考虑 |

### P2 — 建议改进

| # | 问题 | 文件 | 说明 |
|---|---|---|---|
| 1 | `validate.py` 没有校验 `title.en` 非空（只检查了 `zh`）| `validate.py:122-126` | architecture 要求双语，但校验只强校验了中文。建议增加 `if title_en is empty → warning` |
| 2 | `join-query.json` 的 `optimize` phase 缺失 | `join-query.json` | 5 步覆盖了 lex/parse/plan/execute/result，跳过了 optimize。虽然 5 种不同 phase 已满足 ≥3 的验收要求，但作为教学演示，缺少 "优化器如何选择 JOIN 算法" 这一步是信息缺口 |
| 3 | `schema.json` 缺少 `DemoPackage` 的 `createdAt` / `updatedAt` 字段 | `schema.json` | 便于版本追踪和日志审计。PoC 可暂缓，但 Phase 1 正式版建议加 |

### P3 — 风格建议

| # | 问题 | 文件 | 说明 |
|---|---|---|---|
| 1 | `validate.py` 的 `VALID_PHASES` 枚举值分散在 `schema.json` 和 `validate.py` 两处 | 两个文件 | 未来应统一用 schema.json 作为单一真相源，validate.py 动态读取 schema 中的 enum |

### 约束检查清单

| 约束 | 是否合规 | 说明 |
|---|---|---|
| **DeepSeek-only** | ✅ | 本项目不涉及 LLM 调用，纯 JSON 无 Provider 依赖 |
| **双引擎 EXPLAIN** | ✅ | `engineCompare` 字段已定义，同时预留了 mysql/postgres 两个引擎的位置 |
| **EXPLAIN grounding** | ✅ | `groundingRef` 字段已定义，step_3 (plan) 和 step_4 (execute) 引用 `mysql_explain.node_001` |
| **workflowPhase 枚举合法** | ✅ | 5 步全部在 `[lex, parse, optimize, plan, execute, result]` 范围内 |
| **教学简化标注** | ⚠️ 未涉及 | 当前无引擎实际运行，不存在简化标注需求。Player 阶段需要考虑 |
| **敏感信息不提交** | ✅ | 无 API Key、密码、个人身份信息 |
