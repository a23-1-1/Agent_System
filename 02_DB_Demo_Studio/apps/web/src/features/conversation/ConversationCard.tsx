// features/conversation/ConversationCard.tsx
import type { ConversationSummary } from '../../lib/types'

interface Props {
  conv: ConversationSummary
  isActive: boolean
  onClick: () => void
  onRename: (title: string) => void
  onDelete: () => void
}

const TYPE_LABELS: Record<string, string> = {
  p0: 'P0', p1: 'P1', p2: 'P2',
}
const STATUS_DOTS: Record<string, string> = {
  active: 'bg-green-400',
  draft: 'bg-yellow-400',
  finalized: 'bg-blue-400',
  archived: 'bg-gray-300',
}

export function ConversationCard({ conv, isActive, onClick, onRename, onDelete }: Props) {
  const date = new Date(conv.lastActivity)
  const dateStr = date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })

  return (
    <div
      onClick={onClick}
      className={`group relative px-3 py-2.5 cursor-pointer border-b border-gray-100 transition-colors
        ${isActive ? 'bg-blue-50 border-l-2 border-l-blue-500' : 'hover:bg-gray-50 border-l-2 border-l-transparent'}`}
    >
      <div className="flex items-center gap-2 mb-1">
        <span className={`w-2 h-2 rounded-full ${STATUS_DOTS[conv.status] || 'bg-gray-300'}`} />
        <span className="text-xs font-medium text-gray-800 truncate flex-1">{conv.title}</span>
        {conv.demoType !== 'standard' && (
          <span className="text-[10px] font-mono text-gray-400 bg-gray-100 rounded px-1">
            {TYPE_LABELS[conv.demoType] || ''}
          </span>
        )}
      </div>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3 text-[10px] text-gray-400 truncate">
          <span>{dateStr}</span>
          <span>{conv.messageCount} 条</span>
          {conv.curriculumNode && (
            <span className="text-gray-300 truncate max-w-[90px]">{conv.curriculumNode}</span>
          )}
          {conv.summary && (
            <span className="text-gray-300 truncate max-w-[120px]">{conv.summary}</span>
          )}
        </div>
      </div>

      {/* Hover actions */}
      <div className="absolute right-2 top-2 hidden group-hover:flex gap-1">
        <button
          onClick={(e) => { e.stopPropagation(); const t = prompt('重命名:', conv.title); if (t) onRename(t) }}
          className="text-[10px] text-gray-400 hover:text-blue-600 bg-white rounded px-1 py-0.5 shadow-sm"
        >
          重命名
        </button>
        <button
          onClick={(e) => { e.stopPropagation(); if (confirm('删除此对话？')) onDelete() }}
          className="text-[10px] text-gray-400 hover:text-red-600 bg-white rounded px-1 py-0.5 shadow-sm"
        >
          删除
        </button>
      </div>
    </div>
  )
}
