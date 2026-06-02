// features/chat/QuickActions.tsx

interface Action {
  label: string
  icon: string
  action: string
}

const ACTIONS: Action[] = [
  { label: '加可视化', icon: '📊', action: 'viz' },
  { label: '出题', icon: '📝', action: 'quiz' },
  { label: '换引擎', icon: '🔄', action: 'engine' },
  { label: 'TTS', icon: '🔊', action: 'tts' },
  { label: '导出', icon: '📤', action: 'export' },
  { label: '换模型', icon: '🤖', action: 'model' },
]

interface Props {
  onAction: (action: string) => void
}

export function QuickActions({ onAction }: Props) {
  return (
    <div className="flex flex-wrap gap-1.5 px-3 py-2 border-t border-gray-100">
      {ACTIONS.map(a => (
        <button
          key={a.action}
          onClick={() => onAction(a.action)}
          className="text-[11px] text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg px-2 py-1 transition-colors"
          title={a.label}
        >
          {a.icon} {a.label}
        </button>
      ))}
    </div>
  )
}
