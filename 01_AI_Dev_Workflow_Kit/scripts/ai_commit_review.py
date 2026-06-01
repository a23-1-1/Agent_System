#!/usr/bin/env python3
"""
AI Commit Review — 读取 git diff 并生成 Code Review 报告。

用法:
    python scripts/ai_commit_review.py              # 审查 staged changes
    python scripts/ai_commit_review.py --unstaged   # 审查 unstaged changes
    python scripts/ai_commit_review.py --commit HEAD~1  # 审查指定 commit

环境变量（可复制 .env.example 为 .env）:
    DEEPSEEK_API_KEY      必填
    DEEPSEEK_BASE_URL     默认 https://api.deepseek.com
    DEEPSEEK_MODEL        默认 deepseek-chat
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = PROJECT_ROOT / "prompts" / "code_review.md"
LOGS_DIR = PROJECT_ROOT / "logs"
DIFF_MAX_CHARS = 8000

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"

FALLBACK_SYSTEM_PROMPT = """你是一个严格的 Code Reviewer，请审查用户提供的代码变更。

## 请按优先级输出

### P0 — 必须修复
- Bug、安全漏洞、数据丢失风险

### P1 — 强烈建议修复
- 逻辑错误、性能问题、缺少错误处理

### P2 — 建议改进
- 可读性、命名、重复代码、测试覆盖

### P3 — 风格建议
- 格式、注释（仅当影响理解时）

## 每个问题请包含

- 文件和行号（如能定位）
- 问题描述
- 建议修复方式
- 严重程度（P0-P3）

## 要求

- 不要误报纯风格偏好
- 关注逻辑正确性和边界条件
- 如果没有问题，明确说「LGTM」并说明审查范围
"""


def load_dotenv() -> None:
    try:
        from dotenv import load_dotenv as _load_dotenv
    except ImportError:
        return
    _load_dotenv(PROJECT_ROOT / ".env")


def get_git_diff(staged: bool = True, commit: str | None = None) -> str:
    if commit:
        cmd = ["git", "diff", f"{commit}^", commit]
    elif staged:
        cmd = ["git", "diff", "--cached"]
    else:
        cmd = ["git", "diff"]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=PROJECT_ROOT.parent,
    )
    if result.returncode != 0:
        print(f"Error running git diff: {result.stderr}", file=sys.stderr)
        print("Hint: run `git init` in Agent_System if this is a new repo.", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def load_system_prompt() -> str:
    if not PROMPT_FILE.exists():
        return FALLBACK_SYSTEM_PROMPT

    text = PROMPT_FILE.read_text(encoding="utf-8")
    marker = "```markdown\n"
    start = text.find(marker)
    if start == -1:
        return text.strip() or FALLBACK_SYSTEM_PROMPT

    start += len(marker)
    section_end = text.find("\n---\n", start)
    if section_end == -1:
        section_end = len(text)

    prompt = text[start:section_end].rstrip()
    if prompt.endswith("```"):
        prompt = prompt[: prompt.rfind("```")].rstrip()

    diff_header = "## Git Diff"
    if diff_header in prompt:
        before, after = prompt.split(diff_header, 1)
        after = after.lstrip()
        if after.startswith("```"):
            closing = after.find("\n```", 3)
            if closing != -1:
                after = after[closing + 4 :]
        prompt = f"{before.rstrip()}\n\n{after.lstrip()}".strip()

    return prompt or FALLBACK_SYSTEM_PROMPT


def truncate_diff(diff: str) -> tuple[str, bool]:
    if len(diff) <= DIFF_MAX_CHARS:
        return diff, False
    return diff[:DIFF_MAX_CHARS], True


def build_user_message(diff: str, truncated: bool) -> str:
    message = f"请审查以下 Git Diff：\n\n```diff\n{diff}\n```"
    if truncated:
        message += (
            f"\n\n> 注意：diff 已截断至前 {DIFF_MAX_CHARS} 字符，"
            "请在报告开头说明审查范围可能不完整。"
        )
    return message


def get_llm_config() -> tuple[str, str, str]:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        print("Error: DEEPSEEK_API_KEY is not set.", file=sys.stderr)
        print(
            f"Hint: copy `{PROJECT_ROOT / '.env.example'}` to `.env` and add your key.",
            file=sys.stderr,
        )
        sys.exit(1)

    base_url = os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL).strip() or DEFAULT_BASE_URL
    model = os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    return api_key, base_url, model


def call_deepseek(system_prompt: str, user_message: str) -> str:
    try:
        from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError
    except ImportError:
        print("Error: openai package is not installed.", file=sys.stderr)
        print("Hint: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    api_key, base_url, model = get_llm_config()
    client = OpenAI(api_key=api_key, base_url=base_url)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
    except RateLimitError as exc:
        print(f"Error: DeepSeek API rate limit exceeded: {exc}", file=sys.stderr)
        sys.exit(1)
    except APITimeoutError as exc:
        print(f"Error: DeepSeek API request timed out: {exc}", file=sys.stderr)
        sys.exit(1)
    except APIConnectionError as exc:
        print(f"Error: failed to connect to DeepSeek API: {exc}", file=sys.stderr)
        sys.exit(1)
    except APIStatusError as exc:
        print(f"Error: DeepSeek API returned {exc.status_code}: {exc.message}", file=sys.stderr)
        sys.exit(1)

    content = response.choices[0].message.content
    if not content:
        print("Error: DeepSeek API returned an empty response.", file=sys.stderr)
        sys.exit(1)
    return content.strip()


def describe_review_scope(unstaged: bool, commit: str | None) -> str:
    if commit:
        return f"commit `{commit}`"
    if unstaged:
        return "unstaged changes"
    return "staged changes"


def generate_review_report(diff: str, review_scope: str) -> str:
    truncated_diff, was_truncated = truncate_diff(diff)
    system_prompt = load_system_prompt()
    user_message = build_user_message(truncated_diff, was_truncated)
    review_body = call_deepseek(system_prompt, user_message)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _, _, model = get_llm_config()

    truncation_note = (
        f"- Diff truncated: yes (first {DIFF_MAX_CHARS} chars)\n"
        if was_truncated
        else "- Diff truncated: no\n"
    )

    return f"""# Code Review Report

> Generated: {timestamp}
> Scope: {review_scope}
> Model: {model}

## Diff Summary

- Lines changed: {len(diff.splitlines())}
- Diff size: {len(diff)} chars
{truncation_note}
## Review

{review_body}
"""


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="AI Commit Review")
    parser.add_argument("--unstaged", action="store_true", help="Review unstaged changes")
    parser.add_argument("--commit", type=str, help="Review specific commit")
    parser.add_argument("--output", type=str, help="Output file path")
    args = parser.parse_args()

    diff = get_git_diff(staged=not args.unstaged, commit=args.commit)
    if not diff.strip():
        print("No changes to review.")
        return

    review_scope = describe_review_scope(args.unstaged, args.commit)
    report = generate_review_report(diff, review_scope)

    LOGS_DIR.mkdir(exist_ok=True)
    output_path = Path(args.output) if args.output else LOGS_DIR / f"review_{datetime.now():%Y%m%d_%H%M%S}.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"Review report saved to: {output_path}")
    print(f"Diff lines: {len(diff.splitlines())}")


if __name__ == "__main__":
    main()
