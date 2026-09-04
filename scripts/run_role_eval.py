#!/usr/bin/env python3
"""Run deterministic retrieval and scope regression cases for the role pack."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run product-manager role retrieval evaluations.")
    parser.add_argument("--cases", type=Path)
    parser.add_argument("--fixtures", type=Path)
    return parser.parse_args()


def load_hook(root: Path):
    path = root / "scripts" / "memory_hook.py"
    spec = importlib.util.spec_from_file_location("role_pack_memory_hook", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    cases_path = (args.cases or root / "evaluations" / "product-manager.jsonl").resolve()
    fixtures = (args.fixtures or root / "evaluations" / "fixtures").resolve()
    hook = load_hook(root)
    results = []
    for line in cases_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        runtime = {
            "vault_path": str(fixtures),
            "max_files": 100,
            "max_results": 3,
            "max_excerpt_chars": 900,
            "allowed_prefixes": case.get("allowed_prefixes", []),
            "excluded_prefixes": case.get("excluded_prefixes", []),
        }
        actual = hook.retrieve(case["query"], runtime)
        paths = [item["path"] for item in actual]
        excerpts = "\n".join(item["excerpt"] for item in actual)
        expected = case.get("expected_any", [])
        forbidden = case.get("forbidden", [])
        ok = (not expected or any(path in paths for path in expected))
        ok = ok and not any(path in paths for path in forbidden)
        required_context = case.get("context_contains", [])
        if isinstance(required_context, str):
            required_context = [required_context]
        if isinstance(required_context, list):
            ok = ok and all(item in excerpts for item in required_context)
        results.append({"id": case["id"], "ok": ok, "paths": paths})
    failed = [item for item in results if not item["ok"]]
    print(json.dumps({"status": "pass" if not failed else "fail", "cases": results}, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
