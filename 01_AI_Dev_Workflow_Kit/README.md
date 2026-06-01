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
- [x] 5 个 Prompt 模板骨架（requirements / architecture / code_review / debug / refactor）
- [ ] AI 开发工作流文档定稿
- [x] 5 个 AI 编程场景分析（Day 1 已填个人案例）
- [x] `ai_commit_review.py` — DeepSeek Code Review 已跑通
- [ ] 至少 5 条真实使用记录（当前 1/5）

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

### 本地运行

```bash
cd 01_AI_Dev_Workflow_Kit
cp .env.example .env   # 填入 DEEPSEEK_API_KEY
pip install -r requirements.txt

# 审查 staged changes
python scripts/ai_commit_review.py

# 审查 unstaged / 指定 commit
python scripts/ai_commit_review.py --unstaged
python scripts/ai_commit_review.py --commit HEAD~1
```

### Docker 运行（无需本地 pip）

在 `01_AI_Dev_Workflow_Kit/` 目录下：

```bash
cp .env.example .env   # 填入 DEEPSEEK_API_KEY

# 构建镜像
docker compose build

# 审查 staged changes（默认）
docker compose run --rm ai-commit-review

# 传递 CLI 参数
docker compose run --rm ai-commit-review --unstaged
docker compose run --rm ai-commit-review --commit HEAD~1
docker compose run --rm ai-commit-review --output logs/my_review.md
```

容器会将上级目录 `Agent_System/` 挂载到 `/workspace`，脚本在此目录执行 `git diff`；报告写入 `logs/`（宿主机同步可见）。

**Windows 注意**：在 PowerShell 中于 `01_AI_Dev_Workflow_Kit` 运行上述命令即可；需已安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/) 并启用 WSL2 后端。若 `.env` 缺失，`docker compose` 会报错，请先复制 `.env.example`。

### 手动使用 Prompt 模板

```bash
# 复制 prompts/ 下的模板到 Cursor / Claude，填入具体上下文
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

- diff 超过 8000 字符会截断，审查范围可能不完整
- scenarios.md 格式待 Day 2 统一整理

---

## 9. API 策略

本仓库 LLM 调用统一使用 **DeepSeek API**。配置见 `.env.example` 与 `00_Roadmap/learning_constraints.md`。

---

## 10. 后续计划

- Week 2：完成编码闭环实战
- Week 3：Debug 与 Refactor 模板实战
- Week 4：阶段总结 + 文章草稿

---

## 10. 学习记录

- 2026-05-27：项目启动；ai_commit_review 接入 DeepSeek；第 1 条使用记录
