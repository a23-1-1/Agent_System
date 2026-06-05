// stores/demoStore.ts
// 当前演示 + 版本快照

import { create } from 'zustand'
import type { DemoPackage, DemoStep, WsServerEvent } from '../lib/types'

interface DemoState {
  currentDemo: DemoPackage | null
  snapshots: DemoPackage[]
  activeSnapshotIndex: number
  generationStatus: 'idle' | 'generating' | 'interrupted'

  setDemo: (demo: DemoPackage) => void
  updateStep: (stepId: string, updates: Partial<DemoStep>) => void
  reorderSteps: (fromIndex: number, toIndex: number) => void
  regenerateStep: (stepId: string, hint?: string) => Promise<void>
  saveSnapshot: () => void
  restoreSnapshot: (index: number) => void
  handleServerEvent: (event: WsServerEvent) => void
}

export const useDemoStore = create<DemoState>((set, get) => ({
  currentDemo: null,
  snapshots: [],
  activeSnapshotIndex: -1,
  generationStatus: 'idle',

  setDemo: (demo) => set({ currentDemo: demo }),

  updateStep: (stepId, updates) => {
    set(s => {
      if (!s.currentDemo) return s
      return {
        currentDemo: {
          ...s.currentDemo,
          steps: s.currentDemo.steps.map(st =>
            st.id === stepId ? { ...st, ...updates } : st
          ),
        },
      }
    })
  },

  reorderSteps: (fromIndex, toIndex) => {
    set(s => {
      if (!s.currentDemo) return s
      const steps = [...s.currentDemo.steps]
      const [moved] = steps.splice(fromIndex, 1)
      steps.splice(toIndex, 0, moved)
      return {
        currentDemo: {
          ...s.currentDemo,
          steps: steps.map((st, i) => ({ ...st, order: i + 1 })),
        },
      }
    })
  },

  regenerateStep: async (stepId, hint) => {
    const { currentDemo } = get()
    if (!currentDemo) return
    try {
      await fetch('/api/ai/regenerate-step', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ demo_id: currentDemo.id, step_id: stepId, hint }),
      })
    } catch (err) {
      console.error('Failed to regenerate step:', err)
    }
  },

  saveSnapshot: () => {
    const { currentDemo } = get()
    if (!currentDemo) return
    set(s => ({
      snapshots: [...s.snapshots, { ...currentDemo }],
      activeSnapshotIndex: s.snapshots.length,
    }))
  },

  restoreSnapshot: (index) => {
    const { snapshots } = get()
    if (index >= 0 && index < snapshots.length) {
      set({ currentDemo: { ...snapshots[index] }, activeSnapshotIndex: index })
    }
  },

  handleServerEvent: (event) => {
    switch (event.type) {
      case 'demo:updated':
        set({ currentDemo: event.demo, generationStatus: 'idle' })
        break
      case 'demo:complete':
        if (event.demo) {
          set({ currentDemo: event.demo, generationStatus: 'idle' })
        } else {
          set({ generationStatus: 'idle' })
        }
        break
      case 'demo:step_preview':
        // Step preview: we add or update the step in current demo
        set(s => {
          if (!s.currentDemo) return s
          const existing = s.currentDemo.steps.findIndex(st => st.order === event.order)
          const steps = [...s.currentDemo.steps]
          if (existing >= 0) {
            steps[existing] = event.step
          } else {
            steps.push(event.step)
          }
          return { currentDemo: { ...s.currentDemo, steps } }
        })
        break
      case 'demo:step_regenerated':
        set(s => {
          if (!s.currentDemo) return s
          return {
            currentDemo: {
              ...s.currentDemo,
              steps: s.currentDemo.steps.map(st =>
                st.id === event.step.id ? event.step : st
              ),
            },
          }
        })
        break
      default:
        break
    }
  },
}))
