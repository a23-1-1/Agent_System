# 学习约束与工具配置

> 最后更新：2026-06-01  
> 本文件记录个人学习过程中的固定约束，所有 Phase 项目均遵守。

---

## LLM API 策略

**本仓库所有需要调用 LLM 的脚本、实验、Demo，统一使用 DeepSeek API。**

| 配置项 | 值 |
|---|---|
| Provider | DeepSeek（OpenAI 兼容接口） |
| Base URL | `https://api.deepseek.com` |
| 默认模型 | `deepseek-chat` |
| SDK | `openai` Python 包 |
| 密钥存放 | 本地 `.env`，**绝不提交 git** |

### 环境变量规范

```env
DEEPSEEK_API_KEY=sk-your-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

### 安全规则

1. `.env` 已在 `.gitignore` 中忽略
2. `.env.example` 只放占位符，**禁止写入真实 Key**
3. commit 前检查：`git diff --cached | findstr /i "sk-"`（PowerShell 可用 `Select-String`）
4. 日志、Daily Log、截图中不得出现完整 API Key

### 适用范围

| Phase | 项目 | LLM 用途 |
|---|---|---|
| Phase 1 | **DB Demo Studio**（主）+ AI Dev Workflow Kit（模板/审查） | 需求/架构/编码/测试；Code Review 可选脚本 |
| Phase 2 | Paper RAG Assistant | Embedding 可选 DeepSeek；生成用 deepseek-chat |
| Phase 3+ | MCP / Agent / Research | 统一 DeepSeek |

> Phase 2 Embedding 若 DeepSeek 不支持，可单独使用本地 embedding 模型，但**文本生成**仍用 DeepSeek。

---

## Git 提交规范

- 每日学习结束至少 1 次 commit
- commit message 格式：`feat:` / `log:` / `docs:` + 简短说明
- 敏感文件不进 git：`.env`、密钥、个人身份信息

---

## 每日文件命名规范

每日新建的学习文件，文件名须带 **Day 序号 + 日期**，避免混淆：

| 类型 | 命名格式 | 存放目录 | 示例 |
|---|---|---|---|
| 当日任务指南 | `day{N}_{YYYY-MM-DD}_guide.md` | `00_Roadmap/` | `day2_2026-05-28_guide.md` |
| 当日流程复盘 | `day{N}_{YYYY-MM-DD}_workflow.md` | `00_Roadmap/` | `day1_2026-05-27_workflow.md` |
| Daily Log | `{YYYY-MM-DD}.md` | `00_Learning_Logs/daily/` | `2026-05-28.md` |
| 实战 logs（Phase 1 优先） | `{YYYY-MM-DD}_{任务简述}.md` | `02_DB_Demo_Studio/logs/` | `2026-06-01_poc_player_requirements.md` |
| 实战 logs（Kit 侧车） | `{YYYY-MM-DD}_{任务简述}.md` | `01_AI_Dev_Workflow_Kit/logs/` | `2026-05-27_ai_commit_review.md` |

**规则：**
- `{N}` = Day 1、Day 2 …（与 weekly_plan 一致）
- `{YYYY-MM-DD}` = 该 Day 对应日历日期
- 指南（guide）= 当天要做的事；复盘（workflow）= 当天做完后的流程归档

**W1 文件索引：**

| Day | 日期 | 指南 | 复盘/日志 |
|---|---|---|---|
| Day 1 | 2026-05-27 | `day1_2026-05-27_guide.md` / `day1_guide.md` | `day1_2026-05-27_workflow.md` / `2026-05-27.md` |
| Day 2 | 2026-05-28 | `day2_2026-05-28_guide.md` | `2026-05-28.md` |
| Day 3 | 2026-06-01 | `day3_2026-06-01_guide.md` | `2026-06-01.md` |
| Day 4 | 2026-06-02 | `day4_2026-06-02_guide.md` | `2026-06-02.md` |
| Day 5 | — | — | — |


## 相关文件

- 示例配置：`01_AI_Dev_Workflow_Kit/.env.example`
- Phase 1 实战代码库：`02_DB_Demo_Studio/`
- 审查脚本（可选）：`01_AI_Dev_Workflow_Kit/scripts/ai_commit_review.py`
