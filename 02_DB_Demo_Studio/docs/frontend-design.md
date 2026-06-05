# DB Demo Studio — 前端功能架构设计 v5

> 对应：`requirements-spec.md` v5（AI 协作对话版）
> 范围：前端组件树 · 状态管理 · 数据流 · 接口契约 · 路由设计

---

## 1. 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│  DB Demo Studio Frontend Architecture v5                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─ Page Layer (路由级) ───────────────────────────────────┐   │
│  │                                                          │   │
│  │  /teacher     → TeacherWorkbenchPage (主工作台)          │   │
│  │  /classroom   → ClassroomPage (教师课堂投射)              │   │
│  │  /student/:id → StudentPage (学生端自适应学习)            │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                │ 各 Page 组合以下 Feature 模块                    │
│                ▼                                                 │
│  ┌─ Feature Modules ───────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌── ConversationPanel ──┐  ┌── ChatPanel ───────────┐  │   │
│  │  │  对话列表 + 搜索       │  │  消息流 + 输入 + 快      │  │   │
│  │  │  多对话 CRUD          │  │  捷操作 + Agent 轨迹     │  │   │
│  │  └───────────────────────┘  └────────────────────────┘  │   │
│  │                                                          │   │
│  │  ┌── FlowEditor ──────────┐  ┌── ExecutionPlayer ────┐  │   │
│  │  │  步骤卡片 + 拖拽排序    │  │  分步播放 + 控制条     │  │   │
│  │  │  版本快照 + 分支管理    │  │  进度条 + 阶段面板    │  │   │
│  │  └───────────────────────┘  └────────────────────────┘  │   │
│  │                                                          │   │
│  │  ┌── AnimationEngine ─────┐  ┌── QuizPanel ──────────┐  │   │
│  │  │  Mermaid / D3.js /     │  │  嵌入式测验 + 答题    │  │   │
│  │  │  ECharts / 树图 / 模拟器 │  │  掌握度 + 讲解        │  │   │
│  │  └───────────────────────┘  └────────────────────────┘  │   │
│  │                                                          │   │
│  │  ┌── ExportPanel ─────────┐  ┌── StudentLens ───────┐  │   │
│  │  │  导出 MP4/Mermaid/LTI  │  │  学生视角预览          │  │   │
│  │  └───────────────────────┘  └────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                │ 所有模块共享以下 Layer                           │
│                ▼                                                 │
│  ┌─ Shared Layers ─────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌── WebSocket Service ───────────┐                     │   │
│  │  │  连接管理 / 心跳 / 自动重连    │                     │   │
│  │  │  消息路由 / Room 订阅          │                     │   │
│  │  └───────────────────────────────┘                     │   │
│  │                                                          │   │
│  │  ┌── State Store (Zustand) ──────┐                     │   │
│  │  │  conversationStore            │                     │   │
│  │  │  demoStore                    │                     │   │
│  │  │  playbackStore                │                     │   │
│  │  │  teacherStore                 │                     │   │
│  │  └───────────────────────────────┘                     │   │
│  │                                                          │   │
│  │  ┌── API Layer ──────────────────┐                     │   │
│  │  │  REST 客户端 + WebSocket 封装  │                     │   │
│  │  └───────────────────────────────┘                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. 路由设计

```typescript
// src/main.tsx —— 路由表
<Routes>
  <Route element={<AppLayout />}>

    {/* 教师主工作台：多对话 + AI Studio + 演示编辑 + 预览 */}
    <Route path="/" element={<TeacherWorkbenchPage />} />

    {/* 课堂播放：教师投射到投影，学生设备跟随 */}
    <Route path="/classroom" element={<ClassroomPage />} />
    <Route path="/classroom/:convId" element={<ClassroomPage />} />

    {/* 学生端：LMS iframe 嵌入，自适应学习 */}
    <Route path="/student/:demoId" element={<StudentPage />} />

  </Route>
</Routes>
```

---

## 3. 页面级设计

### 3.1 TeacherWorkbenchPage（教师主工作台）

```
┌──────────────────────────────────────────────────────────────────────┐
│  Header: DB Demo Studio  |  对话搜索 🔍  |  [课堂模式] [教师设置]   │
├───────────┬──────────────────────────────────────────────┬───────────┤
│           │                                              │           │
│  ConversationList │  ┌─ ChatPanel ─────────────────┐    │  Preview  │
│  (对话列表)      │  │  消息流 (含 Agent 轨迹)      │    │   Panel   │
│                  │  │                              │    │           │
│  ➤ JOIN 查询    │  │  用户: 讲讲 JOIN 查询         │    │  ┌─────┐  │
│    P1 Mermaid   │  │  AI: [轨迹] 调用知识分析工具  │    │  │Player│  │
│  对话中 | 3轮    │  │       → explain_mysql → ...  │    │  │      │  │
│                  │  │  [步骤预览] lex→parse→...    │    │  │进度条│  │
│  ────────────   │  │                              │    │  │      │  │
│  B+树索引原理   │  │  ┌─ QuickActions ─────────┐   │    │  │控制条│  │
│    P2 模拟器    │  │  │ 📊 加可视化  📝 出题   │   │    │  │      │  │
│  已定稿 | 8轮    │  │  │ 🔊 TTS 试听  📤 导出  │   │    │  └─────┘  │
│                  │  │  └────────────────────────┘   │    │           │
│  ────────────   │  │                              │    │           │
│  事务隔离级别   │  │  [输入知识点/案例/SQL...] [发送]│    │           │
│    P2 事务      │  └──────────────────────────────┘    │           │
│  草稿 | 2轮      │                                     │           │
│                  │  ┌─ FlowEditor ─────────────────┐    │           │
│  [+ 新建对话]   │  │  步骤卡片链 | 拖拽排序       │    │           │
│                  │  │  [1→ lex] [2→ parse] [3→ opt]│    │           │
│                  │  │  ↑ 点击某步可在对话中精修     │    │           │
│                  │  └──────────────────────────────┘    │           │
│                  │                                     │           │
├───────────┴──────────────────────────────────────────────┴───────────┤
│  Status Bar: 对话中 | 模型: Claude Sonnet 4.6 | tokens: 1,234      │
└──────────────────────────────────────────────────────────────────────┘
```

**布局实现：** CSS Grid 三列，左侧 240px 固定，右侧 320px 固定，中间自适应。

```tsx
// src/pages/TeacherWorkbenchPage.tsx (结构概览)
export default function TeacherWorkbenchPage() {
  return (
    <div className="grid h-[calc(100vh-56px)]"
         style={{ gridTemplateColumns: '240px 1fr 320px' }}>
      {/* 左侧：对话列表 */}
      <ConversationPanel />

      {/* 中间：AI 对话 + 步骤编辑 */}
      <div className="flex flex-col overflow-hidden">
        <ChatPanel />
        <FlowEditor />
      </div>

      {/* 右侧：演示预览 */}
      <div className="flex flex-col overflow-hidden border-l border-gray-200">
        <ExecutionPlayer />
      </div>
    </div>
  )
}
```

### 3.2 ClassroomPage（课堂模式）

教师端投射到投影，所有学生设备同步。

```
┌──────────────────────────────────────────────────────────────────┐
│  Header: ← 返回备课  |  演示: JOIN 查询讲解  |  学生: 36 人在线  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─ Player (全宽, 最大化) ────────────────────────────────┐    │
│  │                                                          │    │
│  │  进度条: [■■■■■■■■░░░░] 3/6 步                          │    │
│  │                                                          │    │
│  │  ┌─ Visualization ─────────────────────────────────┐     │    │
│  │  │  Mermaid / D3 B+树 / 树图 / 过程模拟器          │     │    │
│  │  └─────────────────────────────────────────────────┘     │    │
│  │                                                          │    │
│  │  ┌─ Narration ─────────────────────────────────────┐     │    │
│  │  │  讲解词 + TTS 🔊  |  [中/EN]                    │     │    │
│  │  └─────────────────────────────────────────────────┘     │    │
│  │                                                          │    │
│  │  ◀  ▶  ▶▶  [进度: 3/6]                                 │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  学生反馈:  😊 96% 掌握  |  🤔 3人提问  |  平均时长 4.2s/步     │
└──────────────────────────────────────────────────────────────────┘
```

### 3.3 StudentPage（学生自适应端）

可嵌入 LMS iframe。

```
┌──────────────────────────────────────────────────────────────┐
│  JOIN 查询执行过程  |  进度 50%  |  🔊 TTS                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─ Step Display ───────────────────────────────────────┐   │
│  │  [可视化内容: Mermaid / 执行计划 / 动画]              │   │
│  │  [讲解词]                                            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ◀  ▶  ▶▶  [3/6]  [展开细节 ▼]                              │
│                                                              │
│  ┌─ Quiz ──────────────────────────────────────────────┐   │
│  │  ✅ 这步你掌握了吗？                                  │   │
│  │  这条知识点演示对应了哪些关键步骤？                  │   │
│  │  ○ 2  ○ 3  ● 4  ○ 5                               │   │
│  │  ✅ 正确！你已经识别出关键步骤链路。                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─ AI Tutor ───────────────────────────────────────────┐   │
│  │  对这一步有疑问？可以问我...                           │   │
│  │  [输入问题...] [发送]                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  掌握度: ■■■■■■■□□□ 70%  |  推荐下一步: 外连接查询         │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. 组件树

```
src/
├── main.tsx                          # 入口 + 路由
├── App.tsx                           # <Outlet />
├── index.css                         # TailwindCSS
│
├── layouts/
│   └── AppLayout.tsx                 # Header 导航 + 路由出口
│
├── pages/
│   ├── TeacherWorkbenchPage.tsx      # 教师主工作台 (grid 三栏)
│   ├── ClassroomPage.tsx             # 课堂投影
│   └── StudentPage.tsx               # 学生端 (LMS iframe)
│
├── features/
│   ├── conversation/
│   │   ├── ConversationPanel.tsx      # 对话列表侧栏
│   │   ├── ConversationCard.tsx       # 单条对话卡片
│   │   ├── ConversationSearch.tsx     # 搜索/筛选
│   │   └── ConversationActions.tsx    # 创建/删除/重命名
│   │
│   ├── chat/
│   │   ├── ChatPanel.tsx             # 消息流 + 输入区
│   │   ├── MessageBubble.tsx         # 单条消息 (user/assistant/system)
│   │   ├── AgentThinkingChain.tsx    # Agent 轨迹展示
│   │   ├── ChatInput.tsx             # 多模态输入 (text/sql/image/knowledge)
│   │   ├── QuickActions.tsx          # 快捷操作面板
│   │   └── DemoSnapshotIndicator.tsx # 当前演示快照版本
│   │
│   ├── flow-editor/
│   │   ├── FlowEditor.tsx            # 步骤卡片链
│   │   ├── StepCard.tsx              # 单步卡片
│   │   ├── StepDetailDrawer.tsx      # 步骤详情抽屉
│   │   └── VersionTimeline.tsx       # 版本快照时间线
│   │
│   ├── execution-player/
│   │   ├── ExecutionPlayer.tsx       # 主播放器
│   │   ├── ProgressBar.tsx           # 步骤进度条
│   │   ├── PlaybackControls.tsx      # 播放控制 (◀ ▶ ▶ ▶)
│   │   ├── PhasePanel.tsx            # 阶段演示面板
│   │   ├── CostCompareCards.tsx      # 多策略证据对比
│   │   └── NarrationBox.tsx          # 讲解词 + TTS 按钮
│   │
│   ├── animation/
│   │   ├── AnimationEngine.tsx       # 动画引擎调度
│   │   ├── MermaidRenderer.tsx       # Mermaid 渲染
│   │   ├── BPlusTreeCanvas.tsx       # D3.js B+树动画
│   │   ├── SqlSimulator.tsx          # SQL / 过程分步模拟器
│   │   ├── TransactionDemo.tsx       # 事务隔离级别演示
│   │   └── ExecutionPlanTree.tsx     # 可视化推理/执行树
│   │
│   ├── quiz/
│   │   ├── QuizPanel.tsx             # 嵌入式测验
│   │   ├── QuizQuestion.tsx          # 选择题/填空题组件
│   │   └── QuizResult.tsx            # 答题结果 + AI 讲解
│   │
│   ├── student/
│   │   ├── AdaptivePlayer.tsx        # 学生端自适应播放器
│   │   ├── MasteryGauge.tsx          # 掌握度仪表盘
│   │   ├── AiTutor.tsx               # 学生端 AI 问答
│   │   └── AdaptiveSuggestions.tsx   # AI 推荐下一步
│   │
│   └── export/
│       ├── ExportPanel.tsx           # 导出对话框
│       └── ExportOptions.tsx         # 导出格式选择
│
├── lib/
│   ├── types.ts                      # 全局类型定义
│   ├── ws-client.ts                  # WebSocket 客户端封装
│   ├── api-client.ts                 # REST API 客户端
│   └── utils.ts                      # 工具函数
│
├── stores/
│   ├── conversationStore.ts          # 对话状态 (Zustand)
│   ├── demoStore.ts                  # 演示状态
│   ├── playbackStore.ts              # 播放状态
│   ├── teacherStore.ts               # 教师风格
│   └── studentStore.ts               # 学生端状态
│
├── hooks/
│   ├── useWebSocket.ts               # WebSocket hook
│   ├── useConversation.ts            # 对话 CRUD hook
│   ├── useDemoStream.ts              # AI 流式推送 hook
│   └── usePlayback.ts               # 播放器 hook
│
└── components/                       # 全局通用组件
    ├── Button.tsx
    ├── Modal.tsx
    ├── Badge.tsx
    ├── Spinner.tsx
    └── IconButton.tsx
```

---

## 5. 状态管理设计（Zustand）

### 5.1 conversationStore

```typescript
// stores/conversationStore.ts
interface ConversationState {
  // 列表
  conversations: ConversationSummary[]
  activeConvId: string | null
  loading: boolean

  // 当前对话详情
  currentConv: Conversation | null
  messages: Message[]
  hasMoreMessages: boolean          // 分页加载

  // Actions
  loadConversations: () => Promise<void>
  createConversation: (title?: string) => Promise<string>  // 返回 convId
  switchConversation: (convId: string) => Promise<void>
  deleteConversation: (convId: string) => Promise<void>
  renameConversation: (convId: string, title: string) => Promise<void>
  searchConversations: (query: string) => Promise<void>

  // 消息
  appendMessage: (msg: Message) => void
  appendStreamChunk: (chunk: string) => void   // 流式追加
  loadMoreMessages: () => Promise<void>         // 懒加载更早消息

  // 状态同步 (WebSocket)
  syncFromServer: (payload: ServerSyncPayload) => void
}
```

### 5.2 demoStore

```typescript
// stores/demoStore.ts
interface DemoState {
  // 当前演示
  currentDemo: DemoPackage | null
  snapshots: DemoPackage[]          // 版本快照列表
  activeSnapshotIndex: number

  // 对话关联
  currentConvId: string | null
  generationStatus: 'idle' | 'generating' | 'interrupted'

  // Actions
  setDemo: (demo: DemoPackage) => void
  updateStep: (stepId: string, updates: Partial<DemoStep>) => void
  reorderSteps: (fromIndex: number, toIndex: number) => void
  addBranch: (afterStepId: string, branchDemo: DemoPackage) => void
  regenerateStep: (stepId: string, hint?: string) => Promise<void>

  // 快照
  saveSnapshot: () => void
  restoreSnapshot: (index: number) => void
  compareSnapshots: (a: number, b: number) => SnapshotDiff

  // 导出
  exportDemo: (format: 'mp4' | 'mermaid' | 'lti') => Promise<string>
}
```

### 5.3 playbackStore

```typescript
// stores/playbackStore.ts
interface PlaybackState {
  // 播放状态
  currentStepIndex: number
  isPlaying: boolean
  isAdaptiveMode: boolean           // 自适应模式（仅学生端）
  speedMultiplier: number

  // 学生数据（学生端）
  quizResults: QuizResult[]
  masteryLevel: number              // 0-100
  timeOnStep: number                // 当前步停留秒数

  // Actions
  nextStep: () => void
  prevStep: () => void
  seekTo: (index: number) => void
  togglePlay: () => void
  setSpeed: (speed: number) => void

  // 自适应
  adaptToStudent: () => AdaptiveDecision
  recordQuizAnswer: (questionId: string, answer: number) => void
  recordTimeOnStep: () => void
}

interface AdaptiveDecision {
  action: 'next' | 'skip' | 'expand' | 'branch'
  rationale: string
  targetStepIndex?: number
}
```

### 5.4 teacherStore

```typescript
// stores/teacherStore.ts
interface TeacherState {
  profile: TeacherProfile | null
  isLoaded: boolean

  updateProfile: (updates: Partial<TeacherProfile>) => Promise<void>
  loadProfile: () => Promise<void>
}

interface TeacherProfile {
  id: string
  name: string
  preferredModel: string            // 默认 LLM
  defaultDemoType: string           // P0/P1/P2
  narrationStyle: 'concise' | 'detailed' | 'example-heavy' | 'analogy'
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  preferences: {
    autoGenerateQuiz: boolean
    defaultTTS: boolean
    exportFormat: string
  }
}
```

---

## 6. 数据流设计

### 6.1 用户发送消息 → 接收 AI 流式响应

```
用户输入 "讲讲 JOIN 查询" → 点击发送
        │
        ▼
ChatInput ──dispatch──→ conversationStore.appendMessage({role:'user',...})
        │
        ▼
useWebSocket.send({type:'chat:message', convId, content: {text, sql?}})
        │
        ▼  WebSocket 连接
[FastAPI WebSocket Manager]
        │
        ▼  后端处理...
        │
        ▼  流式推送回前端
useWebSocket.onMessage ──事件类型路由──→
        │
        ├── 'agent:thinking' → ChatPanel 展示 Agent 轨迹
        │     DemoSnapshotIndicator 更新 "生成中..."
        │
        ├── 'step:preview'   → FlowEditor 新增步骤卡片
        │     ExecutionPlayer 进度条更新
        │
        ├── 'demo:updated'   → demoStore.setDemo(evt.demo)
        │     Player 刷新全部
        │
        ├── 'quiz:result'    → QuizPanel 展示结果
        │
        └── 'demo:complete'  → conversationStore.appendMessage({role:'assistant',...})
              DemoSnapshotIndicator 更新 "已就绪"
              generationStatus → 'idle'
```

### 6.2 对话切换

```
用户点击对话列表中的另一条对话
        │
        ▼
ConversationCard.onClick
        │
        ▼
conversationStore.switchConversation(targetConvId)
        │
        ├── 1. 保存当前对话未发送的输入 (草稿)
        │
        ├── 2. WebSocket 发送 conv:switch {convId: targetConvId}
        │
        ├── 3. 本地:
        │     ├── Redis: 快速加载最近 50 条消息 (conv:messages)
        │     └── demoStore.setDemo(targetConv.currentDemo)
        │
        ├── 4. 同时懒加载 PG 全量历史 (如有需要)
        │
        └── 5. Playback重置 → stepIndex=0, isPlaying=false
```

### 6.3 课堂广播

```
教师在课堂模式点击"下一步"
        │
        ▼
PlaybackControls.nextStep()
        │
        ├── playbackStore.nextStep()
        │
        └── WebSocket 发送: {type:'player:seek', stepIndex:3, convId}
              │
              ▼
        后端 Redis Pub/Sub → room:{convId}
              │
              ▼
        所有学生端 WebSocket 收到: {type:'player:sync', stepIndex:3}
              │
              ▼
        学生端 playbackStore.seekTo(3) → StudentPage 同步跳转
```

### 6.4 学生端自适应学习

```
学生在第 2 步做错了一道题
        │
        ▼
QuizPanel 提交答案 → WebSocket → {type:'quiz:answer', stepIndex:2, answer:1}
        │
        ▼
后端记录 + AI 判断掌握度
        │
        ▼
WebSocket ← {type:'adaptive:suggest',
              action:'expand',
              rationale:'学生未理解 WHERE 过滤，建议展开详细讲',
              targetStepIndex:2.5}
        │
        ▼
StudentPage 弹出 "AI 建议展开讲解 WHERE 子句，是否查看？"
        │
用户确认 → 播放器跳转到展开的子步骤链
```

---

## 7. WebSocket 客户端封装

```typescript
// lib/ws-client.ts
type WsEvent =
  // 客户端 → 服务端
  | { type: 'chat:message'; convId: string; content: ChatContent }
  | { type: 'chat:interrupt'; convId: string }
  | { type: 'conv:create'; title?: string }
  | { type: 'conv:switch'; convId: string }
  | { type: 'conv:delete'; convId: string }
  | { type: 'conv:rename'; convId: string; title: string }
  | { type: 'step:regenerate'; convId: string; stepId: string; hint?: string }
  | { type: 'quiz:answer'; stepIndex: number; answer: number }
  | { type: 'player:seek'; stepIndex: number; convId: string }
  | { type: 'demo:export'; format: string }

  // 服务端 → 客户端
  | { type: 'conv:list'; conversations: ConversationSummary[] }
  | { type: 'conv:loaded'; convId: string; messages: Message[] }
  | { type: 'agent:thinking'; content: string }
  | { type: 'agent:tool_call'; tool: string; status: 'start' | 'complete'; result?: unknown }
  | { type: 'step:preview'; step: DemoStep }
  | { type: 'step:regenerated'; convId: string; step: DemoStep }
  | { type: 'demo:updated'; convId: string; demo: DemoPackage }
  | { type: 'demo:complete'; convId: string; demo: DemoPackage }
  | { type: 'demo:exported'; url: string; format: string }
  | { type: 'quiz:result'; correct: boolean; explanation: string }
  | { type: 'adaptive:suggest'; action: string; rationale: string }
  | { type: 'player:sync'; stepIndex: number }  // 课堂广播
  | { type: 'error'; message: string }
```

```typescript
// hooks/useWebSocket.ts
function useWebSocket() {
  // 自动连接 (带 teacherId + convId)
  // 心跳保持 (ping/pong 每 30s)
  // 自动重连 (指数退避: 1s → 2s → 4s → max 30s)
  // 事件分发: 按 type 路由到对应 store/component

  return {
    send: (event: WsEvent) => void
    sendInterrupt: () => void
    reconnect: () => void
    connectionStatus: 'connecting' | 'connected' | 'disconnected'
  }
}
```

---

## 8. 核心类型定义（补充 requirements-spec.md）

```typescript
// lib/types.ts

// === 对话 ===
interface ConversationSummary {
  id: string
  title: string
  status: 'active' | 'draft' | 'finalized' | 'archived'
  demoType: 'p0' | 'p1' | 'p2'
  messageCount: number
  lastActivity: string              // ISO datetime
  summary?: string
  tags?: string[]
}

interface Conversation extends ConversationSummary {
  messages: Message[]
  currentDemoId?: string
  snapshotsCount: number
}

interface Message {
  id: string
  convId: string
  role: 'user' | 'assistant' | 'system'
  type: 'text' | 'sql' | 'image' | 'demo_snapshot' | 'tool_call'
  content: MessageContent
  createdAt: string
  metadata?: {
    model?: string
    tokensUsed?: number
    latencyMs?: number
  }
}

interface MessageContent {
  text?: string
  sql?: string
  knowledge?: string
  imageUrl?: string
  toolCalls?: ToolCall[]
  demoSnapshotId?: string
}

interface ToolCall {
  tool: string
  args: unknown
  result?: unknown
  status: 'running' | 'complete' | 'error'
}

// === 演示 ===
interface DemoPackage {
  id: string
  convId: string
  version: number
  snapshotOrder: number
  title: { zh: string; en: string }
  demoType: 'standard' | 'mermaid' | 'ascii' | 'echarts' | 'sql-simulator' | 'bplus-tree' | 'transaction'
  metadata: DemoMetadata
  steps: DemoStep[]
  simulationData?: SimulationData
  engineCompare?: { mysql?: unknown; postgres?: unknown }
  adaptiveMeta?: AdaptiveMeta
}

interface DemoMetadata {
  teacherId: string
  priority: 'p0' | 'p1' | 'p2'
  generatedAt: string
  model: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
}

interface DemoStep {
  id: string
  order: number
  phase: 'lex' | 'parse' | 'optimize' | 'plan' | 'execute' | 'result'
  narration: {
    zh: string
    en: string
    ttsUrl?: string
    source: 'ai' | 'teacher'
  }
  visuals: VisualConfig
  quiz?: QuizQuestion
  adaptiveSkip?: 'if_mastered' | null
}

type VisualConfig = {
  type: 'highlight-sql' | 'mermaid-step' | 'ascii-frame'
      | 'simulator-step' | 'index-anim' | 'transaction-scene'
  config: Record<string, unknown>
}

interface QuizQuestion {
  question: string
  options: string[]
  answer: number
  explanation: string
}

interface SimulationData {
  mermaidCode?: string
  sqlSimulator?: {
    steps: Array<{ clause: string; description: string; intermediateRows: number }>
  }
  indexAnimation?: {
    treeType: 'bplus'
    order: number
    operations: Array<{ type: string; key: number; highlightNode: string }>
  }
  transactionDemo?: {
    isolationLevel: string
    sessionA: string[]
    sessionB: string[]
    observedPhenomenon: string
  }
}

// === 自适应 ===
interface AdaptiveMeta {
  prerequisites: string[]
  teaches: string[]
  estimatedDuration: number
}

interface MasteryData {
  stepId: string
  correctRate: number        // 0-100
  attempts: number
  timeSpent: number          // 秒
  quizResults: QuizResult[]
}

// === 教师风格 ===
interface TeacherProfile {
  id: string
  preferredModel: string
  defaultDemoType: string
  narrationStyle: 'concise' | 'detailed' | 'example-heavy' | 'analogy'
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  preferences: {
    autoGenerateQuiz: boolean
    defaultTTS: boolean
    exportFormat: string
  }
}

// === 问答 ===
interface QuizResult {
  questionId: string
  selectedAnswer: number
  correctAnswer: number
  isCorrect: boolean
  timestamp: string
}
```

---

## 9. 模块职责矩阵

| 模块 | 数据 Owner | WebSocket 事件订阅 | 依赖 |
|---|---|---|---|
| ConversationPanel | conversationStore | conv:list, conv:loaded | 无 |
| ChatPanel | conversationStore | agent:thinking, agent:tool_call, step:preview, demo:complete | ConversationPanel |
| FlowEditor | demoStore | demo:updated, step:regenerated | ChatPanel |
| ExecutionPlayer | playbackStore + demoStore | player:sync, demo:updated | FlowEditor |
| AnimationEngine | demoStore (simulationData) | step:preview | ExecutionPlayer |
| QuizPanel | playbackStore (quizResults) | quiz:result | ExecutionPlayer |
| AiTutor (学生端) | studentStore | adaptive:suggest | QuizPanel |

---

## 10. 响应式适配

| 断点 | 布局 | 说明 |
|---|---|---|
| ≥ 1280px | 三栏 (240px + 1fr + 320px) | 教师桌面备课 |
| 1024px ~ 1279px | 两栏 (对话+编辑 叠加 预览) | 小屏幕笔记本 |
| 768px ~ 1023px | 单栏 (对话+编辑+预览 垂直堆叠) | 平板 |
| < 768px | 单栏全屏 (学生端 LMS 嵌入) | 手机/iframe |

---

> **设计原则：**
> - 状态分散到有明确职责的 Store，不搞全局单一 Store
> - WebSocket 事件是"单向数据流"的源头→Store→React 重新渲染
> - 每个 Feature 模块只订阅与自己相关的事件，互不干扰
> - 对话是核心实体，其他所有数据都从 convId 关联
