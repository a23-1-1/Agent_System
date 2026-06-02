// stores/playbackStore.ts
// 播放状态 + 自适应决策

import { create } from 'zustand'
import type { QuizResult, AdaptiveDecision } from '../lib/types'

interface PlaybackState {
  currentStepIndex: number
  isPlaying: boolean
  isAdaptiveMode: boolean
  speedMultiplier: number

  // 学生数据
  quizResults: QuizResult[]
  masteryLevel: number   // 0-100
  timeOnStep: number     // 当前步停留秒数

  // Actions
  nextStep: (totalSteps: number) => void
  prevStep: () => void
  seekTo: (index: number) => void
  togglePlay: () => void
  setSpeed: (speed: number) => void
  reset: () => void
  setAdaptiveMode: (on: boolean) => void

  // 自适应
  recordQuizAnswer: (questionId: string, answer: number, correctAnswer: number) => void
  recordTimeOnStep: () => void
  getAdaptiveDecision: () => AdaptiveDecision | null
}

export const usePlaybackStore = create<PlaybackState>((set, get) => ({
  currentStepIndex: 0,
  isPlaying: false,
  isAdaptiveMode: false,
  speedMultiplier: 1.0,
  quizResults: [],
  masteryLevel: 0,
  timeOnStep: 0,

  nextStep: (totalSteps) => {
    set(s => {
      if (s.currentStepIndex >= totalSteps - 1) return { isPlaying: false }
      return { currentStepIndex: s.currentStepIndex + 1, timeOnStep: 0 }
    })
  },

  prevStep: () => {
    set(s => ({
      currentStepIndex: Math.max(0, s.currentStepIndex - 1),
      timeOnStep: 0,
    }))
  },

  seekTo: (index) => set({ currentStepIndex: index, timeOnStep: 0 }),
  togglePlay: () => set(s => ({ isPlaying: !s.isPlaying })),
  setSpeed: (speed) => set({ speedMultiplier: speed }),
  reset: () => set({
    currentStepIndex: 0, isPlaying: false, quizResults: [],
    masteryLevel: 0, timeOnStep: 0,
  }),
  setAdaptiveMode: (on) => set({ isAdaptiveMode: on }),

  recordQuizAnswer: (questionId, answer, correctAnswer) => {
    const result: QuizResult = {
      questionId,
      selectedAnswer: answer,
      correctAnswer,
      isCorrect: answer === correctAnswer,
      timestamp: new Date().toISOString(),
    }
    set(s => {
      const results = [...s.quizResults, result]
      const correctCount = results.filter(r => r.isCorrect).length
      return {
        quizResults: results,
        masteryLevel: Math.round((correctCount / results.length) * 100),
      }
    })
  },

  recordTimeOnStep: () => {
    set(s => ({ timeOnStep: s.timeOnStep + 1 }))
  },

  getAdaptiveDecision: () => {
    const { masteryLevel, quizResults, timeOnStep, currentStepIndex } = get()
    if (quizResults.length < 2) return null

    // Simple adaptive logic: if mastery > 80%, suggest skip
    if (masteryLevel > 80 && timeOnStep < 3) {
      return {
        action: 'skip',
        rationale: '你已掌握这个知识点，建议跳过。',
        targetStepIndex: currentStepIndex + 1,
      }
    }
    // If mastery < 40%, suggest expand
    if (masteryLevel < 40 && quizResults.length >= 2) {
      return {
        action: 'expand',
        rationale: '这个知识点还有些薄弱，展开详细讲解一下？',
        targetStepIndex: currentStepIndex,
      }
    }
    return null
  },
}))
