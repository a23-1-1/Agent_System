#!/usr/bin/env python3
"""
AI Commit Review — 读取 git diff 并生成 Code Review 报告。

用法:
    python scripts/ai_commit_review.py              # 审查 staged changes
    python scripts/ai_commit_review.py --unstaged   # 审查 unstaged changes
    python scripts/ai_commit_review.py --commit HEAD~1  # 审查指定 commit

TODO (Week 1 Day 5):
    - 接入 LLM API（OpenAI / Claude / 本地模型）
    - 读取 prompts/code_review.md 作为 system prompt
    - 输出 markdown 报告到 logs/
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = PROJECT_ROOT / "prompts" / "code_review.md"
LOGS_DIR = PROJECT_ROOT / "logs"


def get_git_diff(staged: bool = True, commit: str | None = None) -> str:
    if commit:
        cmd = ["git", "diff", f"{commit}^", commit]
    elif staged:
        cmd = ["git", "diff", "--cached"]
    else:
        cmd = ["git", "diff"]

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=PROJECT_ROOT.parent
    )
    if result.returncode != 0:
        print(f"Error running git diff: {result.stderr}", file=sys.stderr)
        print("Hint: run `git init` in Agent_System if this is a new repo.", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def load_prompt_template() -> str:
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text(encoding="utf-8")
    return ""


def generate_review_report(diff: str) -> str:
    """Placeholder — 后续接入 LLM API。"""
    prompt = load_prompt_template()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""# Code Review Report

> Generated: {timestamp}
> Status: **DRAFT — LLM not connected yet**

## Diff Summary

- Lines changed: {len(diff.splitlines())}
- Diff size: {len(diff)} chars

## Diff Content

```diff
{diff[:8000]}
{"...(truncated)" if len(diff) > 8000 else ""}
```

## Next Steps

1. 接入 LLM API（OpenAI / Claude）
2. 使用 `{PROMPT_FILE.name}` 作为 review prompt
3. 输出结构化审查报告（P0-P3 分级）

## Prompt Template Preview

{prompt[:500]}...
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="AI Commit Review")
    parser.add_argument("--unstaged", action="store_true", help="Review unstaged changes")
    parser.add_argument("--commit", type=str, help="Review specific commit")
    parser.add_argument("--output", type=str, help="Output file path")
    args = parser.parse_args()

    diff = get_git_diff(staged=not args.unstaged, commit=args.commit)
    if not diff.strip():
        print("No changes to review.")
        return

    report = generate_review_report(diff)

    LOGS_DIR.mkdir(exist_ok=True)
    output_path = args.output or LOGS_DIR / f"review_{datetime.now():%Y%m%d_%H%M%S}.md"
    Path(output_path).write_text(report, encoding="utf-8")
    print(f"Review report saved to: {output_path}")
    print(f"Diff lines: {len(diff.splitlines())}")


if __name__ == "__main__":
    main()
