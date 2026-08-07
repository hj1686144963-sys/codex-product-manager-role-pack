#!/usr/bin/env python3
"""Validate Skill lifecycle metadata and replacement rules."""

from __future__ import annotations

import json
from pathlib import Path

ALLOWED = {"candidate", "active", "deprecated", "retired"}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    registry = json.loads((root / "skills" / "REGISTRY.json").read_text(encoding="utf-8"))
    skills = registry.get("skills", [])
    errors = []
    names = set()
    for item in skills:
        name = item.get("name")
        status = item.get("status")
        if not isinstance(name, str) or not name:
            errors.append("missing skill name")
            continue
        if name in names:
            errors.append(f"duplicate skill: {name}")
        names.add(name)
        if status not in ALLOWED:
            errors.append(f"invalid status for {name}: {status}")
        if status in {"deprecated", "retired"} and not item.get("successor"):
            errors.append(f"{name} requires a successor")
        if status == "active" and not (root / "skills" / name / "SKILL.md").is_file():
            errors.append(f"active skill missing: {name}")
    print(json.dumps({"status": "pass" if not errors else "fail", "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
