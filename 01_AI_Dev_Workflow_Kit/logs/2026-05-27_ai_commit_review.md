# AI 辅助开发使用记录 — ai_commit_review 接入 LLM

> **这是模板文件。** 实战完成后，把每节「（待填写）」改成你的真实经历。
> 路径：`01_AI_Dev_Workflow_Kit/logs/2026-05-27_ai_commit_review.md`

---

## 日期

2026-05-27

## 任务

给 `scripts/ai_commit_review.py` 接入 LLM API，读取 git diff 生成 Code Review 报告。

## 我自己原本会怎么做

（待填写：2-3 句。例：手动 `git diff`，逐文件看变更，凭经验找 bug 和风格问题，大约 20 分钟。）
手动 `git diff`，逐文件看变更，凭经验找 bug 和风格问题，大约 20 分钟。保证代码能跑通，在后续出现bug时才可能修复

## AI 帮我做了什么

（待填写：2-3 句。例：用 requirements 模板澄清需求；让 Cursor 写接入 Deepseek 的代码；跑脚本自动生成报告。）
用 requirements 模板澄清需求；让 Cursor 写接入 Deepseek 的代码；跑脚本自动生成报告。
## 哪些地方有效

（待填写： bullet 列表。例：- 需求模板帮我想到了 .env.example 和 diff 截断）
需求模板帮我想到了 .env.example 和 diff 截断

## 哪些地方无效

（待填写： bullet 列表。例：- AI 第一次漏了 base_url 配置）
AI 第一次漏了 base_url 配置
未创建.env文件

## 我如何修正 AI 输出

（待填写：1-2 句。例：补上了 OPENAI_BASE_URL，重新跑脚本验证。）
补上了 OPENAI_BASE_URL，重新跑脚本验证。
我自己创建.env

## 可复用经验

（待填写：1-2 条。例：先写需求再写代码，比直接让 AI 改文件少返工。）
先写需求再写代码，比直接让 AI 改文件少返工。还要让ai进行代码审查

## 关联文件

- 需求澄清输出：（如有）`logs/2026-05-27_ai_commit_review_requirements.md`
- 审查报告输出：`logs/review_YYYYMMDD_HHMMSS.md`（脚本运行后自动生成）
