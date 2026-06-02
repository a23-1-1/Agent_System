import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useDemoStore } from '../stores/demoStore'
import { ExecutionPlayer } from '../features/execution-player/Player'
import type { DemoPackage } from '../lib/types'

export default function ClassroomPage() {
  const { convId } = useParams<{ convId: string }>()
  const currentDemo = useDemoStore(s => s.currentDemo)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const demoId = 'dp_20260601_join'
    fetch(`/api/demos/${demoId}`)
      .then(r => r.json())
      .then(demo => useDemoStore.getState().setDemo(demo))
      .catch(() => import('../data/join-query.json').then(m => useDemoStore.getState().setDemo((m.default || m) as unknown as DemoPackage)))
      .finally(() => setLoading(false))
  }, [convId])

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-8 text-center text-gray-400">
        <div className="animate-pulse text-2xl">加载演示中...</div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100">
          <h1 className="text-xl font-semibold">{currentDemo?.title?.zh || '课堂演示'}</h1>
          <p className="text-sm text-gray-500">{currentDemo?.title?.en}</p>
        </div>
        <div className="p-6">
          <ExecutionPlayer />
        </div>
      </div>
    </div>
  )
}
