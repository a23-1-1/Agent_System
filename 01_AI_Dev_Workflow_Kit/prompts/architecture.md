# Prompt: 架构设计

## 使用场景

新模块、新服务或重大重构前，生成架构方案对比和模块划分。

---

## 模板

```markdown
你是一个系统架构师，请帮我设计以下功能的架构方案。

## 需求摘要

{{粘贴澄清后的需求，或 requirements.md 的输出}}

这是requirements.md 的输出D:\AI_Projects\01_Research\Agent_System\00_Notes\requirements\db_demo_video_requirements.md
设计这个功能的架构方案
## 现有系统上下文

- 技术栈：
- 相关模块：
- 约束：
使用D:\AI_Projects\01_Research\Agent_System\00_Notes\requirements\db_demo_video_requirements.md的要求

## 请输出

1. **方案 A（推荐）**
   - 模块划分
   - 核心接口定义
   - 数据流
   - 优点 / 缺点

2. **方案 B（备选）**
   - 同上结构

3. **方案对比表**（维度：复杂度、可扩展性、维护成本、风险）

4. **推荐方案及理由**

5. **实施步骤**（分阶段，每阶段可独立交付）

6. **风险与缓解措施**

## 要求

- 优先考虑与现有代码的兼容性
- 接口设计遵循项目现有命名和风格
- 不要过度设计，标注 YAGNI 部分
```

---

## 使用记录

| 日期 | 任务 | 效果 | 改进 |
|---|---|---|---|
| 2026-06-01 | DB Demo Studio：`packages/ai-orchestrator/` 架构设计 | 有效。把总架构里的 Agent 编排模块细化为 `orchestrator / session-store / agent-runner / tool-router / policies / stream-events`，明确了 SSE 事件、工具调用、单步重写和 grounding 守卫 | 下次填 prompt 时要明确「只设计某个模块」，避免重复输出整个系统架构；输出文件命名带 Day + 日期 |

---

## 迭代笔记

- 2026-06-01：本模板适合做“模块级架构细化”，但输入上下文必须控制范围。例如今天聚焦 `packages/ai-orchestrator/`，而不是重新设计整个 DB Demo Studio。
- 模板中建议新增一项「目标粒度」：系统级 / 模块级 / 接口级 / PoC 级。这样能减少 AI 过度设计。
- 对 Agent 类模块，必须额外要求输出：会话状态、工具路由、SSE 事件、超时/防循环、grounding 校验。
