# Git 管理学习历程 — 操作指南

> 用 Git 把「学习过程」变成「可追踪、可展示、可复盘」的资产。

---

## 1. 为什么用 Git 管理学学习

| 普通文件夹 | Git 管理 |
|---|---|
| 改了什么不知道 | 每次提交有 message，可追溯 |
| 实验失败无法回退 | `git checkout` 回到上一个版本 |
| 简历说不清贡献 | commit 历史 = 真实开发轨迹 |
| 项目无法展示 | push 到 GitHub = 公开作品集 |

**核心原则：一个 commit = 一个可见产出。**

---

## 2. 一次性初始化（只做一次）

在 PowerShell 中执行：

```powershell
cd d:\AI_Projects\01_Research\Agent_System

# 初始化仓库
git init

# 配置用户信息（如果还没配过）
git config user.name "你的名字"
git config user.email "你的邮箱"

# 首次提交：学习管理系统骨架
git add .
git commit -m "init: 学习管理系统 + Phase1 AI Dev Workflow Kit 骨架"

# （可选）关联 GitHub 远程仓库
# 先在 GitHub 创建空仓库 Agent_System，然后：
git remote add origin https://github.com/你的用户名/Agent_System.git
git branch -M main
git push -u origin main
```

---

## 3. 目录与分支策略

### 3.1 目录 = 项目模块（不用多分支）

学习仓库用 **单分支 `main`** + 目录区分项目，简单清晰：

```text
Agent_System/          ← 一个 Git 仓库
├── 00_Roadmap/        ← 计划与看板
├── 00_Learning_Logs/  ← 每日/每周日志
├── 00_Notes/          ← 概念笔记、论文笔记
├── 00_Portfolio/      ← 简历、面试材料
├── 01_AI_Dev_Workflow_Kit/
├── 06_RAG_Research_Assistant/   ← M1 创建
├── 07_MCP_Server/               ← M2 创建
├── 08_Mini_Agent_Framework/     ← M2 创建
└── 09_Coding_Agent/             ← M3 创建
```

**不需要**为每个 Phase 开分支——你的 commit message 已经标记阶段。

### 3.2 什么时候开分支

只在以下情况开分支：

| 场景 | 分支名示例 |
|---|---|
| 实验性重构，可能失败 | `exp/rag-chunk-v2` |
| 同时做两个互不干扰的功能 | `feat/mcp-git-tool` |
| 写文章/文档大改 | `docs/rag-evaluation-report` |

实验成功后 merge 回 main；失败就 delete 分支，main 不受影响。

---

## 4. Commit Message 规范

用 **类型前缀** 标记每次提交的性质：

```text
类型: 简短描述（中文或英文均可）

类型列表：
  init    — 初始化项目/目录
  log     — 学习日志（daily/weekly/monthly）
  note    — 概念笔记、论文笔记
  feat    — 新功能
  fix     — Bug 修复
  exp     — 实验记录与结果
  docs    — README、文档、文章
  refactor— 重构
  chore   — 配置、gitignore 等杂项
```

### 示例

```text
log: 2026-05-27 daily — Phase1 Day1 系统搭建
note: Agent 概念卡片 — 补充 ReAct 理解
feat: RAG PDF 解析模块 — PyMuPDF 提取标题/摘要/正文
exp: chunk size 对比 — 512 vs 1024 vs 2048 召回率
docs: Paper RAG README — 添加快速开始和评估结果
feat: MCP Server — 实现 search_files 和 read_file
feat: mini-agent core loop — Observe/Think/Act 基础循环
```

**规则：每天至少 1 个 commit**（可以是 log 或 note，不一定写代码）。

---

## 5. 每日 Git 工作流（5 分钟）

```text
开始学习前：
  git pull                    # 如果有多设备同步

学习过程中：
  随时保存文件（正常编辑）

学习结束前（Daily Git Ritual）：
  1. 打开 00_Learning_Logs/daily/今天.md，补全今日产出
  2. git status               # 看改了什么
  3. git add 相关文件
  4. git commit -m "log: YYYY-MM-DD daily — 一句话摘要"
  5. （如果写了代码）再 git add + commit -m "feat: ..."
```

### 一天多个 commit 的典型节奏

```text
09:00  note: 读 MCP 文档 — 更新 mcp.md
14:00  feat: MCP Server 脚手架 — stdio transport
17:00  log: 2026-05-28 daily — MCP 前 3 个 tool 完成
17:05  exp: tool schema 描述对比 — 详细 vs 简洁
```

---

## 6. 每周 Git 工作流

```text
周日复盘时：
  1. 写 00_Learning_Logs/weekly/YYYY-WXX.md
  2. git add 00_Learning_Logs/weekly/ + 本周改动
  3. git commit -m "log: 2026-W22 weekly review — M1W1 完成"
  4. 更新 00_Roadmap/project_matrix.md 状态
  5. git commit -m "docs: 更新 project_matrix — Paper RAG 进入 Building"
  6. git push                     # 同步到 GitHub
```

---

## 7. 项目里程碑 Tag

每个项目完成时打 tag，方便简历和 Demo 引用：

```powershell
# Paper RAG v1 完成
git tag -a v0.1-rag -m "Paper RAG Assistant v1 — PDF 问答 + 引用定位"

# Mini Agent Framework 完成
git tag -a v0.1-agent -m "Mini Agent Framework v1 — Loop + Tools + Trace"

# 3 个月总完成
git tag -a v1.0-portfolio -m "3-month portfolio complete"

# 推送 tag
git push origin --tags
```

简历里可以写：`github.com/你/Agent_System/tree/v0.1-agent`

---

## 8. GitHub 展示建议

### 仓库结构

- **主仓库**：`Agent_System`（mono-repo，所有项目在一个仓库）
- 或 **拆分**：每个项目独立仓库（更适合求职展示）

**推荐 mono-repo**（你当前结构），因为：
- 学习日志和项目在一起，commit 历史完整
- 一个链接展示全部成长轨迹

### GitHub 设置

1. 仓库设为 **Public**
2. README.md 写 Portfolio 首页（项目矩阵 + Demo 链接）
3. Pin 这个仓库到你的 GitHub Profile
4. 用 GitHub Releases 配合 tag 发布里程碑

### 根目录 README 建议内容

```markdown
# Agent System — AI 学习作品集

> 3 个月项目驱动学习：RAG → MCP → Agent → Coding Agent

## 项目

| 项目 | 状态 | Demo |
|------|------|------|
| AI Dev Workflow Kit | Done | ... |
| Paper RAG Assistant | Done | ... |
| ... | | |

## 学习轨迹

- 60+ commits, 30+ daily logs
- 标签：v0.1-rag, v0.1-agent, v1.0-portfolio
```

---

## 9. 什么该提交、什么不该提交

### 应该提交

- 代码、Prompt 模板、脚本
- 学习日志、笔记、实验记录
- README、架构图（markdown/mermaid）
- 配置文件（不含密钥）
- 小型样例数据（< 1MB）

### 不要提交（已在 .gitignore）

- `.env`、API Key
- 大型 PDF 论文库
- 向量数据库文件
- `__pycache__/`、`.venv/`
- 模型权重文件

### 论文 PDF 怎么处理

```text
data/
  papers/           ← .gitignore 忽略
  samples/          ← 提交 1-2 篇样例 PDF 用于复现
  README.md         ← 说明如何获取完整数据集
```

---

## 10. 常用命令速查

```powershell
# 查看状态
git status
git log --oneline -20          # 最近 20 条提交
git log --oneline --grep="log" # 只看学习日志提交

# 提交
git add 文件或目录
git commit -m "type: 描述"

# 撤销（学习实验经常用到）
git checkout -- 文件            # 丢弃未提交的修改
git reset HEAD~1               # 撤销最后一次 commit（保留文件改动）

# 同步
git push
git pull

# 查看某天的学习产出
git log --after="2026-05-27" --before="2026-05-28" --oneline

# 统计学习 commit 数（成就感来源）
git log --oneline | Measure-Object -Line
```

---

## 11. 学习历程可视化

3 个月后你可以：

```powershell
# 提交热力图（GitHub 自动生成）

# 按类型统计
git log --oneline --grep="^feat" | Measure-Object   # 功能提交数
git log --oneline --grep="^log"  | Measure-Object   # 日志提交数
git log --oneline --grep="^exp"  | Measure-Object   # 实验提交数
git log --oneline --grep="^note" | Measure-Object   # 笔记提交数
```

面试时可以展示：**「这是我的 3 个月 commit 历史，120+ 次提交，涵盖 5 个项目。」**

---

## 12. 今天立即执行

```powershell
cd d:\AI_Projects\01_Research\Agent_System
git init
git add .
git commit -m "init: 学习管理系统 + 3个月计划 + Phase1 Workflow Kit 骨架"
```

然后每天结束前：

```powershell
git add 00_Learning_Logs/daily/今天.md
git commit -m "log: 今天 daily — 一句话摘要"
git push
```

这就是你的 Git 学习管理系统。
