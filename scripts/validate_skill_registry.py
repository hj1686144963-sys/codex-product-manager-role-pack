#!/usr/bin/env python3
"""Validate the generated Skill registry and merge lineage on Python-capable hosts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills" / "REGISTRY.json"
CATALOG = ROOT / "skills" / "CATALOG.json"
ALLOWED_STATUSES = {"draft", "candidate", "active", "deprecated", "retired"}
ALLOWED_RISKS = {"read-only", "local-write", "external-write", "high-impact"}


def main() -> int:
    payload = json.loads(REGISTRY.read_text(encoding="utf-8-sig"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    if payload.get("schema_version") != 3:
        errors.append("schema_version must be 3")
    if payload.get("generated") is not True:
        errors.append("registry must be generated")
    skills = payload.get("skills", [])
    names = [item.get("name") for item in skills]
    if len(names) != len(set(names)):
        errors.append("duplicate Skill names in registry")

    known = set(names)
    catalog_names = {item.get("name") for item in catalog.get("skills", [])}
    if known != catalog_names:
        errors.append("catalog and registry Skill names differ")
    categories = set(catalog.get("category_taxonomy", {}))
    for item in skills:
        name = item.get("name", "<missing-name>")
        for field in (
            "version", "status", "category", "risk", "capability_summary",
            "route_description", "capabilities", "source", "skill_sha256",
            "capability_manual", "merged_from",
        ):
            if field not in item:
                errors.append(f"{name}: missing {field}")
        if item.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{name}: invalid status {item.get('status')}")
        if item.get("risk") not in ALLOWED_RISKS:
            errors.append(f"{name}: invalid risk {item.get('risk')}")
        if item.get("category") not in categories:
            errors.append(f"{name}: unknown category {item.get('category')}")
        if item.get("status") in {"candidate", "active", "deprecated"}:
            skill_path = ROOT / "skills" / name / "SKILL.md"
            if not skill_path.is_file():
                errors.append(f"{name}: registered but missing SKILL.md")
        if not isinstance(item.get("capabilities"), list) or not item.get("capabilities"):
            errors.append(f"{name}: capabilities must be a non-empty list")
        digest = item.get("skill_sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            errors.append(f"{name}: invalid skill_sha256")
        merged_from = item.get("merged_from") or []
        if merged_from and not item.get("merge_notes"):
            errors.append(f"{name}: merged Skill requires merge_notes")
        for origin in merged_from:
            origin_name = origin.get("name") if isinstance(origin, dict) else origin
            if origin_name not in known:
                errors.append(f"{name}: unknown merged_from Skill {origin_name}")
        if item.get("status") in {"deprecated", "retired"} and not item.get("successor"):
            errors.append(f"{name}: deprecated or retired Skill requires successor")

    result = {"status": "pass" if not errors else "fail", "skill_count": len(skills), "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
