# 需求澄清 — ai_commit_review 接入 DeepSeek API

> 生成时间：2026-05-27  
> 方式：使用 `prompts/requirements.md` 模板  
> 状态：**已澄清，可进入编码**

---

## 原始需求

给 `ai_commit_review.py` 接入 DeepSeek API，读取 git diff 生成 Code Review 报告。

## 现有上下文

- 脚本路径：`01_AI_Dev_Workflow_Kit/scripts/ai_commit_review.py`
- 已有能力：读取 staged / unstaged / 指定 commit 的 git diff，输出占位报告到 `logs/`
- Review Prompt：`prompts/code_review.md`（含 P0-P3 分级模板）
- Git 根目录：`Agent_System/`（脚本在子目录，diff 从父目录跑）
- `.gitignore` 已忽略 `.env`

---

## 1. 需求摘要

在现有 `ai_commit_review.py` 占位逻辑上，接入 **DeepSeek OpenAI 兼容 API**，将 git diff 与 `code_review.md` 模板组合后发送给 LLM，生成 **P0-P3 分级** 的 Markdown Code Review 报告并保存到 `logs/`。

---

## 2. 用户故事

- **As a** 日常开发者  
- **I want** 运行一条命令就能让 AI 审查我的 git diff  
- **So that** 提交前快速发现 P0/P1 问题，减少人工逐行 review 时间

---

## 3. 功能点清单

| # | 功能 | 优先级 |
|---|---|:---:|
| F1 | 从环境变量读取 `DEEPSEEK_API_KEY`（可选 `DEEPSEEK_BASE_URL`、`DEEPSEEK_MODEL`） | P0 |
| F2 | 读取 `prompts/code_review.md` 作为 system prompt | P0 |
| F3 | 将 git diff 作为 user message 发送给 DeepSeek API | P0 |
| F4 | 解析 LLM 响应，生成含 P0-P3 分级的 Markdown 报告 | P0 |
| F5 | 报告写入 `logs/review_YYYYMMDD_HHMMSS.md`（保留 `--output`） | P0 |
| F6 | diff 过大时截断（如 >8000 字符）并在报告中注明 | P1 |
| F7 | API 失败时打印清晰错误（缺 Key、网络、限流） | P1 |
| F8 | 新增 `.env.example` 和 `requirements.txt` | P1 |
| F9 | 保留现有 CLI：`--unstaged`、`--commit`、`--output` | P0 |

---

## 4. 边界条件与异常场景

| 场景 | 期望行为 |
|---|---|
| 无 diff（空变更） | 打印 `No changes to review.`，退出码 0 |
| 未配置 API Key | 报错提示复制 `.env.example` → `.env` |
| diff 超过 token 限制 | 截断 diff + 报告注明「已截断」 |
| API 超时 / 5xx | 打印错误信息，退出码非 0 |
| 不在 git 仓库内 | 现有 git diff 错误提示保留 |
| LLM 返回非 Markdown | 原样写入报告，不强制解析 |

---

## 5. 验收标准（可测试）

- [ ] `pip install -r requirements.txt` 成功
- [ ] 复制 `.env.example` 为 `.env` 并填入 DeepSeek Key 后，脚本能运行
- [ ] `python scripts/ai_commit_review.py --unstaged` 在有变更时生成报告
- [ ] 报告 **不含** `DRAFT — LLM not connected yet`
- [ ] 报告包含 **P0 / P1 / P2 / P3** 章节（或 LLM 明确 LGTM）
- [ ] `git status` 中 **不出现** `.env`
- [ ] 现有三个 CLI 模式（默认 staged / `--unstaged` / `--commit`）均可用

---

## 6. 不在范围内

- 不做 Web UI
- 不做多轮对话 / 自动修复代码
- 不做 GitHub PR 自动评论
- 不做单元测试框架（Week 1 先跑通 MVP）
- 不支持非 DeepSeek 的多 Provider 抽象（后续迭代）

---

## 7. 技术约束与依赖

| 项 | 选择 |
|---|---|
| API | DeepSeek（OpenAI 兼容） |
| Base URL | `https://api.deepseek.com`（默认） |
| Model | `deepseek-chat`（默认，可用 env 覆盖） |
| Python 包 | `openai`（官方 SDK，兼容 DeepSeek） |
| 配置 | `python-dotenv` 可选；至少支持 os.environ |
| Python | 3.10+（现有脚本用 `str \| None` 类型注解） |

**`.env.example` 示例：**
```env
DEEPSEEK_API_KEY=sk-your-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

---

## 8. 待确认问题

| # | 问题 | 决定 |
|---|---|---|
| Q1 | 用哪个 API？ | ✅ **DeepSeek** |
| Q2 | 用哪个模型？ | ✅ **deepseek-chat**（可 env 覆盖） |
| Q3 | Key 放哪？ | ✅ `.env` 本地，不进 git |
| Q4 | diff 截断长度？ | 建议 **8000 字符**（与占位版一致） |

---

## 下一步（编码）

在 Cursor 里说：

> 按 `logs/2026-05-27_ai_commit_review_requirements.md` 实现 DeepSeek 接入

或直接让我现在帮你写代码。
