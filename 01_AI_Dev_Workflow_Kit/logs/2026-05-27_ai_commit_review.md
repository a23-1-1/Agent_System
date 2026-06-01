# AI 辅助开发使用记录 — ai_commit_review 接入 DeepSeek

> 路径：`01_AI_Dev_Workflow_Kit/logs/2026-05-27_ai_commit_review.md`

---

## 日期

2026-05-27

## 任务

给 `scripts/ai_commit_review.py` 接入 DeepSeek API，读取 git diff 生成 Code Review 报告。

## 我自己原本会怎么做

手动 `git diff`，逐文件看变更，凭经验找 bug 和风格问题，大约 20-30 分钟；大 diff 容易遗漏边界问题。

## AI 帮我做了什么

1. 用 `prompts/requirements.md` 模板澄清需求，生成结构化功能清单和验收标准
2. Cursor Agent 实现 DeepSeek API 接入、diff 截断、错误处理
3. 补充 Docker 运行方式和 README 文档
4. 跑脚本自动生成 P0-P3 分级审查报告

## 哪些地方有效

- 需求模板帮想全了 `.env.example`、diff 截断、CLI 参数保留等边界
- Code Review 报告按 P0-P3 分级，比人工初筛更快
- 脚本可复用，后续每次 commit 前都能跑

## 哪些地方无效

- 初期不清楚在哪个文件写什么，需要模板引导
- diff 超过 8000 字符会截断，审查范围不完整（报告中有说明）

## 我如何修正 AI 输出

- 明确 API 策略：统一 DeepSeek，写入 `learning_constraints.md`
- 修正 `.env.example` 为占位符，真实 Key 只放本地 `.env`

## 可复用经验

- **先需求澄清再编码**，比直接让 AI 改文件少返工
- **每条实战都写 logs/**，Phase 1 验收靠记录数量
- **API Key 绝不进 git**

## 关联文件

- 需求澄清：`logs/2026-05-27_ai_commit_review_requirements.md`
- 审查报告：`logs/review_20260601_012246.md`
