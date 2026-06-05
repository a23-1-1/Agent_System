// features/quiz/QuizPanel.tsx
// 嵌入式测验：AI 根据当前步骤出题，答题后显示结果 + 讲解

import { useState } from 'react'
import type { QuizQuestion } from '../../lib/types'
import { usePlaybackStore } from '../../stores/playbackStore'

interface Props {
  stepIndex: number
  question: QuizQuestion
}

const SAMPLE_QUESTIONS: Record<string, QuizQuestion[]> = {
  lex: [
    { id: 'lex_1', question: '数据库语句解析的第一阶段是什么？', options: ['词法分析', '语法分析', '查询优化', '执行计划'], answer: 0, explanation: '词法分析（Lex）将语句分解为关键字、表名等基本单元（tokens），是解析的第一步。' },
    { id: 'lex_2', question: '以下哪个不是 SQL 关键字？', options: ['SELECT', 'FROM', 'TABLE', 'students'], answer: 3, explanation: 'students 是表名，不是 SQL 关键字。SELECT、FROM 都是 SQL 关键字。' },
  ],
  parse: [
    { id: 'parse_1', question: '语法分析阶段的主要任务是什么？', options: ['生成执行计划', '检查表是否存在', '拆分为 tokens', '执行查询'], answer: 1, explanation: '语法分析（Parse）验证语句的语法正确性，并检查引用的表和列是否存在。' },
  ],
  optimize: [
    { id: 'opt_1', question: '以下哪种扫描方式在大表无索引时效率最高？', options: ['全表扫描', '索引查找', '哈希连接', '嵌套循环连接'], answer: 1, explanation: '索引查找避免全表扫描，通过 B+树快速定位到少量数据行。全表扫描适合小表。' },
  ],
  plan: [
    { id: 'plan_1', question: '数据库演示中使用 JOIN 时常用哪种算法？', options: ['Hash Join', 'Nested Loop Join', 'Merge Join', '全表扫描'], answer: 1, explanation: '在常见教学场景中，JOIN 演示常用 Nested Loop Join（嵌套循环连接）来解释逐行匹配的过程。' },
  ],
  result: [
    { id: 'result_1', question: 'INNER JOIN 的结果中，不匹配的行会被怎样处理？', options: ['保留为 NULL', '丢弃', '排在最后', '报错'], answer: 1, explanation: 'INNER JOIN 只保留两表中匹配的行，不匹配的行会被丢弃。' },
  ],
}

export function QuizPanel({ stepIndex, question }: Props) {
  const recordQuizAnswer = usePlaybackStore(s => s.recordQuizAnswer)
  const quizResults = usePlaybackStore(s => s.quizResults)
  const [selected, setSelected] = useState<number | null>(null)
  const [submitted, setSubmitted] = useState(false)

  // Check if already answered
  const existing = quizResults.find(r => r.questionId === question.id)
  const prevAnswer = existing !== undefined

  // Find sample questions for this phase if no specific question
  const effectiveQuestion = question.id ? question : getSampleQuestion(stepIndex)

  if (!effectiveQuestion) return null

  const handleSubmit = () => {
    if (selected === null) return
    recordQuizAnswer(effectiveQuestion.id!, selected, effectiveQuestion.answer)
    setSubmitted(true)
  }

  if (submitted || prevAnswer) {
    const result = quizResults.find(r => r.questionId === effectiveQuestion.id)
    return (
      <div className={`rounded-xl border p-3 ${result?.isCorrect ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
        <div className="flex items-center gap-2 mb-2">
          <span className="text-sm">{result?.isCorrect ? '✅' : '❌'}</span>
          <span className="text-xs font-medium text-gray-700">
            {result?.isCorrect ? '回答正确！' : '回答错误'}
          </span>
        </div>
        <p className="text-xs text-gray-600 leading-relaxed">
          {effectiveQuestion.explanation}
        </p>
      </div>
    )
  }

  return (
    <div className="border border-gray-200 rounded-xl p-3 bg-white">
      <div className="text-xs font-medium text-gray-500 mb-2">📝 课程知识测验</div>
      <p className="text-sm text-gray-700 mb-3">{effectiveQuestion.question}</p>
      <div className="space-y-2">
        {effectiveQuestion.options.map((opt, i) => (
          <button
            key={i}
            onClick={() => setSelected(i)}
            className={`w-full text-left px-3 py-2 rounded-lg border text-sm transition-colors
              ${selected === i
                ? 'border-blue-400 bg-blue-50 text-blue-700'
                : 'border-gray-200 text-gray-600 hover:border-blue-300 hover:bg-blue-50/50'
              }`}
          >
            {String.fromCharCode(65 + i)}. {opt}
          </button>
        ))}
      </div>
      <button
        onClick={handleSubmit}
        disabled={selected === null}
        className="mt-3 w-full text-center text-sm bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white rounded-lg py-2 transition-colors"
      >
        提交答案
      </button>
    </div>
  )
}

function getSampleQuestion(stepIndex: number): QuizQuestion | null {
  const phases = ['lex', 'parse', 'optimize', 'plan', 'execute', 'result']
  const phase = phases[stepIndex] || 'result'
  const questions = SAMPLE_QUESTIONS[phase]
  if (!questions || questions.length === 0) return null
  return questions[stepIndex % questions.length]
}
