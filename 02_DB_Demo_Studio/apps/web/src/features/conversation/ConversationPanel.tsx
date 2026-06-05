// features/conversation/ConversationPanel.tsx
import { useState } from 'react'
import { useConversationStore } from '../../stores/conversationStore'
import { ConversationCard } from './ConversationCard'
import { ConversationSearch } from './ConversationSearch'

interface Props {
  activeConvId: string | null
  onSwitchConv: (convId: string) => void
  onCreateConv: () => Promise<void>
}

export function ConversationPanel({ activeConvId, onSwitchConv, onCreateConv }: Props) {
  const conversations = useConversationStore(s => s.conversations)
  const deleteConv = useConversationStore(s => s.deleteConversation)
  const renameConv = useConversationStore(s => s.renameConversation)
  const [search, setSearch] = useState('')

  const filtered = search
    ? conversations.filter(c =>
        c.title.toLowerCase().includes(search.toLowerCase()) ||
        c.summary?.toLowerCase().includes(search.toLowerCase()) ||
        c.curriculumNode?.toLowerCase().includes(search.toLowerCase())
      )
    : conversations

  return (
    <div className="flex flex-col h-full bg-gray-50 border-r border-gray-200">
      {/* Header */}
      <div className="px-3 py-3 border-b border-gray-200">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-sm font-semibold text-gray-700">对话列表</h2>
          <button
            onClick={onCreateConv}
            className="text-xs bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-3 py-1.5 transition-colors"
          >
            + 新建
          </button>
        </div>
        <ConversationSearch value={search} onChange={setSearch} />
      </div>

      {/* List */}
      <div className="flex-1 overflow-y-auto">
        {filtered.length === 0 && (
          <div className="text-center text-gray-300 text-xs mt-8">
            {search ? '无匹配对话' : '暂无对话，点击"新建"开始'}
          </div>
        )}
        {filtered.map(conv => (
          <ConversationCard
            key={conv.id}
            conv={conv}
            isActive={conv.id === activeConvId}
            onClick={() => onSwitchConv(conv.id)}
            onRename={(title) => renameConv(conv.id, title)}
            onDelete={() => deleteConv(conv.id)}
          />
        ))}
      </div>
    </div>
  )
}
