// SQL 过程模拟器 — 展示每一步的中间结果表

export interface SqlSimulatorStep {
  clause: string
  description: string
  intermediateRows: number
  columns?: string[]
  rows?: Record<string, string | number>[]
}

interface Props {
  steps: SqlSimulatorStep[]
  activeIndex: number
}

export function SqlSimulator({ steps, activeIndex }: Props) {
  if (!steps.length) {
    return (
      <div className="rounded-xl border border-dashed border-gray-200 bg-gray-50 px-3 py-4 text-center text-xs text-gray-400">
        暂无 SQL 过程模拟数据。发送含 JOIN 的 SELECT 语句可生成中间结果表。
      </div>
    )
  }

  const idx = Math.min(Math.max(0, activeIndex), steps.length - 1)
  const current = steps[idx]

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between gap-2">
        <span className="text-[10px] font-semibold uppercase tracking-wide text-blue-600">
          SQL 过程模拟
        </span>
        <span className="text-[10px] text-gray-400">
          步骤 {idx + 1} / {steps.length}
        </span>
      </div>

      <div className="flex flex-wrap gap-1">
        {steps.map((s, i) => (
          <span
            key={`${s.clause}-${i}`}
            className={`rounded px-2 py-0.5 text-[10px] font-mono ${
              i === idx
                ? 'bg-blue-100 text-blue-800'
                : i < idx
                  ? 'bg-green-50 text-green-700'
                  : 'bg-gray-100 text-gray-400'
            }`}
          >
            {i + 1}. {s.clause.split(/\s+/)[0] ?? s.clause}
          </span>
        ))}
      </div>

      <div className="rounded-xl border border-blue-100 bg-blue-50/50 px-3 py-2">
        <div className="mb-1 font-mono text-xs font-medium text-blue-800">{current.clause}</div>
        <p className="text-xs leading-relaxed text-gray-600">{current.description}</p>
        <p className="mt-1 text-[10px] text-gray-500">
          中间结果行数：<strong>{current.intermediateRows}</strong>
        </p>
      </div>

      <ResultTable step={current} />
    </div>
  )
}

function ResultTable({ step }: { step: SqlSimulatorStep }) {
  const cols = step.columns?.length ? step.columns : []
  const rows = step.rows?.length ? step.rows : []

  if (!cols.length) {
    return (
      <div className="text-xs text-gray-400">本步无表格数据（仅统计行数）。</div>
    )
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
      <table className="min-w-full text-left text-xs">
        <thead>
          <tr className="border-b border-gray-200 bg-gray-50">
            {cols.map(c => (
              <th key={c} className="px-2 py-1.5 font-medium text-gray-600">
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.slice(0, 8).map((row, ri) => (
            <tr key={ri} className="border-b border-gray-100 last:border-0">
              {cols.map(c => (
                <td key={c} className="px-2 py-1 font-mono text-gray-700">
                  {String(row[c] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {rows.length > 8 && (
        <p className="px-2 py-1 text-[10px] text-gray-400">仅展示前 8 行，共 {rows.length} 行</p>
      )}
    </div>
  )
}
