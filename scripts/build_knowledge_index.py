#!/usr/bin/env python3
"""Build an incremental, content-hash knowledge manifest without vector dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {".git", ".obsidian", ".trash", ".venv", "node_modules", "__pycache__", ".codex-index"}
SOURCE_ID_PATTERN = re.compile(r"(?m)^source_id:\s*['\"]?([^'\"\n]+)")
TITLE_PATTERN = re.compile(r"(?m)^#\s+(.+?)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an incremental Markdown knowledge manifest.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def normalized_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    return ("\n".join(lines).strip() + "\n").encode("utf-8")


def load_manifest(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def source_id_for(path: Path, root: Path, text: str, content_hash: str, prior: dict) -> str:
    explicit = SOURCE_ID_PATTERN.search(text)
    if explicit:
        return explicit.group(1).strip()
    matching_prior = [
        item for item in prior.get("files", [])
        if isinstance(item, dict) and item.get("content_hash") == content_hash
    ]
    if len(matching_prior) == 1 and isinstance(matching_prior[0].get("source_id"), str):
        return matching_prior[0]["source_id"]
    relative = str(path.relative_to(root)).replace("\\", "/").casefold()
    return "path-" + hashlib.sha256(relative.encode("utf-8")).hexdigest()[:20]


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    output = (args.output or root / ".codex-index" / "knowledge-manifest.json").expanduser().resolve()
    prior = load_manifest(output)
    prior_by_id = {
        item.get("source_id"): item for item in prior.get("files", [])
        if isinstance(item, dict) and isinstance(item.get("source_id"), str)
    }

    entries = []
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        data = normalized_bytes(path)
        text = data.decode("utf-8")
        content_hash = hashlib.sha256(data).hexdigest()
        source_id = source_id_for(path, root, text, content_hash, prior)
        title_match = TITLE_PATTERN.search(text)
        entries.append({
            "source_id": source_id,
            "path": str(path.relative_to(root)).replace("\\", "/"),
            "title": title_match.group(1).strip() if title_match else path.stem,
            "content_hash": content_hash,
            "size": len(data),
        })

    current_by_id = {item["source_id"]: item for item in entries}
    new = [key for key in current_by_id if key not in prior_by_id]
    updated = [
        key for key, item in current_by_id.items()
        if key in prior_by_id and item["content_hash"] != prior_by_id[key].get("content_hash")
    ]
    moved = [
        key for key, item in current_by_id.items()
        if key in prior_by_id
        and item["content_hash"] == prior_by_id[key].get("content_hash")
        and item["path"] != prior_by_id[key].get("path")
    ]
    unchanged = [
        key for key, item in current_by_id.items()
        if key in prior_by_id
        and item["content_hash"] == prior_by_id[key].get("content_hash")
        and item["path"] == prior_by_id[key].get("path")
    ]
    deleted = [key for key in prior_by_id if key not in current_by_id]

    by_hash: dict[str, list[str]] = {}
    for item in entries:
        by_hash.setdefault(item["content_hash"], []).append(item["path"])
    duplicates = [
        {"content_hash": digest, "canonical": sorted(paths)[0], "duplicates": sorted(paths)[1:]}
        for digest, paths in by_hash.items() if len(paths) > 1
    ]

    result = {
        "schema_version": 1,
        "root": str(root),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "strategy": "source_id+content_hash; no vector index",
        "files": entries,
        "duplicates": duplicates,
        "changes": {
            "new": new,
            "updated": updated,
            "moved": moved,
            "unchanged": unchanged,
            "deleted": deleted,
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "indexed",
        "output": str(output),
        "files": len(entries),
        "new": len(new),
        "updated": len(updated),
        "moved": len(moved),
        "unchanged": len(unchanged),
        "deleted": len(deleted),
        "duplicate_groups": len(duplicates),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
