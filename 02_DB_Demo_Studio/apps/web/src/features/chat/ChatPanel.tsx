// features/chat/ChatPanel.tsx — WebSocket 驱动的 AI 对话面板
// 消息历史管理：日期分隔 + 时间戳 + 删除 + 搜索

import { useState, useRef, useEffect, useMemo } from 'react'
import { useConversationStore } from '../../stores/conversationStore'
import { useDemoStore } from '../../stores/demoStore'
import type { WsClient } from '../../lib/ws-client'
import type { Message } from '../../lib/types'
import { MessageBubble } from './MessageBubble'
import { ChatHeader } from './ChatHeader'
import { AgentThinkingChain } from './AgentThinkingChain'
import { QuickActions } from './QuickActions'
import { DemoSnapshotIndicator } from './DemoSnapshotIndicator'

interface Props {
  wsClient: WsClient | null
  activeConvId: string | null
}

export function ChatPanel({ wsClient, activeConvId }: Props) {
  const messages = useConversationStore(s => s.messages)
  const conversations = useConversationStore(s => s.conversations)
  const generationStatus = useConversationStore(s => s.generationStatus)
  const setGenerationStatus = useConversationStore(s => s.setGenerationStatus)
  const appendMessage = useConversationStore(s => s.appendMessage)
  const createConversation = useConversationStore(s => s.createConversation)
  const switchConversation = useConversationStore(s => s.switchConversation)
  const deleteMessage = useConversationStore(s => s.deleteMessage)
  const currentDemo = useDemoStore(s => s.currentDemo)
  const [input, setInput] = useState('')
  const [thinking, setThinking] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [showSearch, setShowSearch] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const chatEndRef = useRef<HTMLDivElement>(null)
  const searchInputRef = useRef<HTMLInputElement>(null)

  const activeConv = conversations.find(c => c.id === activeConvId) || null

  // Auto scroll to bottom on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, thinking])

  // Focus search input when opened
  useEffect(() => {
    if (showSearch) searchInputRef.current?.focus()
  }, [showSearch])

  // Filter messages by search
  const filteredMessages = useMemo(() => {
    if (!searchQuery.trim()) return messages
    const q = searchQuery.toLowerCase()
    return messages.filter(m =>
      m.content.text?.toLowerCase().includes(q) ||
      m.content.sql?.toLowerCase().includes(q)
    )
  }, [messages, searchQuery])

  const send = () => {
    if (!input.trim() || !wsClient || !activeConvId || generationStatus === 'streaming') return

    const text = input
    setInput('')
    setThinking('')
    setErrorMessage('')
    setGenerationStatus('streaming')

    const sqlMatch = text.match(/(SELECT|INSERT|UPDATE|DELETE|CREATE).*/is)
    const sql = sqlMatch ? sqlMatch[0].trim() : undefined

    // Optimistic user message for better send feedback
    appendMessage({
      id: `local_${Date.now()}`,
      convId: activeConvId,
      role: 'user',
      type: 'text',
      content: { text, sql },
      createdAt: new Date().toISOString(),
    })

    wsClient.send({
      type: 'chat:message',
      convId: activeConvId,
      content: { text, sql },
    })
  }

  const handleQuickAction = (action: string) => {
    const prompts: Record<string, string> = {
      viz: '为当前演示添加 Mermaid 可视化',
      quiz: '给当前知识点出两道选择题',
      engine: '对比 MySQL 和 PostgreSQL 的执行计划',
      tts: '为讲解词生成 TTS 配音',
      export: '导出当前演示',
      model: '切换到 Claude 模型重新生成',
    }
    const prompt = prompts[action]
    if (prompt && wsClient && activeConvId) {
      setInput(prompt)
    }
  }

  const handleDelete = (msgId: string) => {
    if (activeConvId && wsClient) {
      wsClient.send({
        type: 'message:delete' as any,
        convId: activeConvId,
        msgId,
      })
    }
    deleteMessage(activeConvId || '', msgId)
  }

  // Listen for agent:thinking events
  useEffect(() => {
    if (!wsClient) return
    const unsub = wsClient.onEvent((evt) => {
      if (evt.type === 'agent:thinking') {
        setThinking(evt.content)
      }
      if (evt.type === 'error') {
        setErrorMessage(evt.message || '生成失败，请重试')
        setGenerationStatus('idle')
      }
    })
    return unsub
  }, [wsClient, setGenerationStatus])

  // Group messages by date for date separators
  const groupedMessages = useMemo(() => {
    const groups: { date: string; label: string; msgs: Message[] }[] = []
    let lastDate = ''

    for (const msg of filteredMessages) {
      const dateKey = msg.createdAt?.slice(0, 10) || 'unknown'
      if (dateKey !== lastDate) {
        groups.push({ date: dateKey, label: formatDateLabel(dateKey), msgs: [] })
        lastDate = dateKey
      }
      groups[groups.length - 1].msgs.push(msg)
    }
    return groups
  }, [filteredMessages])

  return (
    <div className="flex flex-col h-full">
      {/* Header with title + search + clear */}
      {activeConv && (
        <ChatHeader
          conv={activeConv}
          showSearch={showSearch}
          onToggleSearch={() => setShowSearch(!showSearch)}
        />
      )}

      {/* Search bar */}
      {showSearch && (
        <div className="px-3 py-2 border-b border-gray-100 bg-gray-50">
          <input
            ref={searchInputRef}
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="搜索消息内容..."
            className="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-blue-400"
          />
          {searchQuery && (
            <div className="text-[10px] text-gray-400 mt-1">
              找到 {filteredMessages.length} 条匹配消息
            </div>
          )}
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-4 text-sm">
        {!activeConvId && (
          <div className="text-center text-gray-400 mt-8 space-y-3">
            <p className="text-sm">当前没有可用对话，先创建一个再开始。</p>
            <button
              onClick={async () => {
                const id = await createConversation('新对话')
                if (id) await switchConversation(id)
              }}
              className="text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 transition-colors"
            >
              新建对话
            </button>
          </div>
        )}

        {messages.length === 0 && !searchQuery && (
          <div className="text-center text-gray-300 mt-8">
            <div className="text-3xl mb-2">SQL</div>
            <p className="text-xs text-gray-300">输入知识点或粘贴 SQL</p>
            <p className="text-xs text-gray-200">AI 将流式生成分步演示</p>
          </div>
        )}

        {messages.length > 0 && filteredMessages.length === 0 && searchQuery && (
          <div className="text-center text-gray-300 text-xs mt-8">
            无匹配消息
          </div>
        )}

        {/* Date group */}
        {groupedMessages.map(group => (
          <div key={group.date}>
            {/* Date separator */}
            <div className="flex items-center gap-3 mb-3 mt-2">
              <div className="flex-1 h-px bg-gray-100" />
              <span className="text-[10px] text-gray-300 font-medium whitespace-nowrap">
                {group.label}
              </span>
              <div className="flex-1 h-px bg-gray-100" />
            </div>

            {/* Messages in this date group */}
            <div className="space-y-3">
              {group.msgs.map(m => (
                <MessageBubble key={m.id} message={m} onDelete={handleDelete} />
              ))}
            </div>
          </div>
        ))}

        {/* Agent thinking */}
        {generationStatus === 'streaming' && thinking && (
          <AgentThinkingChain content={thinking} />
        )}

        {/* Streaming indicator */}
        {generationStatus === 'streaming' && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-xl rounded-bl-md px-3 py-2 text-gray-400 text-xs">
              <span className="animate-pulse">已发送，AI 正在生成演示...</span>
            </div>
          </div>
        )}

        {errorMessage && (
          <div className="flex justify-start">
            <div className="bg-red-50 text-red-600 rounded-xl rounded-bl-md px-3 py-2 text-xs">
              {errorMessage}
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Demo snapshot indicator */}
      {currentDemo && generationStatus === 'idle' && (
        <DemoSnapshotIndicator
          version={currentDemo.metadata?.teacherVersion || 1}
          stepCount={currentDemo.steps?.length || 0}
        />
      )}

      {/* Quick actions */}
      <QuickActions onAction={handleQuickAction} />

      {/* Input */}
      <div className="border-t border-gray-100 p-3">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send()}
            placeholder="输入知识点或 SQL..."
            className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-100"
          />
          <button
            onClick={send}
            disabled={generationStatus === 'streaming' || !input.trim() || !activeConvId}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
          >
            发送
          </button>
        </div>
        <div className="flex gap-2 mt-2">
          {['SELECT', 'JOIN', 'ER 建模', '范式', '事务', '索引'].map(tag => (
            <button
              key={tag}
              onClick={() => setInput(prev => prev ? `${prev}, ${tag}` : tag)}
              className="text-[11px] text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded px-2 py-0.5 transition-colors"
            >
              {tag}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

function formatDateLabel(dateKey: string): string {
  try {
    const d = new Date(dateKey)
    if (isNaN(d.getTime())) return dateKey
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    if (d.toDateString() === today.toDateString()) return '今天'
    if (d.toDateString() === yesterday.toDateString()) return '昨天'

    const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
    const month = d.getMonth() + 1
    const day = d.getDate()
    const wd = weekdays[d.getDay()]
    return `${month}月${day}日 ${wd}`
  } catch {
    return dateKey
  }
}
