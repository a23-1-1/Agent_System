#!/usr/bin/env python3
"""
demo-schema 校验脚本

用途：
  验证 DemoPackage JSON 是否符合 schema.json 定义的基本约束。
  纯本地运行，不依赖 LLM / 网络。

用法：
  python validate.py                          # 校验默认样例
  python validate.py examples/join-query.json  # 校验指定文件
  python validate.py ../../logs/*.json         # 批量校验

验收标准（对应 day3_guide 验收清单）：
  1. schema.json 能通过 JSON Schema 基本校验
  2. examples/join-query.json 包含 ≥5 步，step 数组不为空
  3. 每个 step 都含 workflowPhase 字段，值取自枚举
  4. DemoPackage 顶层含 id、title.zh、title.en
  5. 至少包含 3 种不同的 workflowPhase
"""

import json
import sys
import os
from pathlib import Path

# ── 从 schema.json 读取枚举 ────────────────────────────────────────
_SCHEMA_DIR = Path(__file__).parent
_SCHEMA_PATH = _SCHEMA_DIR / "schema.json"

VALID_PHASES = set()
VALID_STEP_SOURCES = set()
VALID_AI_ACTIONS = set()
VALID_WORKFLOW_TYPES = set()

try:
    with open(_SCHEMA_PATH, encoding="utf-8") as f:
        _schema = json.load(f)
    _step_def = _schema.get("definitions", {}).get("DemoStep", {}).get("properties", {})
    _phase_enum = _step_def.get("workflowPhase", {}).get("enum", [])
    VALID_PHASES = set(_phase_enum)
    _source_enum = _step_def.get("narration", {}).get("properties", {}).get("source", {}).get("enum", [])
    VALID_STEP_SOURCES = set(_source_enum)
    _trace_props = _schema.get("properties", {}).get("workflowTrace", {}).get("properties", {})
    _wt_enum = _trace_props.get("workflowType", {}).get("enum", [])
    VALID_WORKFLOW_TYPES = set(_wt_enum)
    _meta_props = _schema.get("properties", {}).get("metadata", {}).get("properties", {})
    _action_enum = _meta_props.get("lastAiAction", {}).get("enum", [])
    VALID_AI_ACTIONS = set(_action_enum)
except (FileNotFoundError, json.JSONDecodeError, KeyError):
    # 降级：schema.json 不可用时用硬编码
    VALID_PHASES = {"lex", "parse", "optimize", "plan", "execute", "result", "concept", "transform", "compare", "summary"}
    VALID_STEP_SOURCES = {"ai", "teacher"}
    VALID_WORKFLOW_TYPES = {"sql-execution", "concept-progression"}
    VALID_AI_ACTIONS = {"full-generate", "regenerate-step", "teacher-edit"}

# ── 错误收集 ────────────────────────────────────────────────────────
errors = []
warnings = []
warnings = []

def err(file: str, msg: str):
    errors.append(f"  [ERR] {file}: {msg}")

def warn(file: str, msg: str):
    warnings.append(f"  [WARN] {file}: {msg}")


# ── 单文件校验 ──────────────────────────────────────────────────────
def validate(filepath: str) -> bool:
    local_errors = []
    path = Path(filepath)

    if not path.exists():
        err(filepath, "文件不存在")
        return False

    try:
        with open(path, encoding="utf-8") as f:
            dp = json.load(f)
    except json.JSONDecodeError as e:
        err(filepath, f"JSON 解析失败: {e}")
        return False
    except UnicodeDecodeError as e:
        err(filepath, f"文件编码错误（非 UTF-8）: {e}")
        return False

    ok = True

    # 1. 顶层必填字段
    for field in ("id", "title", "steps", "metadata", "playback"):
        if field not in dp:
            err(filepath, f"缺少顶层字段: {field}")
            ok = False

    # 2. id 格式
    if "id" in dp and not isinstance(dp["id"], str):
        err(filepath, "id 必须是字符串")
        ok = False

    # 3. title
    title = dp.get("title", {})
    if not isinstance(title, dict):
        err(filepath, "title 必须是对象")
        ok = False
    else:
        for lang in ("zh", "en"):
            if lang not in title or not title[lang]:
                err(filepath, f"title.{lang} 缺失或为空")
                ok = False
            elif lang == "en" and title.get("en") and len(title["en"].strip()) < 5:
                warn(filepath, f"title.en 内容过短: '{title['en']}'")

    # 4. steps 数组
    steps = dp.get("steps", [])
    if not isinstance(steps, list):
        err(filepath, "steps 必须是数组")
        ok = False
    elif len(steps) == 0:
        err(filepath, "steps 数组为空")
        ok = False
    else:
        # 4a. order 连续
        for i, step in enumerate(steps):
            expected = i + 1
            actual = step.get("order")
            if actual != expected:
                err(filepath, f"step[{i}] order={actual}，期望 {expected}")
                ok = False

        # 4b. 每个 step 检查
        for i, step in enumerate(steps):
            sid = f"steps[{i}] (id={step.get('id', '?')})"

            if "id" not in step:
                err(filepath, f"{sid} 缺少 id")
                ok = False

            if "workflowPhase" not in step:
                err(filepath, f"{sid} 缺少 workflowPhase")
                ok = False
            elif step["workflowPhase"] not in VALID_PHASES:
                err(filepath, f"{sid} workflowPhase='{step['workflowPhase']}' 不在合法枚举中")
                ok = False

            narration = step.get("narration", {})
            if not isinstance(narration, dict):
                err(filepath, f"{sid} narration 必须是对象")
                ok = False
            elif "zh" not in narration or not narration["zh"]:
                err(filepath, f"{sid} narration.zh 缺失或为空")
                ok = False

            source = narration.get("source") if isinstance(narration, dict) else None
            if source and source not in VALID_STEP_SOURCES:
                err(filepath, f"{sid} narration.source='{source}' 不合法")
                ok = False

            # visuals 类型（如果有）
            visuals = step.get("visuals")
            if visuals and not isinstance(visuals, dict):
                err(filepath, f"{sid} visuals 必须是对象")
                ok = False

        # 4c. groundingRef 条件校验：SQL 执行流的 plan/execute 步必须有 groundingRef
        workflow_type = dp.get("workflowTrace", {}).get("workflowType") if isinstance(dp.get("workflowTrace"), dict) else None
        if workflow_type == "sql-execution":
            for i, step in enumerate(steps):
                phase = step.get("workflowPhase")
                if phase in ("plan", "execute") and not step.get("groundingRef"):
                    sid = f"steps[{i}] (id={step.get('id', '?')})"
                    err(filepath, f"{sid} workflowType=sql-execution, phase={phase}, 但 groundingRef 缺失")
                    ok = False

        # 4c. 唯一 phase 数 >= 3
        phases = {s.get("workflowPhase") for s in steps if s.get("workflowPhase") in VALID_PHASES}
        if len(phases) < 3:
            err(filepath, f"唯一 workflowPhase 数={len(phases)}，要求 ≥3")
            ok = False

    # 5. metadata
    meta = dp.get("metadata", {})
    if not isinstance(meta, dict):
        err(filepath, "metadata 必须是对象")
        ok = False
    elif "teacherVersion" not in meta:
        err(filepath, "metadata.teacherVersion 缺失")
        ok = False
    else:
        if not isinstance(meta["teacherVersion"], int) or meta["teacherVersion"] < 1:
            err(filepath, f"metadata.teacherVersion={meta['teacherVersion']} 必须为正整数")
            ok = False

    last_action = meta.get("lastAiAction") if isinstance(meta, dict) else None
    if last_action and last_action not in VALID_AI_ACTIONS:
        err(filepath, f"metadata.lastAiAction='{last_action}' 不合法")
        ok = False

    # 6. playback
    playback = dp.get("playback", {})
    if not isinstance(playback, dict):
        err(filepath, "playback 必须是对象")
        ok = False
    elif "defaultStepDurationMs" not in playback:
        err(filepath, "playback.defaultStepDurationMs 缺失")
        ok = False
    elif not isinstance(playback["defaultStepDurationMs"], int) or playback["defaultStepDurationMs"] < 1000:
        err(filepath, f"playback.defaultStepDurationMs={playback.get('defaultStepDurationMs')} 必须 ≥1000")
        ok = False

    # 7. workflowTrace（可选校验）
    trace = dp.get("workflowTrace")
    if trace:
        if not isinstance(trace, dict):
            err(filepath, "workflowTrace 必须是对象")
            ok = False
        elif trace.get("workflowType") and trace["workflowType"] not in VALID_WORKFLOW_TYPES:
            err(filepath, f"workflowTrace.workflowType='{trace['workflowType']}' 不合法")
            ok = False

    # 8. 级数限制（防止特大文件）
    if len(steps) > 100:
        err(filepath, f"steps 数量={len(steps)}，超过 100 步限制")
        ok = False

    # ── 汇总 ──
    if ok:
        phases_used = ", ".join(sorted(phases)) if steps else "(无)"
        print(f"  [OK] {path.name}: {len(steps)} 步, phases=[{phases_used}]")
    else:
        pass  # 错误已收集到全局 errors

    return ok


# ── 主入口 ──────────────────────────────────────────────────────────
def main():
    global errors
    global warnings

    # 默认搜索路径
    default_patterns = [
        "examples/join-query.json",
        "examples/*.json",
    ]

    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        # 自动发现
        script_dir = Path(__file__).parent
        targets = []
        for pat in default_patterns:
            targets.extend(str(p) for p in sorted(script_dir.glob(pat)))
        if not targets:
            print("用法: python validate.py <path_to_demo_package.json>")
            sys.exit(1)

    print(f"\n{'='*50}")
    print(f"  DemoPackage Validator")
    print(f"{'='*50}\n")

    passed = 0
    failed = 0

    for target in targets:
        errors_before = len(errors)
        ok = validate(target)
        if ok:
            passed += 1
        else:
            failed += 1

    print()
    if errors:
        print("--- ERRORS ---")
        for e in errors:
            print(e)
    if warnings:
        print("--- WARNINGS ---")
        for w in warnings:
            print(w)

    print(f"\n{'='*50}")
    print(f"  结果: {passed} OK, {failed} FAILED, {len(errors)} ERRORS")
    print(f"{'='*50}\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
