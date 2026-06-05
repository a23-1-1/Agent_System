// features/chat/ChatHeader.tsx
// 对话标题栏 + 搜索toggle + 清空历史按钮

import type { ConversationSummary } from '../../lib/types'
import { useConversationStore } from '../../stores/conversationStore'

interface Props {
  conv: ConversationSummary | null
  showSearch: boolean
  onToggleSearch: () => void
}

export function ChatHeader({ conv, showSearch, onToggleSearch }: Props) {
  const clearMessages = useConversationStore(s => s.clearMessages)

  if (!conv) {
    return (
      <div className="px-4 py-2 border-b border-gray-100 text-xs font-medium text-gray-400">
        选择一个课程对话开始
      </div>
    )
  }

  const statusLabels: Record<string, string> = {
    active: '对话中',
    draft: '草稿',
    finalized: '已定稿',
    archived: '已归档',
  }

  return (
    <div className="px-4 py-2 border-b border-gray-100 flex items-center justify-between">
      <div className="flex items-center gap-2 min-w-0">
        <span className="text-xs font-semibold text-gray-700 truncate">{conv.title}</span>
        <span className="text-[9px] text-gray-400 bg-gray-100 rounded px-1 py-0.5 whitespace-nowrap">
          {statusLabels[conv.status] || conv.status}
        </span>
        <span className="text-[9px] text-gray-300 whitespace-nowrap">{conv.messageCount} 条</span>
      </div>
      <div className="flex items-center gap-1">
        <button
          onClick={onToggleSearch}
          className={`text-[10px] px-1.5 py-0.5 rounded transition-colors ${
            showSearch ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600'
          }`}
          title="搜索消息"
        >
          🔍
        </button>
        <button
          onClick={() => {
            if (conv.messageCount > 0 && confirm(`清空「${conv.title}」的所有课程消息？`)) {
              clearMessages(conv.id)
            }
          }}
          className="text-[10px] text-gray-400 hover:text-red-500 px-1.5 py-0.5 rounded transition-colors"
          title="清空历史"
        >
          🗑
        </button>
      </div>
    </div>
  )
}
