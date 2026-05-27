# AI Dev Workflow Kit

> Phase 1 项目：把 AI 接入日常开发流程，形成可复用的提示词模板和工作流规范。

---

## 1. 项目目标

- 建立个人 AI 辅助开发协议（需求、设计、编码、测试、审查、调试、重构）
- 沉淀可复用 Prompt 模板
- 提供 git diff 自动审查脚本
- 形成可展示的 GitHub 仓库和面试叙事

---

## 2. 核心功能

- [x] 项目骨架与 README
- [ ] 5 个 Prompt 模板（requirements / architecture / code_review / debug / refactor）
- [ ] AI 开发工作流文档
- [ ] 5 个 AI 编程场景分析
- [ ] `ai_commit_review.py` — 读取 git diff 生成审查报告
- [ ] 至少 5 条真实使用记录

---

## 3. 技术架构

```text
01_AI_Dev_Workflow_Kit/
  prompts/          # 提示词模板
  docs/             # 工作流文档与场景分析
  scripts/          # 自动化脚本
  logs/             # AI 辅助开发过程记录
  README.md
```

---

## 4. 快速开始

```bash
# 使用 git diff 审查（需配置 LLM API）
python scripts/ai_commit_review.py

# 或手动使用 prompts/ 下的模板
# 复制模板内容到 Cursor / Claude，填入具体上下文
```

---

## 5. 使用示例

1. 打开 `prompts/requirements.md`，复制模板到 Cursor
2. 填入你的功能需求，让 AI 生成结构化需求文档
3. 将 AI 输出保存到 `logs/` 目录
4. 在 Daily Log 中记录：有效/无效/修正方式

---

## 6. 关键设计

- **模板而非魔法**：Prompt 是可编辑的协议，不是一次性对话
- **记录驱动改进**：每次使用都记录效果，持续优化模板
- **场景优先**：从真实开发场景出发，而非抽象技巧

---

## 7. 实验与评估

| 指标 | 目标 |
|---|---|
| 真实使用记录 | >= 5 条 |
| Prompt 模板 | 5 个完整版 |
| 小功能闭环 | 1 个完整 commit |
| 3 分钟讲述 | 能讲清楚 AI 在开发流程中的作用 |

---

## 8. 已知问题

- `ai_commit_review.py` 尚未实现 LLM 调用（Week 1 Day 5 任务）

---

## 9. 后续计划

- Week 2：完成编码闭环实战
- Week 3：Debug 与 Refactor 模板实战
- Week 4：阶段总结 + 文章草稿

---

## 10. 学习记录

- 2026-05-27：项目启动，创建骨架
