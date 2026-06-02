// features/chat/MessageBubble.tsx
// 单条消息组件：头像/角色/时间戳/hover 操作菜单

import type { Message } from '../../lib/types'

interface Props {
  message: Message
  onDelete?: (msgId: string) => void
}

export function MessageBubble({ message, onDelete }: Props) {
  const isUser = message.role === 'user'
  const time = formatTime(message.createdAt)

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} group`}>
      {/* AI avatar */}
      {!isUser && (
        <div className="w-7 h-7 rounded-full bg-blue-100 text-blue-600 text-[10px] font-bold flex items-center justify-center flex-shrink-0 mt-1 mr-2">
          AI
        </div>
      )}

      <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col`}>
        {/* Role + Time */}
        <div className={`flex items-center gap-2 mb-0.5 ${isUser ? 'flex-row-reverse' : ''}`}>
          <span className="text-[10px] text-gray-400 font-medium">
            {isUser ? '你' : 'AI'}
          </span>
          <span className="text-[9px] text-gray-300">{time}</span>
        </div>

        {/* Message body */}
        <div className={`relative rounded-xl px-3 py-2 whitespace-pre-wrap text-sm ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-md'
            : 'bg-gray-100 text-gray-700 rounded-bl-md'
        }`}>
          {message.deleted ? (
            <span className="italic text-gray-400 text-xs">[消息已删除]</span>
          ) : (
            <>
              {message.content.text}
              {message.content.sql && (
                <div className="mt-1 text-[10px] font-mono opacity-60">{message.content.sql}</div>
              )}
            </>
          )}
        </div>

        {/* AI metadata */}
        {!isUser && message.metadata?.model && (
          <div className="text-[9px] text-gray-300 mt-0.5">
            {message.metadata.model} · {message.metadata.tokensUsed || '?'} tokens
          </div>
        )}
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="w-7 h-7 rounded-full bg-gray-200 text-gray-500 text-[10px] font-bold flex items-center justify-center flex-shrink-0 mt-1 ml-2">
          U
        </div>
      )}

      {/* Hover actions */}
      {onDelete && !message.deleted && (
        <div className="opacity-0 group-hover:opacity-100 transition-opacity self-center ml-1">
          <button
            onClick={() => onDelete(message.id)}
            className="text-[9px] text-gray-300 hover:text-red-500 bg-white rounded px-1 py-0.5 shadow-sm border border-gray-100"
            title="删除消息"
          >
            ✕
          </button>
        </div>
      )}
    </div>
  )
}

function formatTime(iso: string): string {
  try {
    const d = new Date(iso)
    if (isNaN(d.getTime())) return iso.slice(11, 16) || ''
    return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}
