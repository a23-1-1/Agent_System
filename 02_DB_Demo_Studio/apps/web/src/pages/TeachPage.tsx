import { useState } from 'react'
import { ChatPanel } from '../features/ai-studio/ChatPanel'
import { FlowEditor } from '../features/flow-editor/FlowEditor'
import { ExecutionPlayer } from '../features/execution-player/Player'

export default function TeachPage() {
  const [currentDemo, setCurrentDemo] = useState<DemoPackage | null>(null)

  return (
    <div className="max-w-7xl mx-auto p-4">
      {/* 三栏布局：左侧对话 | 中间流程图 | 右侧预览 */}
      <div className="grid grid-cols-4 gap-4" style={{height: 'calc(100vh - 80px)'}}>
        {/* 左侧对话区 */}
        <div className="col-span-1 bg-white rounded-xl border border-gray-200 overflow-hidden flex flex-col">
          <div className="px-4 py-3 border-b border-gray-100 font-medium text-sm text-gray-700">
            AI Studio 对话
          </div>
          <ChatPanel onDemoUpdate={setCurrentDemo} />
        </div>

        {/* 中间拖拽编辑区 */}
        <div className="col-span-2 bg-white rounded-xl border border-gray-200 overflow-hidden flex flex-col">
          <div className="px-4 py-3 border-b border-gray-100 font-medium text-sm text-gray-700">
            步骤编辑器
          </div>
          <FlowEditor demo={currentDemo} />
        </div>

        {/* 右侧实时预览 */}
        <div className="col-span-1 bg-white rounded-xl border border-gray-200 overflow-hidden flex flex-col">
          <div className="px-4 py-3 border-b border-gray-100 font-medium text-sm text-gray-700">
            实时预览
          </div>
          <ExecutionPlayer demo={currentDemo} />
        </div>
      </div>
    </div>
  )
}

// 类型定义（后续放到 @/types）
export interface DemoPackage {
  id: string
  title: { zh: string; en: string }
  steps: DemoStep[]
  metadata: { teacherVersion: number }
  playback: { defaultStepDurationMs: number }
}

export interface DemoStep {
  id: string
  order: number
  workflowPhase: string
  narration: { zh: string; en: string; source: string }
  visuals?: { type: string; highlightRange?: number[] }
  groundingRef?: string | null
}
