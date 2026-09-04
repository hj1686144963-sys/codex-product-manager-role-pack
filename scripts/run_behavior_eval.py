#!/usr/bin/env python3
"""Evaluate required public behavior memories by priority."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    cases = [
        json.loads(line)
        for line in (root / "evaluations" / "behavior-memory.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    sources = [
        root / "knowledge" / "roles" / "product-manager" / "approved" / "behavior-memory.md",
        root / "assets" / "templates" / "global-agents-block.md",
        root / "skills" / "product-manager-core" / "references" / "product-workflows.md",
    ]
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in sources)
    results = []
    for case in cases:
        required = case.get("required_all", [])
        ok = bool(required) and all(isinstance(token, str) and token in corpus for token in required)
        results.append({"id": case["id"], "priority": case["priority"], "ok": ok})

    scores = {}
    for priority in ("P0", "P1"):
        group = [item for item in results if item["priority"] == priority]
        passed = sum(1 for item in group if item["ok"])
        scores[priority] = {
            "passed": passed,
            "total": len(group),
            "rate": round(passed / len(group), 4) if group else 0.0,
        }
    ok = scores["P0"]["rate"] == 1.0 and scores["P1"]["rate"] >= 0.95
    print(json.dumps({"status": "pass" if ok else "fail", "scores": scores, "cases": results}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
