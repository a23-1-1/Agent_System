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
| | | | |

---

## 迭代笔记
