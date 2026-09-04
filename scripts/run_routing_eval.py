#!/usr/bin/env python3
"""Run deterministic static checks for the central/product role-routing contract."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    cases = [
        json.loads(line)
        for line in (root / "evaluations" / "role-routing.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    sources = [
        root / "assets" / "templates" / "global-agents-block.md",
        root / "docs" / "ROUTING-PROTOCOL.md",
        root / "skills" / "product-manager-core" / "references" / "role-routing.md",
    ] + list((root / "agents").glob("*.toml"))
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in sources)
    results = []
    for case in cases:
        required = case.get("required_tokens", [])
        ok = all(isinstance(token, str) and token in corpus for token in required)
        results.append({"id": case.get("id"), "ok": ok, "required_tokens": required})
    failed = [item for item in results if not item["ok"]]
    print(json.dumps({"status": "pass" if not failed else "fail", "cases": results}, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
