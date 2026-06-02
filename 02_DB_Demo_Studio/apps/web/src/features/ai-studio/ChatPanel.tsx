import { useState, useRef, useEffect } from 'react'
import type { DemoPackage } from '../../pages/TeachPage'

interface Props {
  onDemoUpdate: (demo: DemoPackage) => void
}

export function ChatPanel({ onDemoUpdate }: Props) {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [streaming, setStreaming] = useState(false)
  const chatEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async () => {
    if (!input.trim() || streaming) return
    const userMsg: Message = { role: 'user', content: input, ts: Date.now() }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setStreaming(true)

    try {
      const payload = {
        sql: detectSql(input) || undefined,
        message: input,
        curriculum_node: detectCurriculum(input),
      }

      const resp = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)

      // 读取 SSE 流
      const reader = resp.body?.getReader()
      if (!reader) throw new Error('No reader')

      let fullText = ''
      const decoder = new TextDecoder()
      let done = false

      while (!done) {
        const { value, done: d } = await reader.read()
        done = d
        if (value) {
          const chunk = decoder.decode(value)
          const lines = chunk.split('\n').filter(l => l.startsWith('data:'))
          for (const line of lines) {
            try {
              const evt = JSON.parse(line.slice(5).trim())
              if (evt.type === 'text-delta') {
                fullText += evt.content
              } else if (evt.type === 'demo-updated' && evt.demo) {
                onDemoUpdate(evt.demo)
              }
            } catch { /* ignore parse errors */ }
          }
        }
      }

      const aiMsg: Message = { role: 'assistant', content: fullText || '已生成演示初稿，请在编辑器中查看', ts: Date.now() }
      setMessages(prev => [...prev, aiMsg])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant', content: `[错误: ${err instanceof Error ? err.message : '未知'}]`, ts: Date.now()
      }])
    } finally {
      setStreaming(false)
    }
  }

  return (
    <>
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3 text-sm">
        {messages.length === 0 && (
          <div className="text-center text-gray-300 mt-8">
            <div className="text-3xl mb-2">💬</div>
            输入知识点或粘贴 SQL<br/>AI 将流式生成分步演示
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : ''}`}>
            <div className={`max-w-[85%] rounded-xl px-3 py-2 ${
              m.role === 'user'
                ? 'bg-blue-600 text-white rounded-br-md'
                : 'bg-gray-100 text-gray-700 rounded-bl-md'
            }`}>
              {m.content}
            </div>
          </div>
        ))}
        {streaming && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-xl rounded-bl-md px-3 py-2 text-gray-400 text-xs">
              <span className="animate-pulse">AI 正在生成...</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* 输入区 */}
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
            disabled={streaming || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
          >
            发送
          </button>
        </div>
        <div className="flex gap-2 mt-2">
          {['SELECT ...', 'JOIN', 'ER 建模', '范式', '事务', '索引'].map(tag => (
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
    </>
  )
}

type Message = { role: 'user' | 'assistant'; content: string; ts: number }

function detectSql(text: string): string | null {
  const m = text.match(/\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\b/i)
  return m ? text : null
}

function detectCurriculum(text: string): string | null {
  const keywords = ['JOIN', 'ER', '范式', '事务', '索引', 'B+树', '恢复', 'ACID', '锁']
  return keywords.find(k => text.includes(k)) || null
}
