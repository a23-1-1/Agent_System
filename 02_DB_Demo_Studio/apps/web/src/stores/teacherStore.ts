// stores/teacherStore.ts
// 教师风格 Profile

import { create } from 'zustand'
import type { TeacherProfile } from '../lib/types'

interface TeacherState {
  profile: TeacherProfile | null
  isLoaded: boolean

  loadProfile: () => Promise<void>
  updateProfile: (updates: Partial<TeacherProfile>) => Promise<void>
}

const DEFAULT_PROFILE: TeacherProfile = {
  id: 'local',
  preferredModel: 'deepseek',
  defaultDemoType: 'standard',
  narrationStyle: 'detailed',
  difficulty: 'intermediate',
  preferences: {
    autoGenerateQuiz: false,
    defaultTTS: false,
    exportFormat: 'web',
  },
}

export const useTeacherStore = create<TeacherState>((set) => ({
  profile: null,
  isLoaded: false,

  loadProfile: async () => {
    try {
      const resp = await fetch('/api/teacher/profile')
      if (resp.ok) {
        const data = await resp.json()
        set({ profile: data, isLoaded: true })
        return
      }
    } catch { /* fallback */ }
    set({ profile: DEFAULT_PROFILE, isLoaded: true })
  },

  updateProfile: async (updates) => {
    set(s => ({
      profile: s.profile ? { ...s.profile, ...updates } : { ...DEFAULT_PROFILE, ...updates },
    }))
    try {
      await fetch('/api/teacher/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(get().profile),
      })
    } catch { /* ignore */ }
  },
}))

function get() {
  return useTeacherStore.getState()
}
