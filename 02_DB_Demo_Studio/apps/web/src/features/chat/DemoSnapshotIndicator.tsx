// features/chat/DemoSnapshotIndicator.tsx

interface Props {
  version: number
  stepCount: number
}

export function DemoSnapshotIndicator({ version, stepCount }: Props) {
  return (
    <div className="text-[10px] text-gray-400 px-3 py-1 border-t border-gray-100 flex items-center gap-3">
      <span>版本: v{version}</span>
      <span>{stepCount} 步</span>
      <span className="text-green-500">● 已就绪</span>
    </div>
  )
}
