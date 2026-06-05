# DB Demo Studio 项目审查与优化建议报告

审查日期：2026-06-02  
审查范围：
- `docs/requirements-spec.md`
- `docs/frontend-design.md`
- `apps/web` 前端实现
- `apps/api` 后端实现
- `packages/*` 核心 PoC 能力

## 1. 总体结论

DB Demo Studio 的产品方向是成立的：以 AI 对话作为入口，把数据库课程的知识讲解、原理演示、可视化、课堂播放、学生自学和测验闭环统一到一个教学演示工作台里。SQL 只是其中最典型的演示场景之一，`requirements-spec.md` 和 `frontend-design.md` 已经把 v5 的目标形态描述得比较完整，核心叙事也统一为“对话驱动的课程演示生产流水线”。

但当前仓库实现仍明显处在 Phase 1 PoC 阶段，和 v5 文档存在较大落差。最需要优先处理的是：

1. 修复源码中文乱码与 UI 文案损坏问题。
2. 收敛 v5 需求范围，明确 MVP、Beta、后续版本边界。
3. 将“思维链展示”改为“可审计执行轨迹/工具调用摘要”，避免暴露模型内部推理。
4. 统一 API 契约、数据模型和前端类型定义。
5. 重新设计教师工作台布局，让它更像高密度教学生产工具，而不是简单三栏拼装。
6. 补齐持久化、认证、权限、审计、错误恢复和导出链路。

## 2. 当前项目状态

### 2.1 已具备的能力

- 前端已使用 React + TypeScript + Vite + Tailwind CSS。
- 已有教师工作台、课堂页、学生页基础页面。
- 已有对话列表、聊天面板、FlowEditor、ExecutionPlayer、QuizPanel 等模块雏形。
- 后端已使用 FastAPI，包含 REST、SSE 和 WebSocket 入口。
- `packages/demo-schema`、`packages/db-engine`、`packages/execution-workflow`、`packages/ai-tools` 已形成 PoC 链路。
- WebSocket 已支持基础 `chat:message`、`conv:switch`、`player:seek` 等事件。

### 2.2 主要落差

| 领域 | 文档目标 | 当前实现 | 风险 |
|---|---|---|---|
| 多对话 | PG + Redis 持久化、快照、搜索 | 内存 dict + 部分 Redis cache | 重启丢数据，无法审计 |
| AI 编排 | Agent Runtime + MCP 工具层 | 直接调用本地 tools | 后续扩展成本高 |
| 前端体验 | AI 协作工作台 | 基础三栏布局 | 信息层级和生产效率不足 |
| 课堂同步 | Redis Pub/Sub + Room | 单进程内存 room | 多实例不可用 |
| 学生自适应 | 掌握度分析 + AI Tutor | 基础 quiz + 进度条 | 教学闭环未闭合 |
| 导出 | MP4/Mermaid/LTI | 文档中规划，代码未落地 | 核心交付物缺失 |
| API 契约 | `/api/v5/*` | `/api/*` | 文档与代码不一致 |
| 数据模型 | DemoPackage v5 | 当前仍混用 v4 字段 | 前后端类型漂移 |

## 3. 需求规格优化建议

### 3.1 需求需要分层，避免 v5 一次性过宽

当前 `requirements-spec.md` 同时包含多对话、AI Agent、MCP、双引擎 EXPLAIN、Mermaid、D3、B+树、事务模拟器、TTS、MP4、LMS、RAG、学生掌握度、教师风格学习等能力。作为愿景文档可以，但作为执行规格过宽。

建议拆成三层：

| 层级 | 建议范围 | 验收标准 |
|---|---|---|
| MVP | 任一知识点输入、演示模板选择、6 步讲解、对话精修、基础播放器、版本快照 | 教师能生成、编辑、播放、保存一节知识点演示 |
| Beta | 多对话持久化、Mermaid/树图可视化、课堂同步、基础测验、导出 HTML | 一门课可被复用、投屏、学生跟随 |
| V1 | P2 模拟器、TTS/MP4、LMS、RAG、学生 AI Tutor、教师风格学习 | 可进入真实教学试点 |

### 3.2 “思维链”表述应调整

文档多处写到“思维链展示”。不建议把模型内部推理直接作为产品功能。更稳妥的需求是：

- 展示工具调用轨迹：`knowledge_analyze -> demo_plan -> tool_calls -> validate_demo_package`
- 展示关键证据：知识点、课件素材、图示结构、计算/实验结果、错误信息
- 展示生成摘要：为什么选择 P0/P1/P2，哪些内容被改写
- 保留审计日志：prompt hash、模型、token、latency、工具入参/出参摘要

建议把文档中的“思维链”统一改为“AI 执行轨迹”或“生成依据”。

### 3.3 补充核心用户故事

建议新增可验收用户故事，而不只是功能表：

- 作为教师，我输入一个数据库知识点，系统能在 10 秒内生成 6 步演示，并标明每一步的知识依据或实验依据。
- 作为教师，我能对第 3 步说“讲通俗一点”，系统只重写第 3 步，不破坏其他步骤。
- 作为教师，我能保存当前演示为版本 A，继续修改为版本 B，并查看差异。
- 作为学生，我能跟随课堂同步播放，并在某一步提交测验答案。

### 3.4 补充非功能需求的可测口径

当前非功能指标较理想化，建议补上测量方式：

- AI 首帧 `<500ms`：仅指服务端接受消息后推送 `agent:thinking`，不包含完整生成。
- 完整演示生成：MVP 可设 `<15s`，P2 模拟器另设 `<45s`。
- 前端体积 `<400KB` 不现实，Mermaid、D3、ECharts 同时引入会显著超出。建议改为首屏 JS `<500KB gzip`，重型可视化按需加载。
- 并发 `>200 学生/教室` 需要指定部署形态、单实例资源、WebSocket 压测脚本。

### 3.5 补充安全与合规需求

建议新增：

- 教师/学生身份认证。
- 演示、对话、课堂 room 的权限边界。
- 知识演示中的代码/实验沙箱限制：只读、超时、资源限制、禁止危险操作。
- LLM 数据脱敏策略。
- 学生学习数据的最小化采集与删除机制。
- 导出链接的有效期和访问控制。

## 4. 前端设计优化建议

### 4.1 教师工作台布局需要更偏生产工具

当前文档采用三栏：对话列表 + Chat/FlowEditor + Preview。方向正确，但右侧 320px 预览太窄，无法承载 Mermaid、树图、状态机、实验模拟器等核心内容。

建议改为：

- 左侧：对话/课程大纲/历史搜索，可折叠，默认 280px。
- 中间：主工作区，使用 Tab 或 Split View 切换 `对话`、`步骤编排`、`版本对比`。
- 右侧：可伸缩 Inspector，展示当前步骤属性、演示证据、测验、导出设置。
- 演示预览使用底部或独立大面板，不固定死在 320px。

推荐工作台结构：

```text
---------------------------------------------------------------+
| Header: Project / Course / Model / Sync / Export             |
+----------+--------------------------------------+-------------+
| Library  | Main Canvas                          | Inspector   |
|          | - Chat                               | - Evidence  |
| Conv     | - Flow                               | - Step meta |
| Search   | - Preview                            | - Quiz      |
| Tags     | - Diff                               | - Export    |
+----------+--------------------------------------+-------------+
| Status: ws / generation / token / last saved                  |
+---------------------------------------------------------------+
```

### 4.2 前端应减少卡片堆叠，强化密度和状态

这是教师备课工具，不适合过多大圆角卡片和装饰性空间。建议：

- 卡片圆角控制在 6-8px。
- 工作区背景使用中性灰，内容区使用清晰分割线。
- 常用操作使用 icon button + tooltip。
- 状态信息固定显示：连接状态、生成状态、保存状态、当前模型、当前版本。
- 不把说明文字写进 UI，改成明确控件和状态。

### 4.3 需要明确交互状态

文档缺少以下状态设计：

- 空状态：无对话、无演示、无步骤、无网络。
- 生成中：工具调用、步骤预览、可打断。
- 局部重写中：只锁定当前步骤，不冻结整个页面。
- 失败状态：知识演示解析失败、LLM 失败、WebSocket 断开、导出失败。
- 冲突状态：同一对话多标签页同时编辑。
- 保存状态：未保存、保存中、已保存、保存失败。

### 4.4 学生端应独立设计，不应复用完整教师播放器

当前 `StudentPage` 直接嵌入 `ExecutionPlayer`，这会把教师端复杂控件带到学生端。建议拆分：

- `TeacherPlayer`：可编辑、可跳转、可查看证据。
- `ClassroomPlayer`：大屏投射，少控件、高可读。
- `StudentPlayer`：只读、答题、追问、掌握度反馈。

### 4.5 可视化引擎应按需加载

Mermaid、D3、ECharts、执行计划树、B+树模拟器不应全部进首屏包。建议：

- `MermaidRenderer` 使用动态 import。
- P2 模拟器独立 chunk。
- 学生端不加载教师编辑器。
- Classroom 不加载 ConversationPanel 和 FlowEditor。

## 5. 当前实现风险

### 5.1 源码中文存在明显乱码

`apps/web/src/pages/*`、`apps/web/src/features/execution-player/Player.tsx`、`apps/web/src/lib/types.ts`、`apps/api/main.py`、`README.md` 等文件在当前环境读取时存在大量乱码。部分 JSX 文案看起来已损坏到接近语法错误的程度，例如缺少闭合引号、闭合标签异常、按钮符号乱码。

虽然 `npx.cmd tsc -p tsconfig.app.json --noEmit --incremental false` 当前通过，但 UI 文案已经不可交付。建议：

1. 统一仓库编码为 UTF-8。
2. 修复所有已损坏中文文案。
3. 增加 `.editorconfig`。
4. CI 中增加 `npm run build`、`npm run lint` 和基础页面 smoke test。

### 5.2 构建命令在当前环境受写入路径影响

`npm.cmd run build` 失败原因是 TypeScript 尝试写入：

```text
apps/web/node_modules/.tmp/tsconfig.app.tsbuildinfo
apps/web/node_modules/.tmp/tsconfig.node.tsbuildinfo
```

当前沙箱拒绝写入该位置。建议将 `tsBuildInfoFile` 改到项目可写目录，例如：

```json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./.tmp/tsconfig.app.tsbuildinfo"
  }
}
```

并将 `.tmp/` 加入 `.gitignore`。

### 5.3 API 版本和契约不一致

文档写的是 `/api/v5/*`，代码实际是 `/api/*`。WebSocket query 参数文档是 `teacherId`、`convId`，代码里前端发送的是 `teacher_id`、`conv_id`，后端参数也是 `teacher_id`、`conv_id`。

建议建立单一契约源：

- `packages/api-contract/openapi.json`
- `packages/api-contract/ws-events.schema.json`
- 前端类型从契约生成，不手写漂移。

### 5.4 后端仍是内存状态，不满足多对话需求

当前后端：

- `conversations` 是内存 dict。
- `messages` 是内存 dict。
- `connected_rooms` 是进程内 set。
- Redis 只用于尝试缓存 message。

这不满足文档中的持久化、重连恢复、跨实例课堂广播，也不满足课程知识资产长期复用。建议优先落地 PostgreSQL 表：

- `conversations`
- `messages`
- `demo_snapshots`
- `teacher_profiles`
- `classroom_sessions`
- `student_progress`

Redis 只承担热缓存、Pub/Sub、限流、短期会话状态。

### 5.5 WebSocket 事件语义不完整

当前存在：

- `assistant-text` 事件不在需求主表中。
- `conv:new_message` 是实现新增事件，文档未定义。
- `chat:interrupt` 文档有，后端未真正打断生成。
- `step:regenerate` 前端/文档有，后端 REST 与 WS 都未完整实现。
- `demo:updated` 在前端 store 支持，但后端主要发送 `demo:complete`。

建议把事件分为：

- 命令：客户端请求改变状态。
- 事件：服务端确认状态改变。
- 流式片段：只用于生成过程。
- 错误：带 `code`、`message`、`retryable`、`requestId`。

### 5.6 前端 store 边界需要调整

当前 `conversationStore` 和 `demoStore` 都有 `generationStatus`，容易状态不同步。建议：

- `conversationStore` 管对话列表、消息、当前对话。
- `demoStore` 管 demo、steps、snapshots。
- `generationStore` 或 `jobStore` 管 AI 生成任务、进度、取消、错误。
- `playbackStore` 只管播放器位置和播放状态。

### 5.7 当前视觉实现和设计文档差距较大

当前页面大量使用通用灰白卡片，右侧预览空间偏窄，课堂页和学生页仍是居中卡片。和“教学演示工作台/课堂投射/学生自适应学习”的目标不匹配。

建议先做三个页面的信息架构重构：

- 教师页：高密度生产工具。
- 课堂页：全屏演示，大字号，弱化编辑控件。
- 学生页：移动端优先，答题和追问在当前步骤下方。

## 6. 建议优先级

### P0：必须先修

1. 修复源码乱码与 UI 文案损坏。
2. 统一 API 路径和 WebSocket 事件命名。
3. 把“思维链展示”改成“AI 执行轨迹/工具调用摘要”。
4. 落地 PG 持久化最小模型：conversation、message、demo_snapshot。
5. 实现 `chat:interrupt` 和 `step:regenerate` 的真实后端流程。
6. 拆分教师/课堂/学生播放器。

### P1：提升可用性

1. 重新设计教师工作台为可伸缩三区域布局。
2. 增加空状态、加载状态、错误状态、保存状态。
3. 动态加载 Mermaid/P2 模拟器。
4. 增加版本快照列表和差异对比。
5. 增加基础导出：HTML + Mermaid。

### P2：进入教学试点

1. Redis Pub/Sub 课堂同步。
2. 学生端 AI Tutor。
3. 课纲 RAG。
4. MP4/TTS/LMS 导出。
5. 教师风格 Profile。
6. 压测、审计、权限、安全策略。

## 7. 文档建议改写点

### `requirements-spec.md`

建议新增章节：

- MVP 范围与非目标。
- 用户故事与验收标准。
- 安全与权限。
- 数据持久化策略。
- 错误码与降级策略。
- 生成任务状态机。
- 知识演示沙箱规则。

建议调整措辞：

- “思维链” -> “AI 执行轨迹 / 工具调用摘要 / 生成依据”。
- “无硬限制” -> 给出产品上限和技术扩展策略。
- “前端体积 <400KB 含 Mermaid/D3.js” -> 改为首屏预算 + 按需加载预算。

### `frontend-design.md`

建议新增章节：

- 设计系统：颜色、字号、间距、控件、图标、状态色。
- 三端差异：教师、课堂、学生分别设计。
- 响应式真实布局草图。
- 组件状态表：loading、empty、error、disabled、streaming、dirty。
- 可访问性：键盘操作、焦点、对比度、投影模式字号。
- 性能策略：lazy loading、虚拟列表、长消息渲染、Mermaid 缓存。

## 8. 推荐下一步执行计划

### 第 1 阶段：修复基础可运行性

- 修复乱码。
- 调整 TypeScript build info 输出目录。
- 建立最小 CI：typecheck、build、lint。
- 确认 `npm.cmd run build` 可通过。

### 第 2 阶段：契约收敛

- 定义统一 REST + WS schema。
- 前后端事件名对齐。
- 删除或标记未实现事件。
- DemoPackage v5 类型和 schema 对齐。

### 第 3 阶段：MVP 产品闭环

- 知识点输入 -> 6 步演示 -> 对话精修某一步 -> 保存快照 -> 播放 -> 导出 HTML。
- 教师页完成高密度工作台改版。
- 学生页与课堂页从教师播放器中拆出。

### 第 4 阶段：教学增强

- Mermaid 可视化。
- Quiz 反馈。
- 课堂同步。
- 版本对比。

## 9. 最关键的产品判断

这个项目的优势不在于“又做一个 SQL 可视化播放器”，而在于把数据库课程备课过程里的反复解释、修改、试讲、出题和复用全部沉淀为可追溯对话和版本化演示。SQL 只是其中最容易起步的知识域之一，最终目标应当覆盖整门课程的知识图谱。

因此接下来的优化重点应放在：

- 让教师快速生成一个可信演示。
- 让教师能低成本改某一步。
- 让每次修改都有版本和证据。
- 让课堂和学生端消费同一个演示资产。

P2 模拟器、RAG、TTS、MP4 都有价值，但应排在这个核心闭环之后。
