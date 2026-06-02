import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import type { DemoPackage } from './TeachPage'
import { ExecutionPlayer } from '../features/execution-player/Player'

export default function ClassroomPage() {
  const { id } = useParams<{ id: string }>()
  const [demo, setDemo] = useState<DemoPackage | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 从 API 加载演示数据
    fetch(`/api/demos/${id || 'dp_20260601_join'}`)
      .then(r => r.json())
      .then(setDemo)
      .catch(err => {
        console.error('加载演示失败:', err)
        // 降级到本地内嵌数据
        import('../data/join-query.json').then(m => setDemo(m.default || m))
      })
      .finally(() => setLoading(false))
  }, [id])

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-8 text-center text-gray-400">
        <div className="animate-pulse text-2xl">加载演示中...</div>
      </div>
    )
  }

  if (!demo) {
    return (
      <div className="max-w-4xl mx-auto p-8 text-center text-gray-400">
        演示不存在
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* 全屏播放模式 */}
      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100">
          <h1 className="text-xl font-semibold">{demo.title.zh}</h1>
          <p className="text-sm text-gray-500">{demo.title.en}</p>
        </div>
        <div className="p-6">
          <ExecutionPlayer demo={demo} />
        </div>
      </div>
    </div>
  )
}
