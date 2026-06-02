import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import type { DemoPackage } from './TeachPage'
import { ExecutionPlayer } from '../features/execution-player/Player'

export default function StudentPage() {
  const { id } = useParams<{ id: string }>()
  const [demo, setDemo] = useState<DemoPackage | null>(null)

  useEffect(() => {
    fetch(`/api/demos/${id || 'dp_20260601_join'}`)
      .then(r => r.json())
      .then(setDemo)
      .catch(() => import('../data/join-query.json').then(m => setDemo(m.default || m)))
  }, [id])

  if (!demo) {
    return <div className="max-w-3xl mx-auto p-8 text-center text-gray-400">加载中...</div>
  }

  return (
    <div className="max-w-3xl mx-auto p-4">
      {/* 学生视图：只读播放器，无编辑控件 */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="px-5 py-3 border-b border-gray-100 bg-gray-50/50">
          <h1 className="text-lg font-semibold">{demo.title.zh}</h1>
          <p className="text-xs text-gray-400">只读模式 · {demo.steps.length} 步</p>
        </div>
        <div className="p-4">
          <ExecutionPlayer demo={demo} />
        </div>
      </div>
    </div>
  )
}
