# PoC #1 需求澄清 — DemoPackage Schema

> 日期：2026-06-01  
> 使用 Prompt：`01_AI_Dev_Workflow_Kit/prompts/requirements.md`  
> 参考文档：`02_DB_Demo_Studio/docs/architecture.md`  
> 项目：DB Demo Studio Phase 1 PoC #1

---

## 需求摘要

为 DB Demo Studio 定义 DemoPackage JSON Schema，并手写一个 JOIN 查询的 5 步演示样例 JSON，作为 Execution Player 的数据源。

## 用户故事

As a **数据库课教师**  
I want **AI 生成一个结构化的分步演示 JSON**  
So that **我可以在 Execution Player 中逐句播放 SQL 执行过程**

## 功能点清单

### P0（必须有）
- [ ] 定义 `DemoPackage` 顶层字段：id、title、steps、metadata
- [ ] 定义 `DemoStep` 字段：id、order、workflowPhase、narration、visuals、groundingRef
- [ ] 定义 `workflowPhase` 枚举：lex / parse / optimize / plan / execute / result / concept
- [ ] 支持中英双语 narration（zh / en）
- [ ] 支持 playback 配置（默认步进时长、字幕）
- [ ] 手写 JOIN 样例 JSON ≥5 步，覆盖 ≥3 个 workflowPhase

### P1（应该有）
- [ ] 含 `workflowTrace` 可追溯 AI 生成链（workflowId、aiSessionId）
- [ ] 含 `engineCompare` 字段存储 MySQL / PostgreSQL EXPLAIN 对照
- [ ] metadata 记录 aiDraftVersion、teacherVersion、lastAiAction

### P2（可以有）
- [ ] Subtitles 字幕轨道定义
- [ ] VisualSpec 动画脚本占位

## 边界条件与异常场景

- 样例 JSON 的 workflowPhase 必须合法（在枚举中）
- groundingRef 可空（手动编写时），但 SQL 类步骤必须有 grounding 意图
- 单步 order 必须连续（1, 2, 3...），不能跳号
- narration 至少要有中文；英文可为空字符串

## 验收标准

1. `schema.json` 能通过 JSON Schema 基本校验
2. `examples/join-query.json` 包含 ≥5 步，且 step 数组不为空
3. 每个 step 都含 `workflowPhase` 字段，值取自枚举
4. DemoPackage 顶层含 `id`、`title.zh`、`title.en`
5. 至少包含 3 种不同的 workflowPhase（如 lex、plan、result）

## 不在范围内

- ❌ Player UI 实现（Day 4-5）
- ❌ 校验脚本编写（当前仅人工校验）
- ❌ TypeScript 类型定义（PoC 阶段用纯 JSON 即可）
- ❌ ai-orchestrator / ai-tools 模块代码

## 技术约束与依赖

- 纯 JSON，不依赖任何运行时
- 文件存于 `02_DB_Demo_Studio/packages/demo-schema/`
- 样例参考 `architecture.md` 中的 `DemoPackage` / `DemoStep` TypeScript 接口
- 遵循 DeepSeek API 序列化友好原则（无复杂嵌套循环）

## 待确认问题

1. 样例 JSON 的 visuals（动画脚本）字段 PoC 阶段填空对象还是省略？
2. workflowTrace 在手动 JSON 阶段是否需要保留？
3. JOIN 样例用 INNER JOIN 还是 LEFT JOIN 作为默认？
4. 5 步分别对应哪 5 个 phase？（推荐：lex → parse → plan → execute → result）

---

## 使用记录

| 日期 | 任务 | 效果 | 改进 |
|---|---|---|---|
| 2026-06-01 | PoC #1 DemoPackage Schema 需求澄清 | 明确了字段范围 / 验收标准 / 不做的范围 | — |
