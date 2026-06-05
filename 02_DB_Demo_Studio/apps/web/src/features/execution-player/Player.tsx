// features/execution-player/Player.tsx
// 从 store 读取数据的分步播放器

import { useEffect } from 'react'
import { useDemoStore } from '../../stores/demoStore'
import { useConversationStore } from '../../stores/conversationStore'
import { usePlaybackStore } from '../../stores/playbackStore'
import { MermaidRenderer } from '../animation/MermaidRenderer'
import { SqlSimulator, type SqlSimulatorStep } from '../animation/SqlSimulator'
import type { SimulationData } from '../../lib/types'
import { QuizPanel } from '../quiz/QuizPanel'

export function ExecutionPlayer() {
  const currentDemo = useDemoStore(s => s.currentDemo)
  const messageCount = useConversationStore(s => s.messages.length)
  const currentStepIndex = usePlaybackStore(s => s.currentStepIndex)
  const isPlaying = usePlaybackStore(s => s.isPlaying)
  const nextStep = usePlaybackStore(s => s.nextStep)
  const prevStep = usePlaybackStore(s => s.prevStep)
  const seekTo = usePlaybackStore(s => s.seekTo)
  const togglePlay = usePlaybackStore(s => s.togglePlay)
  const reset = usePlaybackStore(s => s.reset)
  const setAdaptiveMode = usePlaybackStore(s => s.setAdaptiveMode)

  const steps = currentDemo?.steps || []
  const step = steps[currentStepIndex]

  // Reset on new demo
  useEffect(() => {
    reset()
  }, [currentDemo?.id])

  // Auto-play
  useEffect(() => {
    if (!isPlaying || !currentDemo) return
    const ms = currentDemo.playback?.defaultStepDurationMs || 5000
    const timer = setInterval(() => {
      nextStep(steps.length)
    }, ms)
    return () => clearInterval(timer)
  }, [isPlaying, currentDemo, steps.length, nextStep])

  // Keyboard
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
      switch (e.key) {
        case 'ArrowLeft': prevStep(); break
        case 'ArrowRight': nextStep(steps.length); break
        case ' ': e.preventDefault(); togglePlay(); break
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [steps.length, prevStep, nextStep, togglePlay])

  if (!currentDemo) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-300 text-sm text-center px-4">
        {messageCount > 0
          ? '当前对话暂未生成可播放演示，请发送知识点、案例或 SQL。'
          : '尚未生成演示。先在左侧输入知识点、案例或 SQL。'}
      </div>
    )
  }
  if (!step) return null

  return (
    <div className="flex-1 flex flex-col">
      {/* Progress bar */}
      <div className="flex gap-1.5 mb-4 px-2">
        {steps.map((s, i) => (
          <button
            key={s.id}
            onClick={() => seekTo(i)}
            className={`flex-1 h-1.5 rounded-full transition-all cursor-pointer
              ${i < currentStepIndex ? 'bg-blue-400' : ''}
              ${i === currentStepIndex ? 'bg-blue-600 h-2' : ''}
              ${i > currentStepIndex ? 'bg-gray-200' : ''}
            `}
          />
        ))}
      </div>

      {/* Phase panel */}
      <div className="flex-1 overflow-y-auto px-2 space-y-3">
        <PhaseEvidence
          step={step}
          stepIndex={currentStepIndex}
          totalSteps={steps.length}
          simulationData={currentDemo.simulationData}
        />
      </div>

      {/* Controls */}
      <div className="flex items-center justify-center gap-3 pt-4 border-t border-gray-100 mt-2">
        <button
          onClick={prevStep}
          disabled={currentStepIndex === 0 || isPlaying}
          className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 disabled:opacity-30 flex items-center justify-center text-sm transition-colors"
        >
          ←
        </button>
        <button
          onClick={togglePlay}
          disabled={currentStepIndex >= steps.length - 1}
          className="w-10 h-10 rounded-full bg-blue-600 hover:bg-blue-700 text-white flex items-center justify-center text-sm transition-colors"
        >
          {isPlaying ? '⏸' : '▶'}
        </button>
        <button
          onClick={() => nextStep(steps.length)}
          disabled={currentStepIndex >= steps.length - 1 || isPlaying}
          className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 disabled:opacity-30 flex items-center justify-center text-sm transition-colors"
        >
          →
        </button>
        <span className="text-xs text-gray-400 ml-2">
          {currentStepIndex + 1} / {steps.length}
        </span>
        <button
          onClick={() => setAdaptiveMode(true)}
          className="text-[10px] text-gray-400 hover:text-blue-600 ml-2"
          title="自适应模式"
        >
          🧠
        </button>
      </div>
    </div>
  )
}

/* ─── Phase Evidence Panel ─── */

function mapToSimulatorIndex(workflowIndex: number, workflowTotal: number, simTotal: number): number {
  if (simTotal <= 1 || workflowTotal <= 1) return 0
  return Math.min(
    simTotal - 1,
    Math.round((workflowIndex / (workflowTotal - 1)) * (simTotal - 1)),
  )
}

function PhaseEvidence({
  step,
  stepIndex,
  totalSteps,
  simulationData,
}: {
  step: any
  stepIndex: number
  totalSteps: number
  simulationData?: SimulationData
}) {
  const simSteps = (simulationData?.sqlSimulator?.steps ?? []) as SqlSimulatorStep[]
  const simIndex =
    simSteps.length > 0 ? mapToSimulatorIndex(stepIndex, totalSteps, simSteps.length) : 0

  const labels: Record<string, string> = {
    lex: '词法分析', parse: '语法分析', optimize: '查询优化',
    plan: '执行计划', execute: '执行过程', result: '结果集',
    concept: '概念', transform: '变换', compare: '对比', summary: '总结',
  }

  return (
    <>
      <div className="flex items-center gap-2">
          <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded-full bg-blue-50 text-blue-600">
          {step.workflowPhase}
        </span>
        <span className="text-xs text-gray-500 font-medium">
          {labels[step.workflowPhase] || step.workflowPhase}
        </span>
        {step.groundingRef && (
          <span className="text-[10px] text-green-600 bg-green-50 px-1.5 py-0.5 rounded-full">
            有证据
          </span>
        )}
      </div>

      <p className="text-sm leading-relaxed text-gray-700 bg-gray-50 rounded-xl px-3 py-2">
        {step.narration?.zh || step.narration?.en || '等待 AI 生成讲解词...'}
      </p>

      {simSteps.length > 0 && (
        <div className="mb-3">
          <SqlSimulator steps={simSteps} activeIndex={simIndex} />
        </div>
      )}

      {/* Mermaid visualization for each phase */}
      <div className="mb-3">
        <MermaidRenderer phase={step.workflowPhase} />
      </div>

      {renderEvidence(step)}

      {/* Quiz for current step */}
      <div className="mt-3">
        <QuizPanel stepIndex={step.order - 1} question={step.quiz || {} as any} />
      </div>
    </>
  )
}

function renderEvidence(step: any) {
  const ev = step.engineEvidence
  if (!ev) return null
  switch (step.workflowPhase) {
    case 'lex': return <LexPanel ev={ev} />
    case 'parse': return <ParsePanel ev={ev} />
    case 'optimize': return <OptimizePanel ev={ev} />
    case 'plan': return <PlanPanel ev={ev} enginePlan={step.enginePlan} />
    case 'execute': return <ExecutePanel ev={ev} enginePlan={step.enginePlan} />
    default: return null
  }
}

/* ─── Sub-panels ─── */

function LexPanel({ ev }: { ev: Record<string, unknown> }) {
  const tokens = (ev.tokens as string[]) || []
  return (
    <Panel title="词法分析">
      <div className="flex flex-wrap gap-1.5">
        {tokens.map((t, i) => (
          <span key={i} className="bg-blue-100 text-blue-700 text-xs font-mono px-2 py-0.5 rounded">{t}</span>
        ))}
      </div>
      <div className="text-[11px] text-gray-400 mt-1.5">
        共识别 {(ev.token_count as number) ?? '?'} 个词元
      </div>
    </Panel>
  )
}

function ParsePanel({ ev }: { ev: Record<string, unknown> }) {
  const tables = (ev.tables as string[]) || []
  const flags = [
    { key: 'has_join', label: 'JOIN' }, { key: 'has_where', label: 'WHERE' },
    { key: 'has_group_by', label: 'GROUP BY' }, { key: 'has_order_by', label: 'ORDER BY' },
  ]
  return (
    <Panel title="语法分析结果">
      <div className="mb-2">
        <div className="text-xs text-gray-400 mb-1">涉及表</div>
        <div className="flex flex-wrap gap-1.5">
          {tables.length > 0 ? tables.map((t, i) => (
            <span key={i} className="bg-purple-100 text-purple-700 text-xs font-mono px-2 py-0.5 rounded">{t}</span>
          )) : <span className="text-xs text-gray-300">(无)</span>}
        </div>
      </div>
      <div className="flex flex-wrap gap-2">
        {flags.map(f => (
          <span key={f.key}
            className={`text-xs px-2 py-0.5 rounded-full ${ev[f.key] ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-300'}`}>
            {f.label} {ev[f.key] ? '✓' : '—'}
          </span>
        ))}
      </div>
    </Panel>
  )
}

function OptimizePanel({ ev }: { ev: Record<string, unknown> }) {
  const scanLabels: Record<string, string> = {
    unknown: '未知', full_table_scan: '全表扫描 (Full Table Scan)',
    index_lookup: '索引查找 (Index Lookup)', index_only_scan: '索引覆盖扫描 (Index Only)',
    nested_loop_join: '嵌套循环连接 (Nested Loop Join)', hash_join: '哈希连接 (Hash Join)',
  }
  const scanType = (ev.scan_type as string) || 'unknown'
  return (
    <Panel title="查询优化">
      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400">扫描方式</span>
          <span className="text-sm font-mono text-yellow-700 bg-yellow-50 px-2 py-0.5 rounded">
            {scanLabels[scanType] || scanType}
          </span>
        </div>
        <div className="text-xs text-gray-400">涉及 {(ev.table_count as number) ?? '?'} 张表</div>
      </div>
    </Panel>
  )
}

function PlanPanel({ ev, enginePlan }: { ev: Record<string, unknown>; enginePlan?: Record<string, unknown> }) {
  return (
    <Panel title="执行计划">
      <div className="grid grid-cols-2 gap-2 mb-3">
        <CostCard engine="MySQL" cost={ev.mysql_cost as number | null} />
        <CostCard engine="PostgreSQL" cost={ev.pg_cost as number | null} />
      </div>
      {enginePlan && (
        <details open>
          <summary className="text-xs text-gray-400 cursor-pointer hover:text-gray-600 mb-1">EXPLAIN JSON</summary>
          <div className="bg-gray-900 text-green-300 text-[10px] font-mono rounded-lg p-3 max-h-48 overflow-auto leading-relaxed">
            {!!enginePlan.mysql && <JSONTree label="MySQL" data={enginePlan.mysql} />}
            {!!enginePlan.postgres && <JSONTree label="PostgreSQL" data={enginePlan.postgres} />}
          </div>
        </details>
      )}
    </Panel>
  )
}

function ExecutePanel({ ev, enginePlan: _enginePlan }: { ev: Record<string, unknown>; enginePlan?: Record<string, unknown> }) {
  return (
    <Panel title="执行过程">
      <div className="bg-yellow-50 rounded-lg px-3 py-2 mb-2 inline-block">
        <div className="text-[10px] uppercase text-yellow-600">估计扫描行数</div>
        <div className="text-lg font-mono text-yellow-800">
          {ev.rows_estimate !== null && ev.rows_estimate !== undefined
            ? (ev.rows_estimate as number).toLocaleString()
            : <span className="text-gray-300 text-sm">未知</span>}
        </div>
      </div>
    </Panel>
  )
}

function CostCard({ engine, cost }: { engine: string; cost: number | null }) {
  return (
    <div className="bg-gray-50 rounded-lg px-3 py-2">
      <div className="text-[10px] uppercase text-gray-400">{engine}</div>
      <div className="text-xs font-mono mt-0.5">
        {cost !== null && cost !== undefined ? `${cost.toLocaleString()}` : <span className="text-gray-300">N/A</span>}
      </div>
      <div className="text-[9px] text-gray-300">cost units</div>
    </div>
  )
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="border border-gray-200 rounded-xl px-3 py-2.5 bg-white">
      <div className="text-[11px] font-medium text-gray-400 mb-2 uppercase tracking-wider">{title}</div>
      {children}
    </div>
  )
}

function JSONTree({ label, data }: { label: string; data: unknown }) {
  const text = JSON.stringify(data, null, 2)
  if (text === 'null') return null
  return (
    <div className="mb-2 last:mb-0">
      <div className="text-gray-400 text-[9px] mb-0.5">{label}</div>
      <pre className="whitespace-pre-wrap break-all">{text.slice(0, 2000)}</pre>
      {text.length > 2000 && <span className="text-gray-500">... (truncated)</span>}
    </div>
  )
}
