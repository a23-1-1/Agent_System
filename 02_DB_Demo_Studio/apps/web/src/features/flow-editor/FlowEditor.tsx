// features/flow-editor/FlowEditor.tsx
// 从 demoStore 读取当前演示，展示步骤卡片

import { useDemoStore } from '../../stores/demoStore'

export function FlowEditor() {
  const currentDemo = useDemoStore(s => s.currentDemo)

  if (!currentDemo) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-300 text-sm">
        <div className="text-center">
          <div className="text-4xl mb-2 opacity-50">?</div>
          在左侧 AI Studio 输入要讲的知识点<br/>或直接粘贴案例、SQL
        </div>
      </div>
    )
  }

  const steps = currentDemo.steps || []

  return (
    <div className="flex-1 overflow-auto p-6">
      <div className="relative min-h-[400px]">
        <div className="flex items-start gap-4 flex-wrap">
          {steps.map((step, i) => (
            <div key={step.id} className="relative">
              <StepCard step={step} index={i} />
              {i < steps.length - 1 && (
                <div className="absolute top-1/2 -right-4 w-4 h-px bg-blue-300" />
              )}
            </div>
          ))}
        </div>

        <div className="mt-8 pt-4 border-t border-dashed border-gray-200 flex items-center gap-4 text-xs text-gray-400">
          <span>共 {steps.length} 步</span>
          <span>版本: v{currentDemo.metadata?.teacherVersion || 1}</span>
          <span>步进时长: {currentDemo.playback?.defaultStepDurationMs || 5000}ms</span>
        </div>
      </div>
    </div>
  )
}

function StepCard({ step, index }: { step: any; index: number }) {
  const labels: Record<string, string> = {
    lex: '词法分析', parse: '语法分析', optimize: '策略选择',
    plan: '执行计划', execute: '执行过程', result: '结果集',
    concept: '概念', transform: '变换', compare: '对比', summary: '总结',
  }

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 w-36 hover:border-blue-300 hover:shadow-sm transition-all cursor-pointer group">
      <div className="flex items-center gap-2 mb-1.5">
        <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-700 text-xs flex items-center justify-center font-mono">
          {index + 1}
        </span>
        <span className="text-[10px] uppercase font-mono text-gray-400">{step.workflowPhase}</span>
      </div>
      <div className="text-xs font-medium text-gray-700 mb-1">
        {labels[step.workflowPhase] || step.workflowPhase}
      </div>
      <div className="text-[11px] text-gray-400 line-clamp-2">
        {step.narration?.zh?.slice(0, 30) || '未生成讲解词'}
      </div>
      {step.groundingRef && (
        <div className="mt-1.5 text-[10px] text-green-600 bg-green-50 rounded px-1.5 py-0.5 inline-block">
          有证据
        </div>
      )}
    </div>
  )
}
