import { useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useDemoStore } from '../stores/demoStore'
import { usePlaybackStore } from '../stores/playbackStore'
import { ExecutionPlayer } from '../features/execution-player/Player'
import type { DemoPackage } from '../lib/types'

export default function StudentPage() {
  const { demoId } = useParams<{ demoId: string }>()
  const currentDemo = useDemoStore(s => s.currentDemo)
  const currentStepIndex = usePlaybackStore(s => s.currentStepIndex)
  const masteryLevel = usePlaybackStore(s => s.masteryLevel)
  const recordQuizAnswer = usePlaybackStore(s => s.recordQuizAnswer)
  const step = currentDemo?.steps?.[currentStepIndex]

  useEffect(() => {
    const id = demoId || 'dp_20260601_join'
    fetch(`/api/demos/${id}`)
      .then(r => r.json())
      .then(d => useDemoStore.getState().setDemo(d))
      .catch(() => import('../data/join-query.json').then(m => useDemoStore.getState().setDemo((m.default || m) as unknown as DemoPackage)))
  }, [demoId])

  if (!currentDemo) {
    return <div className="max-w-3xl mx-auto p-8 text-center text-gray-400">加载中...</div>
  }

  return (
    <div className="max-w-3xl mx-auto p-4">
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="px-5 py-3 border-b border-gray-100 bg-gray-50/50 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold">{currentDemo.title.zh}</h1>
            <p className="text-xs text-gray-400">只读模式 · {currentDemo.steps.length} 步</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-400">掌握度</span>
            <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-green-500 rounded-full transition-all" style={{ width: `${masteryLevel}%` }} />
            </div>
            <span className="text-xs font-mono text-gray-500">{masteryLevel}%</span>
          </div>
        </div>
        <div className="p-4">
          <ExecutionPlayer />
        </div>

        {/* Quiz */}
        {step?.quiz && (
          <div className="px-5 py-4 border-t border-gray-100">
            <h3 className="text-sm font-medium text-gray-700 mb-2">📝 知识点测验</h3>
            <p className="text-sm text-gray-600 mb-3">{step.quiz.question}</p>
            <div className="space-y-2">
              {step.quiz.options.map((opt: string, i: number) => (
                <button
                  key={i}
                  onClick={() => recordQuizAnswer(
                    step.quiz?.id || `q_${currentStepIndex}`, i, step.quiz?.answer ?? 0
                  )}
                  className="w-full text-left px-3 py-2 rounded-lg border border-gray-200 text-sm hover:bg-blue-50 hover:border-blue-300 transition-colors"
                >
                  {String.fromCharCode(65 + i)}. {opt}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
