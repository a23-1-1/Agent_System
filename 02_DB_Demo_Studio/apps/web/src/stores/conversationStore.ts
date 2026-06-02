// stores/conversationStore.ts
// 对话列表 + 当前对话 + 消息管理

import { create } from 'zustand'
import type { ConversationSummary, Conversation, Message, WsServerEvent } from '../lib/types'

interface ConversationState {
  // 列表
  conversations: ConversationSummary[]
  activeConvId: string | null
  loading: boolean

  // 当前对话
  currentConv: Conversation | null
  messages: Message[]
  generationStatus: 'idle' | 'streaming' | 'interrupted'

  // Actions
  loadConversations: () => Promise<void>
  setConversations: (list: ConversationSummary[]) => void
  createConversation: (title?: string) => Promise<string>
  switchConversation: (convId: string) => Promise<void>
  deleteConversation: (convId: string) => void
  renameConversation: (convId: string, title: string) => void
  deleteMessage: (convId: string, msgId: string) => void
  clearMessages: (convId: string) => void
  updateConversationSummary: (convId: string, summary: string) => void

  // 消息
  appendMessage: (msg: Message) => void
  appendStreamChunk: (convId: string, text: string) => void
  setGenerationStatus: (s: 'idle' | 'streaming' | 'interrupted') => void
  handleServerEvent: (event: WsServerEvent) => void
} // end ConversationState

export const useConversationStore = create<ConversationState>((set, get) => ({
  conversations: [],
  activeConvId: null,
  loading: false,
  currentConv: null,
  messages: [],
  generationStatus: 'idle',

  loadConversations: async () => {
    set({ loading: true })
    try {
      const resp = await fetch('/api/conversations')
      if (resp.ok) {
        const data = await resp.json()
        set({ conversations: data.conversations || [] })
      }
    } catch (err) {
      console.error('Failed to load conversations:', err)
    } finally {
      set({ loading: false })
    }
  },

  setConversations: (list) => set({ conversations: list }),

  createConversation: async (title) => {
    try {
      const resp = await fetch('/api/conversations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title || '新对话' }),
      })
      if (resp.ok) {
        const data = await resp.json()
        const conv = data as ConversationSummary
        set(s => ({ conversations: [conv, ...s.conversations] }))
        return conv.id
      }
    } catch (err) {
      console.error('Failed to create conversation:', err)
    }
    return ''
  },

  switchConversation: async (convId) => {
    const { activeConvId } = get()
    if (convId === activeConvId) return
    set({ activeConvId: convId, loading: true })

    // If we have it locally, show immediately
    if (get().currentConv?.id === convId) {
      set({ loading: false })
      return
    }

    try {
      const resp = await fetch(`/api/conversations/${convId}/messages`)
      if (resp.ok) {
        const data = await resp.json()
        set({
          messages: data.messages || [],
          currentConv: data.conversation || null,
          generationStatus: 'idle',
          loading: false,
        })
      }
    } catch (err) {
      console.error('Failed to load messages:', err)
      set({ loading: false })
    }
  },

  deleteConversation: (convId) => {
    fetch(`/api/conversations/${convId}`, { method: 'DELETE' }).catch(() => {})
    set(s => ({
      conversations: s.conversations.filter(c => c.id !== convId),
      activeConvId: s.activeConvId === convId ? null : s.activeConvId,
      messages: s.activeConvId === convId ? [] : s.messages,
    }))
  },

  renameConversation: (convId, title) => {
    fetch(`/api/conversations/${convId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    }).catch(() => {})
    set(s => ({
      conversations: s.conversations.map(c =>
        c.id === convId ? { ...c, title } : c
      ),
    }))
  },

  appendMessage: (msg) => {
    set(s => ({ messages: [...s.messages, msg] }))
  },

  appendStreamChunk: (_convId, text) => {
    set(s => {
      const msgs = [...s.messages]
      const last = msgs[msgs.length - 1]
      if (last && last.role === 'assistant') {
        msgs[msgs.length - 1] = {
          ...last,
          content: { ...last.content, text: (last.content.text || '') + text },
        }
      }
      return { messages: msgs }
    })
  },

  setGenerationStatus: (s) => set({ generationStatus: s }),

  deleteMessage: (convId, msgId) => {
    // Soft delete: mark as deleted instead of removing
    set(s => ({
      messages: s.messages.map(m =>
        m.id === msgId ? { ...m, deleted: true } : m
      ),
    }))
    set(s => ({
      conversations: s.conversations.map(c =>
        c.id === convId ? { ...c, messageCount: Math.max(0, c.messageCount - 1) } : c
      ),
    }))
  },

  clearMessages: (convId) => {
    set({ messages: [] })
    set(s => ({
      conversations: s.conversations.map(c =>
        c.id === convId ? { ...c, messageCount: 0, summary: '' } : c
      ),
    }))
  },

  updateConversationSummary: (convId, summary) => {
    set(s => ({
      conversations: s.conversations.map(c =>
        c.id === convId ? { ...c, summary } : c
      ),
    }))
  },

  handleServerEvent: (event) => {
    const store = get()
    switch (event.type) {
      case 'conv:list':
        set({ conversations: event.conversations })
        break
      case 'conv:loaded':
        set({
          messages: event.messages,
          activeConvId: event.convId,
          loading: false,
        })
        break
      case 'conv:created':
        set(s => ({
          conversations: [event.conversation, ...s.conversations],
        }))
        break
      case 'conv:deleted':
        set(s => ({
          conversations: s.conversations.filter(c => c.id !== event.convId),
        }))
        break
      case 'assistant-text':
        if (event.convId === store.activeConvId) {
          store.appendStreamChunk(event.convId, event.content)
        }
        break
      case 'agent:thinking':
        if (event.convId === store.activeConvId) {
          store.appendStreamChunk(event.convId, `\n[思考] ${event.content}`)
        }
        break
      case 'conv:new_message':
        if (event.convId === store.activeConvId) {
          set(s => ({ messages: [...s.messages, event.message] }))
          if (event.message.role === 'assistant') {
            store.setGenerationStatus('idle')
          }
        }
        break
      case 'demo:complete':
        if (event.convId === store.activeConvId) {
          store.setGenerationStatus('idle')
          store.updateConversationSummary(event.convId, event.demo?.title?.zh || '已生成回复')
        }
        break
      case 'error':
        store.setGenerationStatus('idle')
        break
      default:
        break
    }
  },
}))
