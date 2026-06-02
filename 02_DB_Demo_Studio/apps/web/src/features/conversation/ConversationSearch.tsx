// features/conversation/ConversationSearch.tsx
interface Props {
  value: string
  onChange: (v: string) => void
}

export function ConversationSearch({ value, onChange }: Props) {
  return (
    <div className="px-3 py-2">
      <input
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder="搜索对话..."
        className="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-blue-400"
      />
    </div>
  )
}
