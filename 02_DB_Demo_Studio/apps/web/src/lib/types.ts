// DB Demo Studio — 类型定义
// 后续会拆分为独立文件

export interface DemoPackage {
  id: string;
  title: { zh: string; en: string; };
  steps: DemoStep[];
  workflowTrace?: {
    workflowId: string;
    workflowType: 'sql-execution' | 'concept-progression';
    aiSessionId?: string;
    grounding?: { mysql?: string; postgres?: string; };
  };
  engineCompare?: { mysql?: object; postgres?: object; };
  metadata: {
    aiDraftVersion?: string;
    teacherVersion: number;
    lastAiAction?: 'full-generate' | 'regenerate-step' | 'teacher-edit';
  };
  playback: { defaultStepDurationMs: number; subtitles?: { zh?: string; en?: string; }; };
}

interface DemoStep {
  id: string;
  order: number;
  workflowPhase: string;
  narration: { zh: string; en: string; source: 'ai' | 'teacher'; };
  visuals?: { type: string; highlightRange?: number[]; };
  groundingRef?: string;
  timing?: { durationMs: number; };
}
