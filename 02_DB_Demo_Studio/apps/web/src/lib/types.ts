// DB Demo Studio — 类型定义 v5
// 单一真相源：所有组件共享此类型

// ═══════════════════════════════════════════════
// 对话
// ═══════════════════════════════════════════════

export interface ConversationSummary {
  id: string
  title: string
  status: 'active' | 'draft' | 'finalized' | 'archived'
  demoType: DemoTypeLabel
  messageCount: number
  lastActivity: string // ISO datetime
  summary?: string
  tags?: string[]
  curriculumNode?: string
}

export interface Conversation extends ConversationSummary {
  messages: Message[]
  currentDemoId?: string
  snapshotsCount: number
}

export interface Message {
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
  deleted?: boolean
}

export interface MessageContent {
  text?: string
  sql?: string
  knowledge?: string
  imageUrl?: string
  toolCalls?: ToolCall[]
  demoSnapshotId?: string
}

export interface ToolCall {
  tool: string
  args: unknown
  result?: unknown
  status: 'running' | 'complete' | 'error'
}

// ═══════════════════════════════════════════════
// 演示
// ═══════════════════════════════════════════════

export type DemoTypeLabel = 'standard' | 'mermaid' | 'ascii' | 'echarts'
  | 'sql-simulator' | 'bplus-tree' | 'transaction'

export type DemoPriority = 'p0' | 'p1' | 'p2'

export type WorkflowPhase = 'lex' | 'parse' | 'optimize' | 'plan' | 'execute' | 'result'

export interface DemoPackage {
  id: string
  convId?: string
  version?: number
  snapshotOrder?: number
  title: { zh: string; en: string }
  demoType?: DemoTypeLabel
  steps: DemoStep[]
  workflowTrace?: {
    workflowId: string
    workflowType: 'course-demonstration' | 'concept-progression'
    aiSessionId?: string
    grounding?: { mysql?: string; postgres?: string }
  }
  engineCompare?: { mysql?: unknown; postgres?: unknown }
  simulationData?: SimulationData
  metadata: {
    teacherId?: string
    priority?: DemoPriority
    aiDraftVersion?: string
    teacherVersion: number
    lastAiAction?: 'full-generate' | 'regenerate-step' | 'teacher-edit'
    generatedAt?: string
    model?: string
    difficulty?: 'beginner' | 'intermediate' | 'advanced'
  }
  playback: { defaultStepDurationMs: number; subtitles?: { zh?: string; en?: string } }
  adaptiveMeta?: AdaptiveMeta
  _validation?: { valid: boolean; errors?: string[] }
}

export interface DemoStep {
  id: string
  order: number
  workflowPhase: WorkflowPhase | string
  narration: {
    zh: string
    en: string
    source: 'ai' | 'teacher' | 'rule'
    ttsUrl?: string
  }
  engineEvidence?: Record<string, unknown>
  enginePlan?: { mysql?: unknown; postgres?: unknown }
  visuals?: {
    type: 'highlight-sql' | 'mermaid-step' | 'ascii-frame'
      | 'simulator-step' | 'index-anim' | 'transaction-scene'
    config?: Record<string, unknown>
    highlightRange?: number[]
  }
  groundingRef?: string | null
  timing?: { durationMs: number }
  quiz?: QuizQuestion
  adaptiveSkip?: 'if_mastered' | null
}

export interface QuizQuestion {
  id?: string
  question: string
  options: string[]
  answer: number
  explanation: string
}

export interface SimulationData {
  mermaidCode?: string
  sqlSimulator?: {
    steps: Array<{
      clause: string
      description: string
      intermediateRows: number
      columns?: string[]
      rows?: Array<Record<string, string | number>>
    }>
  }
  indexAnimation?: {
    treeType: 'bplus'
    order: number
    operations: Array<{
      type: 'insert' | 'search' | 'delete'
      key: number
      highlightNode: string
    }>
  }
  transactionDemo?: {
    isolationLevel: string
    sessionA: string[]
    sessionB: string[]
    observedPhenomenon: string
  }
  echartsConfig?: Record<string, unknown>
  asciiAnimation?: string[]
}

export interface AdaptiveMeta {
  prerequisites: string[]
  teaches: string[]
  estimatedDuration: number
}

// ═══════════════════════════════════════════════
// 学生端 / 自适应
// ═══════════════════════════════════════════════

export interface QuizResult {
  questionId: string
  selectedAnswer: number
  correctAnswer: number
  isCorrect: boolean
  timestamp: string
}

export interface MasteryData {
  stepId: string
  correctRate: number    // 0-100
  attempts: number
  timeSpent: number      // 秒
  quizResults: QuizResult[]
}

export interface AdaptiveDecision {
  action: 'next' | 'skip' | 'expand' | 'branch'
  rationale: string
  targetStepIndex?: number
}

// ═══════════════════════════════════════════════
// 教师
// ═══════════════════════════════════════════════

export interface TeacherProfile {
  id: string
  name?: string
  preferredModel: string
  defaultDemoType: DemoTypeLabel
  narrationStyle: 'concise' | 'detailed' | 'example-heavy' | 'analogy'
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  preferences: {
    autoGenerateQuiz: boolean
    defaultTTS: boolean
    exportFormat: string
  }
}

// ═══════════════════════════════════════════════
// WebSocket 协议
// ═══════════════════════════════════════════════

// 客户端 → 服务端
export type WsClientEvent =
  | { type: 'conversation:message'; convId: string; content: { text?: string; sql?: string; knowledge?: string } }
  | { type: 'conversation:interrupt'; convId: string }
  | { type: 'conversation:create'; title?: string }
  | { type: 'conversation:switch'; convId: string }
  | { type: 'conversation:delete'; convId: string }
  | { type: 'conversation:rename'; convId: string; title: string }
  | { type: 'demo:regenerate_step'; convId: string; stepId: string; hint?: string }
  | { type: 'quiz:answer'; convId: string; stepIndex: number; answer: number }
  | { type: 'player:seek'; convId: string; stepIndex: number }
  | { type: 'demo:export'; convId: string; format: string }
  | { type: 'message:delete'; convId: string; msgId: string }
  | { type: 'conversation:clear_messages'; convId: string }

// 服务端 → 客户端
export type WsServerEvent =
  | { type: 'conversation:list'; conversations: ConversationSummary[] }
  | { type: 'conversation:loaded'; convId: string; messages: Message[]; currentDemo?: DemoPackage }
  | { type: 'conversation:created'; conversation: ConversationSummary }
  | { type: 'conversation:deleted'; convId: string }
  | { type: 'assistant:trace'; convId: string; content: string }
  | { type: 'assistant:tool_call'; convId: string; tool: string; status: 'start' | 'complete'; result?: unknown }
  | { type: 'demo:step_preview'; convId: string; step: DemoStep; order: number }
  | { type: 'demo:step_regenerated'; convId: string; step: DemoStep }
  | { type: 'demo:updated'; convId: string; demo: DemoPackage }
  | { type: 'demo:complete'; convId: string; demo?: DemoPackage | null; demo_id: string }
  | { type: 'demo:exported'; convId: string; url: string; format: string }
  | { type: 'quiz:result'; convId: string; correct: boolean; explanation: string }
  | { type: 'learning:suggest'; convId: string; action: string; rationale: string; targetStepIndex?: number }
  | { type: 'conversation:new_message'; convId: string; message: Message }
  | { type: 'player:sync'; convId: string; stepIndex: number }
  | { type: 'error'; convId?: string; message: string }
  | { type: 'assistant:text'; convId: string; content: string }
  | { type: 'conversation:cleared'; convId: string }
  | { type: 'message:deleted'; convId: string; msgId: string }

// ═══════════════════════════════════════════════
// 聊天面板内容 (发送到 WS)
// ═══════════════════════════════════════════════

export interface ChatContent {
  text?: string
  sql?: string
  knowledge?: string
}
