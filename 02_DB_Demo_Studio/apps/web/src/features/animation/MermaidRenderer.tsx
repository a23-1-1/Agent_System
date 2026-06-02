// features/animation/MermaidRenderer.tsx
// Mermaid 可视化渲染 + 步骤高亮联动

import { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'

// Initialize mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    primaryColor: '#eff6ff',
    primaryBorderColor: '#3b82f6',
    lineColor: '#93c5fd',
    secondaryColor: '#f0fdf4',
    tertiaryColor: '#fefce8',
    fontSize: '14px',
  },
  securityLevel: 'loose',
})

const DEMO_MERMAID = `flowchart TD
    A["SELECT s.name, c.course_name"] --> B["FROM students s"]
    B --> C{"INNER JOIN"}
    C --> D["courses c ON s.id = c.student_id"]
    D --> E["WHERE (自动过滤)"]
    E --> F["ORDER BY (自动排序)"]
    F --> G["结果集: 姓名 + 课程名"]

    style A fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
    style B fill:#eff6ff,stroke:#3b82f6
    style C fill:#fef2f2,stroke:#ef4444,stroke-width:3px
    style D fill:#eff6ff,stroke:#3b82f6
    style E fill:#f8fafc,stroke:#94a3b8,stroke-dasharray:5
    style F fill:#f8fafc,stroke:#94a3b8,stroke-dasharray:5
    style G fill:#f0fdf4,stroke:#22c55e`

const MERMAID_BY_PHASE: Record<string, string> = {
  lex: `flowchart LR
    subgraph Token["词法分析 Tokens"]
        T1["SELECT"] --> T2["s.name, c.course_name"]
        T2 --> T3["FROM"]
        T3 --> T4["students s"]
        T4 --> T5["INNER JOIN"]
        T5 --> T6["courses c"]
        T6 --> T7["ON s.id = c.student_id"]
    end
    style T1 fill:#dbeafe,stroke:#2563eb
    style T3 fill:#dbeafe,stroke:#2563eb
    style T5 fill:#dbeafe,stroke:#2563eb
    style T7 fill:#dbeafe,stroke:#2563eb`,

  parse: `flowchart TD
    subgraph Tables["涉及表"]
        S["students<br/>(id, name, major)"]
        C["courses<br/>(id, student_id, course_name, score)"]
    end
    S -->|"JOIN ON s.id = c.student_id"| C

    subgraph Clauses["检测到的子句"]
        J["✓ JOIN (INNER JOIN)"]
        W["— WHERE (无)"]
        G["— GROUP BY (无)"]
        O["— ORDER BY (无)"]
    end`,

  optimize: `flowchart LR
    subgraph MySQL["MySQL 策略"]
        M1["扫描 students 表 (3行)"]
        M2["通过索引 idx_courses_student_id"]
        M3["查找 courses 匹配行"]
        M1 --> M2 --> M3
    end
    M3 --> Result["Nested Loop Join<br/>cost ≈ 2.20"]`,

  plan: `flowchart TD
    subgraph MySQLPlan["MySQL 执行计划"]
        Q["Query Block<br/>cost: 2.20"]
        Q --> T["Table Scan: students (3 rows)"]
        Q --> N["Nested Loop"]
        N --> I["Index Lookup: courses<br/>idx_courses_student_id"]
    end

    subgraph PGPlan["PostgreSQL 执行计划"]
        P["Hash Join<br/>cost: 1.85"]
        P --> S["Seq Scan: students"]
        P --> H["Hash"]
        H --> C["Seq Scan: courses"]
    end

    MySQLPlan ---|"代价对比"| PGPlan`,

  execute: `flowchart LR
    subgraph DataFlow["数据流"]
        D1["students 表<br/>3 行"]
        D2["过滤后有 JOIN 条件<br/>→ 2 行匹配"]
        D3["courses 表<br/>4 行"]
        D4["最终结果<br/>2 行"]
    end
    D1 --> D2
    D3 --> D2 --> D4
    style D4 fill:#f0fdf4,stroke:#22c55e,stroke-width:3px`,

  result: `flowchart LR
    subgraph Result["查询结果"]
        R1["张三 | 数据库原理"]
        R2["张三 | 操作系统"]
        R3["李四 | 数据库原理"]
    end
    style R1 fill:#f0fdf4,stroke:#22c55e
    style R2 fill:#f0fdf4,stroke:#22c55e
    style R3 fill:#f0fdf4,stroke:#22c55e`,
}

interface Props {
  phase?: string
  mermaidCode?: string
  highlightIndex?: number
}

export function MermaidRenderer({ phase, mermaidCode, highlightIndex }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [svg, setSvg] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [showRaw, setShowRaw] = useState(false)

  // Determine which mermaid code to use
  const code = mermaidCode || (phase ? MERMAID_BY_PHASE[phase] : null) || DEMO_MERMAID

  useEffect(() => {
    if (!code) return
    let cancelled = false

    mermaid.render('mermaid-svg', code)
      .then(({ svg }) => {
        if (!cancelled) setSvg(svg)
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message || 'Mermaid 渲染失败')
          console.warn('[Mermaid] render error:', err)
        }
      })

    return () => { cancelled = true }
  }, [code])

  if (error) {
    return (
      <div className="border border-red-200 bg-red-50 rounded-xl p-3">
        <div className="text-xs text-red-500 mb-2">Mermaid 渲染失败</div>
        <pre className="text-[10px] text-red-400 font-mono whitespace-pre-wrap">{error}</pre>
        <button
          onClick={() => setShowRaw(!showRaw)}
          className="text-[10px] text-red-400 hover:text-red-600 mt-1"
        >
          {showRaw ? '隐藏源代码' : '显示源代码'}
        </button>
        {showRaw && (
          <pre className="text-[10px] text-gray-500 font-mono mt-2 whitespace-pre-wrap bg-white rounded-lg p-2">
            {code}
          </pre>
        )}
      </div>
    )
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-3 py-2 bg-gray-50 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider">
            {phase ? `${phase} 阶段` : 'Mermaid 可视化'}
          </span>
          {highlightIndex !== undefined && (
            <span className="text-[10px] text-blue-600 bg-blue-50 rounded px-1.5 py-0.5">
              步骤 {highlightIndex + 1}
            </span>
          )}
        </div>
        <button
          onClick={() => setShowRaw(!showRaw)}
          className="text-[10px] text-gray-400 hover:text-blue-600 transition-colors"
        >
          {showRaw ? '视图' : '源码'}
        </button>
      </div>

      {/* Mermaid SVG */}
      {showRaw ? (
        <pre className="text-[10px] text-gray-600 font-mono p-4 whitespace-pre-wrap overflow-x-auto bg-gray-50 max-h-80">
          {code}
        </pre>
      ) : (
        <div
          ref={containerRef}
          className="p-4 flex justify-center overflow-x-auto"
          dangerouslySetInnerHTML={{ __html: svg }}
        />
      )}
    </div>
  )
}
