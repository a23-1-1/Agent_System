// features/chat/AgentThinkingChain.tsx

interface Props {
  content: string
}

export function AgentThinkingChain({ content }: Props) {
  if (!content) return null
  return (
    <div className="bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 text-xs text-amber-700 font-mono leading-relaxed">
      <div className="text-[10px] text-amber-400 font-semibold mb-1">🤖 Agent 思考链</div>
      {content}
    </div>
  )
}
