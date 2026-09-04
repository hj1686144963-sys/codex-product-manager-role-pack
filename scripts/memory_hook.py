#!/usr/bin/env python3
"""Codex lifecycle hook for selective local-memory retrieval.

The hook never sends data to a network service. It returns small, redacted
excerpts as additional developer context and writes content-free session audit
records.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PLUGIN_NAME = "codex-product-manager-role-pack"
RUNTIME_FILE = "codex-product-manager-role-pack.json"
SKIP_DIRS = {
    ".git",
    ".obsidian",
    ".trash",
    ".venv",
    "node_modules",
    "__pycache__",
}
SKIP_NAMES = {
    "auth.json",
    ".env",
    ".env.local",
    ".env.production",
}
STOPWORDS = {
    "这个",
    "那个",
    "一下",
    "帮我",
    "需要",
    "可以",
    "怎么",
    "什么",
    "里面",
    "我的",
    "我们",
    "一个",
    "已经",
    "进行",
    "还是",
    "以及",
    "然后",
    "the",
    "and",
    "for",
    "with",
    "from",
    "this",
    "that",
}
SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"(?i)\b(api[_ -]?key|token|password|secret|cookie)\b\s*[:=]\s*\S+"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S),
]


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def load_runtime() -> dict[str, Any]:
    path = codex_home() / RUNTIME_FILE
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def emit_context(event: str, text: str) -> None:
    payload = {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": text,
        }
    }
    print(json.dumps(payload, ensure_ascii=False))


def redact(text: str) -> str:
    result = text
    for pattern in SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def keywords(text: str) -> list[str]:
    found: set[str] = set()
    for word in re.findall(r"[A-Za-z][A-Za-z0-9_.+-]{1,}", text.casefold()):
        if word not in STOPWORDS:
            found.add(word)
    for run in re.findall(r"[\u4e00-\u9fff]{2,}", text):
        if run not in STOPWORDS and len(run) <= 12:
            found.add(run)
        max_size = min(4, len(run))
        for size in range(2, max_size + 1):
            for index in range(0, len(run) - size + 1):
                token = run[index : index + size]
                if token not in STOPWORDS:
                    found.add(token)
    return sorted(found, key=lambda item: (-len(item), item))[:40]


def markdown_files(
    vault: Path,
    max_files: int,
    allowed_prefixes: list[str] | None = None,
    excluded_prefixes: list[str] | None = None,
) -> list[Path]:
    candidates: list[Path] = []
    allowed = [item.strip("/") for item in (allowed_prefixes or []) if item.strip("/")]
    excluded = [item.strip("/") for item in (excluded_prefixes or []) if item.strip("/")]
    try:
        for path in vault.rglob("*.md"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.name in SKIP_NAMES:
                continue
            relative = str(path.relative_to(vault)).replace("\\", "/")
            if allowed and not any(
                relative == prefix or relative.startswith(prefix + "/")
                for prefix in allowed
            ):
                continue
            if excluded and any(
                relative == prefix or relative.startswith(prefix + "/")
                for prefix in excluded
            ):
                continue
            try:
                if path.stat().st_size > 512_000:
                    continue
            except OSError:
                continue
            candidates.append(path)
            if len(candidates) >= max_files:
                break
    except OSError:
        return []
    return candidates


def path_score(path: Path, vault: Path, terms: list[str]) -> float:
    rel = str(path.relative_to(vault)).casefold()
    stem = path.stem.casefold()
    score = 0.0
    for term in terms:
        term_folded = term.casefold()
        if term_folded in stem:
            score += 8.0
        elif term_folded in rel:
            score += 4.0
    if path.name in {"START-HERE.md", "AGENTS.md"}:
        score += 0.25
    return score


def content_score(text: str, terms: list[str]) -> float:
    folded = text.casefold()
    headings = "\n".join(
        line for line in text.splitlines()[:200] if line.lstrip().startswith("#")
    ).casefold()
    score = 0.0
    for term in terms:
        value = term.casefold()
        score += min(folded.count(value), 5) * 1.25
        if value in headings:
            score += 3.0
    return score


def markdown_sections(text: str) -> list[dict[str, str]]:
    """Split Markdown into small sections while preserving the heading ancestry."""
    sections: list[dict[str, str]] = []
    headings: dict[int, str] = {}
    introductions: dict[int, str] = {}
    current_lines: list[str] = []
    current_level = 0
    current_context = "文档开头"
    current_parent_intro = ""

    def flush() -> None:
        nonlocal current_lines
        body = "\n".join(current_lines).strip()
        if not body:
            current_lines = []
            return
        plain_lines = [
            line.strip()
            for line in current_lines
            if line.strip() and not line.lstrip().startswith("#")
        ]
        intro = " ".join(plain_lines)[:240]
        if current_level:
            introductions[current_level] = intro
        sections.append(
            {
                "context": current_context,
                "parent_intro": current_parent_intro,
                "text": body,
            }
        )
        current_lines = []

    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            current_lines.append(line)
            continue
        flush()
        current_level = len(match.group(1))
        for level in list(headings):
            if level >= current_level:
                headings.pop(level, None)
                introductions.pop(level, None)
        headings[current_level] = match.group(2).strip()
        current_context = " > ".join(
            headings[level] for level in sorted(headings) if level <= current_level
        )
        parent_levels = [level for level in introductions if level < current_level]
        current_parent_intro = (
            introductions[max(parent_levels)] if parent_levels else ""
        )
        current_lines = [line]
    flush()
    return sections


def safe_read(path: Path, limit: int = 12_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def excerpt(section: dict[str, str], terms: list[str], limit: int) -> str:
    text = section.get("text", "")
    if not text:
        return ""
    folded = text.casefold()
    positions = [
        folded.find(term.casefold())
        for term in terms
        if folded.find(term.casefold()) >= 0
    ]
    start = max(0, (min(positions) if positions else 0) - 180)
    context = section.get("context", "文档开头")
    parent_intro = section.get("parent_intro", "")
    prefix = f"章节路径：{context}"
    if parent_intro:
        prefix += f"\n上级摘要：{parent_intro[:240]}"
    body_limit = max(240, limit - len(prefix) - 2)
    snippet = text[start : start + body_limit]
    if start:
        snippet = "…" + snippet
    if start + body_limit < len(text):
        snippet += "…"
    return redact(f"{prefix}\n{snippet.strip()}")


def retrieve(prompt: str, runtime: dict[str, Any]) -> list[dict[str, Any]]:
    vault_value = runtime.get("vault_path")
    if not isinstance(vault_value, str) or not vault_value:
        return []
    vault = Path(vault_value).expanduser()
    if not vault.is_dir():
        return []

    max_files = int(runtime.get("max_files", 800))
    max_results = int(runtime.get("max_results", 4))
    max_excerpt = int(runtime.get("max_excerpt_chars", 900))
    terms = keywords(prompt)
    if not terms:
        return []

    allowed_prefixes = runtime.get("allowed_prefixes")
    excluded_prefixes = runtime.get("excluded_prefixes")
    files = markdown_files(
        vault,
        max_files,
        allowed_prefixes if isinstance(allowed_prefixes, list) else None,
        excluded_prefixes if isinstance(excluded_prefixes, list) else None,
    )
    path_ranked = sorted(
        ((path_score(path, vault, terms), path) for path in files),
        key=lambda item: (item[0], item[1].stat().st_mtime if item[1].exists() else 0),
        reverse=True,
    )
    likely = [item for item in path_ranked if item[0] > 0][:40]
    if not likely:
        recent = sorted(
            files,
            key=lambda path: path.stat().st_mtime if path.exists() else 0,
            reverse=True,
        )[:20]
        likely = [(0.0, path) for path in recent]

    scored: list[tuple[float, Path, dict[str, str]]] = []
    now = datetime.now(timezone.utc).timestamp()
    for initial, path in likely:
        text = safe_read(path)
        try:
            age_days = max(0.0, (now - path.stat().st_mtime) / 86400)
            recency = max(0.0, 1.5 - age_days / 120)
        except OSError:
            recency = 0.0
        for section in markdown_sections(text):
            score = initial + content_score(
                f"{section['context']}\n{section['text']}", terms
            ) + recency
            if score > 1.0:
                scored.append((score, path, section))

    results = []
    used_paths: set[Path] = set()
    for score, path, section in sorted(scored, key=lambda item: item[0], reverse=True):
        if path in used_paths:
            continue
        used_paths.add(path)
        results.append(
            {
                "path": str(path.relative_to(vault)),
                "section": section["context"],
                "score": round(score, 2),
                "excerpt": excerpt(section, terms, max_excerpt),
            }
        )
        if len(results) >= max_results:
            break
    return results


def session_start(runtime: dict[str, Any]) -> None:
    vault = runtime.get("vault_path")
    if isinstance(vault, str) and Path(vault).expanduser().is_dir():
        emit_context(
            "SessionStart",
            (
                "自动记忆机制已启用。无需等待用户发送触发口令。"
                f"知识库根目录：{vault}。"
                "先使用已注入的 Codex Memories；需要本地知识时按标题、路径、"
                "元数据和更新时间筛选少量候选。当前指令与可验证事实优先。"
                "仅在产生长期价值时查重后写回，秘密与临时内容不得沉淀。"
            ),
        )
    else:
        emit_context(
            "SessionStart",
            (
                "检测到 codex-product-manager-role-pack 尚未完成初始化。"
                "如用户要求使用跨会话知识库，运行插件 scripts/install.py 后再验证。"
            ),
        )


def prompt_context(data: dict[str, Any], runtime: dict[str, Any]) -> None:
    prompt = data.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        emit_context("UserPromptSubmit", "")
        return
    results = retrieve(prompt, runtime)
    if not results:
        emit_context(
            "UserPromptSubmit",
            (
                "本次未检索到高相关本地知识片段。继续使用 Codex Memories 和当前项目文件；"
                "不要为了填充上下文而扫描全部知识库。"
            ),
        )
        return
    lines = [
        "以下内容由本地知识库按相关性自动检索，仅作为历史上下文；当前指令和最新证据优先："
    ]
    for index, item in enumerate(results, 1):
        lines.append(
            f"\n[{index}] {item['path']}（相关度 {item['score']}）\n{item['excerpt']}"
        )
    emit_context("UserPromptSubmit", "\n".join(lines))


def session_end(data: dict[str, Any], runtime: dict[str, Any]) -> None:
    vault_value = runtime.get("vault_path")
    if not isinstance(vault_value, str) or not vault_value:
        print("{}")
        return
    vault = Path(vault_value).expanduser()
    if not vault.is_dir():
        print("{}")
        return
    audit_dir = vault / "08-System" / "运行记录"
    try:
        audit_dir.mkdir(parents=True, exist_ok=True)
        today = datetime.now().astimezone().strftime("%Y-%m-%d")
        transcript = str(data.get("transcript_path", ""))
        record = {
            "time": datetime.now().astimezone().isoformat(timespec="seconds"),
            "event": "SessionEnd",
            "session_id": data.get("session_id"),
            "cwd": data.get("cwd"),
            "transcript_ref": hashlib.sha256(transcript.encode()).hexdigest()[:16]
            if transcript
            else None,
            "content_stored": False,
        }
        with (audit_dir / f"{today}.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass
    print("{}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: memory_hook.py session-start|prompt|session-end", file=sys.stderr)
        return 2
    event = sys.argv[1]
    data = read_stdin_json()
    runtime = load_runtime()
    if event == "session-start":
        session_start(runtime)
    elif event == "prompt":
        prompt_context(data, runtime)
    elif event == "session-end":
        session_end(data, runtime)
    else:
        print(f"unknown event: {event}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
