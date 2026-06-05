// pages/TeacherWorkbenchPage.tsx — 课程知识工作台
// 三栏布局：ConversationPanel | ChatPanel + FlowEditor | ExecutionPlayer

import { useEffect } from 'react'
import { useConversationStore } from '../stores/conversationStore'
import { useWebSocket } from '../hooks/useWebSocket'
import { ConversationPanel } from '../features/conversation/ConversationPanel'
import { ChatPanel } from '../features/chat/ChatPanel'
import { FlowEditor } from '../features/flow-editor/FlowEditor'
import { ExecutionPlayer } from '../features/execution-player/Player'

const TEACHER_ID = 'local'

export default function TeacherWorkbenchPage() {
  const activeConvId = useConversationStore(s => s.activeConvId)
  const conversations = useConversationStore(s => s.conversations)
  const loading = useConversationStore(s => s.loading)
  const loadConversations = useConversationStore(s => s.loadConversations)
  const switchConversation = useConversationStore(s => s.switchConversation)
  const createConversation = useConversationStore(s => s.createConversation)

  // WebSocket — only connect when we have a valid convId
  const { status, send: _send, client } = useWebSocket(TEACHER_ID, activeConvId || '')

  // Load initial conversations
  useEffect(() => {
    loadConversations()
  }, [])

  // Auto-select first conversation after list is loaded
  useEffect(() => {
    if (!activeConvId && conversations.length > 0) {
      switchConversation(conversations[0].id)
    }
  }, [activeConvId, conversations, switchConversation])

  // Bootstrap with one conversation if none exists
  useEffect(() => {
    if (!loading && !activeConvId && conversations.length === 0) {
      void (async () => {
        const convId = await createConversation()
        if (convId) {
          await switchConversation(convId)
        }
      })()
    }
  }, [loading, activeConvId, conversations.length, createConversation, switchConversation])

  const handleCreateConv = async () => {
    const convId = await createConversation()
    if (convId) {
      switchConversation(convId)
    }
  }

  return (
    <div className="h-[calc(100vh-56px)] flex overflow-hidden bg-gray-100">
      {/* Left: Conversation Panel */}
      <div className="w-60 flex-shrink-0 overflow-hidden border-r border-gray-200 bg-white">
        <ConversationPanel
          activeConvId={activeConvId}
          onSwitchConv={switchConversation}
          onCreateConv={handleCreateConv}
        />
      </div>

      {/* Center + Right */}
      <div className="flex-1 flex overflow-hidden gap-0">
        {/* Center: Chat + FlowEditor */}
        <div className="flex-1 flex flex-col min-w-0 bg-white mr-px">
          {/* Connection status */}
          <div className="flex items-center gap-2 px-4 py-1.5 bg-gray-50 border-b border-gray-200 text-[11px] flex-shrink-0">
            <span className={`w-1.5 h-1.5 rounded-full ${
              status === 'connected' ? 'bg-green-500' :
              status === 'connecting' ? 'bg-yellow-500' : 'bg-red-500'
            }`} />
            <span className="text-gray-500">
              {status === 'connected' ? '已连接' :
               status === 'connecting' ? '连接中...' : '未连接'}
            </span>
            {activeConvId && (
              <span className="text-gray-300 ml-1 text-[10px]">{activeConvId.slice(0, 12)}...</span>
            )}
            {!activeConvId && (
              <span className="text-gray-400 ml-2">请选择或创建一个课程对话</span>
            )}
          </div>

          <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
            {/* Chat Panel */}
            <div className="flex-1 flex flex-col min-h-0 overflow-hidden border-b border-gray-200">
              <ChatPanel wsClient={client} activeConvId={activeConvId} />
            </div>

            {/* Flow Editor */}
            <div className="h-48 flex-shrink-0 overflow-hidden">
              <div className="px-4 py-2 border-b border-gray-100 bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                演示编辑器
              </div>
              <div className="h-[calc(100%-36px)] overflow-y-auto">
                <FlowEditor />
              </div>
            </div>
          </div>
        </div>

        {/* Right: Player */}
        <div className="w-80 flex-shrink-0 bg-white overflow-hidden flex flex-col">
          <div className="px-4 py-2 border-b border-gray-200 bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-wider flex-shrink-0">
            实时预览
          </div>
          <div className="flex-1 overflow-y-auto p-3">
            <ExecutionPlayer />
          </div>
        </div>
      </div>
    </div>
  )
}
