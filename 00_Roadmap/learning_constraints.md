# 学习约束与工具配置

> 最后更新：2026-05-27  
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
| Phase 1 | AI Dev Workflow Kit | Code Review、Prompt 实战 |
| Phase 2 | Paper RAG Assistant | Embedding 可选 DeepSeek；生成用 deepseek-chat |
| Phase 3+ | MCP / Agent / Research | 统一 DeepSeek |

> Phase 2 Embedding 若 DeepSeek 不支持，可单独使用本地 embedding 模型，但**文本生成**仍用 DeepSeek。

---

## Git 提交规范

- 每日学习结束至少 1 次 commit
- commit message 格式：`feat:` / `log:` / `docs:` + 简短说明
- 敏感文件不进 git：`.env`、密钥、个人身份信息

---

## 相关文件

- 示例配置：`01_AI_Dev_Workflow_Kit/.env.example`
- 审查脚本：`01_AI_Dev_Workflow_Kit/scripts/ai_commit_review.py`
