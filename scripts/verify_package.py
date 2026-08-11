#!/usr/bin/env python3
"""Validate the distributable plugin package without installing it."""

from __future__ import annotations

import json
import hashlib
import py_compile
import re
import sys
import tempfile
from pathlib import Path

PLUGIN_NAME = "codex-product-manager-role-pack"
REQUIRED = [
    ".codex-plugin/plugin.json",
    "skills/codex-auto-memory/SKILL.md",
    "skills/codex-auto-memory/references/memory-policy.md",
    "skills/product-manager-core/SKILL.md",
    "skills/product-manager-core/references/product-workflows.md",
    "skills/product-manager-core/references/promotion-policy.md",
    "skills/five-role-deliberation/SKILL.md",
    "skills/five-role-deliberation/references/protocol.md",
    "skills/leiniao-ui-design-baseline/SKILL.md",
    "skills/leiniao-ui-design-baseline/references/ui-visual-design-baseline.md",
    "agents/coordinator.toml",
    "agents/researcher.toml",
    "agents/product-strategist.toml",
    "agents/system-strategist.toml",
    "agents/red-team-editor.toml",
    "scripts/install.py",
    "scripts/memory_hook.py",
    "scripts/verify.py",
    "scripts/rollback.py",
    "scripts/build_package.py",
    "scripts/build_knowledge_index.py",
    "scripts/run_role_eval.py",
    "scripts/validate_skill_registry.py",
    "assets/templates/global-agents-block.md",
    "assets/knowledge-base/START-HERE.md",
    "assets/knowledge-base/AGENTS.md",
    "assets/knowledge-base/01-Role/产品经理岗位画像.md",
    "assets/knowledge-base/04-Methods/雷鸟UI设计基线.md",
    "assets/knowledge-base/08-System/防踩坑记录.md",
    "README.md",
    "SHARE-PROMPT.md",
    "environment/DEPENDENCIES.md",
    "environment/REBUILD-CHECKLIST.md",
    "environment/ENVIRONMENT-MANIFEST.json",
    "REBUILD-CHECKLIST.md",
    "docs/MULTI-USER-KNOWLEDGE.md",
    "docs/SKILL-LIFECYCLE.md",
    "knowledge/README.md",
    "knowledge/templates/knowledge-object.md",
    "evaluations/product-manager.jsonl",
    "skills/REGISTRY.json",
    "skills/product-manager-core/references/knowledge-governance.md",
    "docs/DASHI-TASKBOARD-INTEGRATION.md",
    "docs/RELEASE-0.3.0.md",
    "scripts/Initialize-WorkspaceFolders.ps1",
    "release/versions/v0.3.0/manifest.json",
]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    checks = []
    for relative in REQUIRED:
        exists = (root / relative).is_file()
        checks.append({"check": f"file:{relative}", "ok": exists})

    try:
        manifest = json.loads(
            (root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        manifest_ok = (
            manifest.get("name") == PLUGIN_NAME
            and bool(re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", manifest.get("version", "")))
        )
    except (OSError, json.JSONDecodeError):
        manifest_ok = False
    checks.append({"check": "manifest", "ok": manifest_ok})

    install_text = (root / "scripts" / "install.py").read_text(encoding="utf-8")
    hooks_ok = all(
        token in install_text
        for token in ("SessionStart", "UserPromptSubmit", "SessionEnd", "merge_user_hooks")
    )
    checks.append({"check": "user_level_hooks_installer", "ok": hooks_ok})

    five_role_ok = all(
        token in install_text
        for token in ("install_role_assets", "five-role-deliberation", "product-manager-core", "max_concurrent_threads_per_session")
    )
    checks.append({"check": "five_role_installer", "ok": five_role_ok})

    governance_ok = all(
        token in (root / "scripts" / "memory_hook.py").read_text(encoding="utf-8")
        for token in ("markdown_sections", "章节路径", "上级摘要")
    )
    checks.append({"check": "parent_context_retrieval", "ok": governance_ok})

    text_files = list(root.rglob("*.md")) + list(root.rglob("*.json"))
    todo_files = []
    for path in text_files:
        try:
            if "[TODO:" in path.read_text(encoding="utf-8"):
                todo_files.append(str(path.relative_to(root)))
        except OSError:
            pass
    checks.append({"check": "no_placeholders", "ok": not todo_files, "files": todo_files})

    compile_errors = []
    with tempfile.TemporaryDirectory(prefix="codex-memory-verify-") as temp_dir:
        for path in (root / "scripts").glob("*.py"):
            try:
                py_compile.compile(
                    str(path),
                    cfile=str(Path(temp_dir) / f"{path.stem}.pyc"),
                    doraise=True,
                )
            except py_compile.PyCompileError as error:
                compile_errors.append(f"{path.name}: {error}")
    checks.append({"check": "python_syntax", "ok": not compile_errors, "errors": compile_errors})

    checksum_path = root / "PACKAGE-CHECKSUMS.json"
    checksum_ok = True
    checksum_errors = []
    if checksum_path.is_file():
        try:
            manifest = json.loads(checksum_path.read_text(encoding="utf-8"))
            for item in manifest.get("files", []):
                path = root / item["path"]
                if not path.is_file():
                    checksum_errors.append(f"missing:{item['path']}")
                    continue
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if digest != item["sha256"]:
                    checksum_errors.append(f"changed:{item['path']}")
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
            checksum_errors.append(str(error))
        checksum_ok = not checksum_errors
    checks.append(
        {
            "check": "package_checksums",
            "ok": checksum_ok,
            "detail": "not built yet" if not checksum_path.exists() else "",
            "errors": checksum_errors,
        }
    )

    forbidden_paths = []
    forbidden_parts = {".git", ".tmp", "node_modules", "__pycache__"}
    forbidden_suffixes = {".sqlite", ".sqlite3", ".db", ".wal", ".shm"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if forbidden_parts.intersection(relative.parts):
            continue
        if path.suffix.lower() in forbidden_suffixes or path.name.endswith(("-wal", "-shm")):
            forbidden_paths.append(str(relative))
    checks.append({"check": "no_runtime_or_database_files", "ok": not forbidden_paths, "files": forbidden_paths})

    private_path_hits = []
    private_path_pattern = re.compile(r"(?:[A-Za-z]:\\Users\\[^\\\s]+|/Users/[^/\s]+)")
    for path in list(root.rglob("*.md")) + list(root.rglob("*.json")) + list(root.rglob("*.ps1")) + list(root.rglob("*.py")):
        relative = path.relative_to(root)
        if forbidden_parts.intersection(relative.parts) or relative == Path("scripts/verify_package.py"):
            continue
        try:
            if private_path_pattern.search(path.read_text(encoding="utf-8")):
                private_path_hits.append(str(path.relative_to(root)))
        except (OSError, UnicodeDecodeError):
            pass
    checks.append({"check": "no_private_absolute_paths", "ok": not private_path_hits, "files": private_path_hits})

    failed = [check for check in checks if not check["ok"]]
    print(
        json.dumps(
            {
                "status": "pass" if not failed else "fail",
                "plugin": PLUGIN_NAME,
                "checks": checks,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
