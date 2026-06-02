import { useEffect, useState } from 'react'
import type { DemoPackage } from '../../pages/TeachPage'

interface Props {
  demo: DemoPackage | null
}

export function ExecutionPlayer({ demo }: Props) {
  const [current, setCurrent] = useState(0)
  const [playing, setPlaying] = useState(false)

  const steps = demo?.steps || []

  useEffect(() => {
    setCurrent(0)
    setPlaying(false)
  }, [demo])

  useEffect(() => {
    if (!playing || !demo) return
    const ms = demo.playback.defaultStepDurationMs || 5000
    const timer = setInterval(() => {
      setCurrent(prev => {
        if (prev >= steps.length - 1) {
          setPlaying(false)
          return prev
        }
        return prev + 1
      })
    }, ms)
    return () => clearInterval(timer)
  }, [playing, demo, steps.length])

  // 键盘控制
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
      switch (e.key) {
        case 'ArrowLeft':  setCurrent(c => Math.max(0, c - 1)); break
        case 'ArrowRight': setCurrent(c => Math.min(steps.length - 1, c + 1)); break
        case ' ': e.preventDefault(); setPlaying(p => !p); break
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [steps.length])

  if (!demo) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-300 text-sm">
        等待生成演示...
      </div>
    )
  }

  const step = steps[current]
  if (!step) return null

  const labels: Record<string, string> = {
    lex: '词法分析', parse: '语法分析', optimize: '查询优化',
    plan: '执行计划', execute: '执行过程', result: '结果集',
    concept: '概念', transform: '变换', compare: '对比', summary: '总结',
  }

  return (
    <div className="flex-1 flex flex-col">
      {/* 进度条 */}
      <div className="flex gap-1.5 mb-4 px-2">
        {steps.map((s, i) => (
          <button
            key={s.id}
            onClick={() => setCurrent(i)}
            className={`flex-1 h-1.5 rounded-full transition-all cursor-pointer
              ${i < current ? 'bg-blue-400' : ''}
              ${i === current ? 'bg-blue-600 h-2' : ''}
              ${i > current ? 'bg-gray-200' : ''}
            `}
          />
        ))}
      </div>

      {/* 当前步骤信息 */}
      <div className="flex items-center gap-2 mb-3 px-2">
        <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded-full bg-blue-50 text-blue-600">
          {step.workflowPhase}
        </span>
        <span className="text-xs text-gray-500">
          {labels[step.workflowPhase] || step.workflowPhase}
        </span>
        {step.groundingRef && (
          <span className="text-[10px] text-green-600">ⓘ EXPLAIN</span>
        )}
      </div>

      {/* 讲解词 */}
      <div className="flex-1 px-2">
        <p className="text-sm leading-relaxed text-gray-700">
          {step.narration?.zh || '等待 AI 生成讲解词...'}
        </p>
      </div>

      {/* 控制栏 */}
      <div className="flex items-center justify-center gap-3 pt-4 border-t border-gray-100 mt-2">
        <button
          onClick={() => setCurrent(c => Math.max(0, c - 1))}
          disabled={current === 0}
          className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 disabled:opacity-30 flex items-center justify-center text-sm transition-colors"
        >
          ←
        </button>
        <button
          onClick={() => setPlaying(p => !p)}
          className="w-10 h-10 rounded-full bg-blue-600 hover:bg-blue-700 text-white flex items-center justify-center text-sm transition-colors"
        >
          {playing ? '⏸' : '▶'}
        </button>
        <button
          onClick={() => setCurrent(c => Math.min(steps.length - 1, c + 1))}
          disabled={current >= steps.length - 1}
          className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 disabled:opacity-30 flex items-center justify-center text-sm transition-colors"
        >
          →
        </button>
        <span className="text-xs text-gray-400 ml-2">
          {current + 1} / {steps.length}
        </span>
      </div>
    </div>
  )
}
