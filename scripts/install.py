#!/usr/bin/env python3
"""Install the Codex product-manager role pack without overwriting user configuration."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:  # Python 3.10 and earlier
    tomllib = None

PLUGIN_NAME = "codex-product-manager-role-pack"
PLUGIN_VERSION = "0.2.0"
FIVE_ROLE_SKILL = "five-role-deliberation"
DESIGN_SKILL = "leiniao-ui-design-baseline"
AUTO_MEMORY_SKILL = "codex-auto-memory"
PRODUCT_MANAGER_SKILL = "product-manager-core"
BEGIN_MARKER = "<!-- BEGIN codex-product-manager-role-pack -->"
END_MARKER = "<!-- END codex-product-manager-role-pack -->"
MEMORY_VALUES = {
    "generate_memories": "true",
    "use_memories": "true",
    "disable_on_external_context": "false",
    "min_rollout_idle_hours": "1",
    "max_rollout_age_days": "90",
    "max_unused_days": "180",
    "max_rollouts_per_startup": "32",
    "max_raw_memories_for_consolidation": "512",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install cross-chat memories, global guidance, hooks, and a knowledge base."
    )
    parser.add_argument("--yes", action="store_true", help="Run without an interactive confirmation.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned paths without writing.")
    parser.add_argument("--home", type=Path, help="Override the user home directory (for testing).")
    parser.add_argument("--codex-home", type=Path, help="Override CODEX_HOME.")
    parser.add_argument("--vault", type=Path, help="Use an existing or new knowledge-base path.")
    parser.add_argument(
        "--skip-plugin-copy",
        action="store_true",
        help="Configure memories and the vault without copying the plugin.",
    )
    return parser.parse_args()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def backup_file(path: Path, destination: Path) -> bool:
    existed = path.exists()
    if not existed:
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    if path.is_dir():
        shutil.copytree(path, destination)
    else:
        shutil.copy2(path, destination)
    return True


def set_toml_value(text: str, section: str, key: str, value: str) -> str:
    lines = text.splitlines()
    header = f"[{section}]"
    section_start = None
    section_end = len(lines)
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == header:
            section_start = index
            continue
        if section_start is not None and index > section_start:
            if stripped.startswith("[") and stripped.endswith("]"):
                section_end = index
                break

    new_line = f"{key} = {value}"
    if section_start is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend([header, new_line])
        return "\n".join(lines).rstrip() + "\n"

    for index in range(section_start + 1, section_end):
        stripped = lines[index].lstrip()
        if stripped.startswith("#"):
            continue
        left = stripped.split("=", 1)[0].strip() if "=" in stripped else ""
        if left == key:
            indent = lines[index][: len(lines[index]) - len(stripped)]
            lines[index] = indent + new_line
            return "\n".join(lines).rstrip() + "\n"

    lines.insert(section_end, new_line)
    return "\n".join(lines).rstrip() + "\n"


def merge_codex_config(path: Path) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    text = set_toml_value(text, "features", "memories", "true")
    text = set_toml_value(text, "features", "hooks", "true")
    for key, value in MEMORY_VALUES.items():
        text = set_toml_value(text, "memories", key, value)
    text = set_toml_value(text, "agents", "enabled", "true")
    text = set_toml_value(text, "agents", "max_concurrent_threads_per_session", "4")
    text = set_toml_value(text, "agents", "default_subagent_model", '"gpt-5.6-sol"')
    text = set_toml_value(text, "agents", "default_subagent_reasoning_effort", '"medium"')
    if tomllib is not None:
        tomllib.loads(text)
    atomic_write(path, text)


def merge_agents(path: Path, template: Path, vault: Path) -> None:
    block = template.read_text(encoding="utf-8").replace(
        "{{VAULT_PATH}}", str(vault.resolve())
    ).strip()
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    has_begin = BEGIN_MARKER in current
    has_end = END_MARKER in current
    if has_begin != has_end:
        raise RuntimeError(
            f"{path} contains an incomplete {PLUGIN_NAME} marker block; repair it first."
        )
    if has_begin:
        start = current.index(BEGIN_MARKER)
        end = current.index(END_MARKER, start) + len(END_MARKER)
        updated = current[:start].rstrip() + "\n\n" + block + "\n" + current[end:].lstrip()
    else:
        prefix = current.rstrip()
        updated = (prefix + "\n\n" if prefix else "") + block + "\n"
    atomic_write(path, updated)


def active_global_agents(codex: Path) -> Path:
    override = codex / "AGENTS.override.md"
    try:
        if override.is_file() and override.read_text(encoding="utf-8").strip():
            return override
    except OSError:
        pass
    return codex / "AGENTS.md"


def hook_handler(command: str, event: str) -> dict[str, Any]:
    handler: dict[str, Any] = {
        "type": "command",
        "command": f"python3 {shlex.quote(command)} {event}",
        "commandWindows": f'py -3 "{command.replace(chr(34), chr(34) * 2)}" {event}',
        "timeout": 3 if event == "session-end" else 8,
    }
    if event == "session-start":
        handler["statusMessage"] = "加载跨会话记忆规则"
        handler["additionalContextLimit"] = 5000
    elif event == "prompt":
        handler["statusMessage"] = "检索相关本地知识"
        handler["additionalContextLimit"] = 6000
    return handler


def merge_user_hooks(path: Path, runtime_script: Path) -> None:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise RuntimeError(f"Invalid hooks root: {path}")
    else:
        data = {
            "description": "User-level lifecycle hooks. Existing hooks are preserved.",
            "hooks": {},
        }
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise RuntimeError(f"Invalid hooks table: {path}")

    marker = PLUGIN_NAME
    for groups in hooks.values():
        if not isinstance(groups, list):
            continue
        retained_groups = []
        for group in groups:
            if not isinstance(group, dict):
                retained_groups.append(group)
                continue
            handlers = group.get("hooks")
            if not isinstance(handlers, list):
                retained_groups.append(group)
                continue
            retained_handlers = [
                handler
                for handler in handlers
                if not (
                    isinstance(handler, dict)
                    and marker in str(handler.get("command", ""))
                )
            ]
            if retained_handlers:
                updated_group = dict(group)
                updated_group["hooks"] = retained_handlers
                retained_groups.append(updated_group)
        groups[:] = retained_groups

    command = str(runtime_script.resolve())
    hooks.setdefault("SessionStart", []).append(
        {
            "matcher": "startup|resume|clear|compact",
            "hooks": [hook_handler(command, "session-start")],
        }
    )
    hooks.setdefault("UserPromptSubmit", []).append(
        {"hooks": [hook_handler(command, "prompt")]}
    )
    hooks.setdefault("SessionEnd", []).append(
        {"hooks": [hook_handler(command, "session-end")]}
    )
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def copy_missing_tree(source: Path, destination: Path) -> list[str]:
    created: list[str] = []
    for path in source.rglob("*"):
        relative = path.relative_to(source)
        target = destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        created.append(str(relative))
    return created


def install_plugin(source: Path, destination: Path) -> None:
    if source.resolve() == destination.resolve():
        return
    temp_destination = destination.with_name(destination.name + ".installing")
    if temp_destination.exists():
        shutil.rmtree(temp_destination)
    shutil.copytree(
        source,
        temp_destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )
    if destination.exists():
        shutil.rmtree(destination)
    temp_destination.replace(destination)


def replace_tree(source: Path, destination: Path) -> None:
    temp_destination = destination.with_name(destination.name + ".installing")
    if temp_destination.exists():
        shutil.rmtree(temp_destination)
    shutil.copytree(
        source,
        temp_destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_destination.replace(destination)


def install_role_assets(plugin_root: Path, codex: Path, home: Path) -> None:
    """Install the five owned role files and all bundled role-pack skills."""
    role_source = plugin_root / "agents"
    role_destination = codex / "agents"
    role_destination.mkdir(parents=True, exist_ok=True)
    for source in sorted(role_source.glob("*.toml")):
        shutil.copy2(source, role_destination / source.name)

    replace_tree(
        plugin_root / "skills" / FIVE_ROLE_SKILL,
        home / ".agents" / "skills" / FIVE_ROLE_SKILL,
    )
    for skill_name in (DESIGN_SKILL, AUTO_MEMORY_SKILL, PRODUCT_MANAGER_SKILL):
        replace_tree(
            plugin_root / "skills" / skill_name,
            codex / "skills" / skill_name,
        )


def merge_marketplace(path: Path) -> None:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise RuntimeError(f"Invalid marketplace root: {path}")
    else:
        data = {
            "name": "personal",
            "interface": {"displayName": "Personal"},
            "plugins": [],
        }
    data.setdefault("name", "personal")
    interface = data.setdefault("interface", {})
    if isinstance(interface, dict):
        interface.setdefault("displayName", "Personal")
    plugins = data.setdefault("plugins", [])
    if not isinstance(plugins, list):
        raise RuntimeError(f"Invalid plugins list: {path}")
    entry = {
        "name": PLUGIN_NAME,
        "source": {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"},
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Productivity",
    }
    replaced = False
    for index, plugin in enumerate(plugins):
        if isinstance(plugin, dict) and plugin.get("name") == PLUGIN_NAME:
            plugins[index] = entry
            replaced = True
            break
    if not replaced:
        plugins.append(entry)
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def write_runtime(path: Path, vault: Path) -> None:
    data = {
        "version": 2,
        "plugin_version": PLUGIN_VERSION,
        "plugin": PLUGIN_NAME,
        "vault_path": str(vault.resolve()),
        "max_files": 800,
        "max_results": 4,
        "max_excerpt_chars": 900,
    }
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def confirm(args: argparse.Namespace, paths: dict[str, Path]) -> None:
    if args.yes:
        return
    if not sys.stdin.isatty():
        raise RuntimeError("Non-interactive install requires --yes.")
    print("The installer will merge, not replace, existing configuration:")
    for name, path in paths.items():
        print(f"  {name}: {path}")
    answer = input("Continue? [y/N] ").strip().lower()
    if answer not in {"y", "yes"}:
        raise RuntimeError("Installation cancelled.")


def main() -> int:
    args = parse_args()
    plugin_root = Path(__file__).resolve().parent.parent
    home = (args.home or Path.home()).expanduser().resolve()
    codex = (args.codex_home or home / ".codex").expanduser().resolve()
    vault = (args.vault or home / "Documents" / "Codex-Obsidian-Vault-Product-Manager").expanduser().resolve()
    marketplace = home / ".agents" / "plugins" / "marketplace.json"
    plugin_destination = home / "plugins" / PLUGIN_NAME
    role_destination = codex / "agents"
    deliberation_skill = home / ".agents" / "skills" / FIVE_ROLE_SKILL
    design_skill = codex / "skills" / DESIGN_SKILL
    auto_memory_skill = codex / "skills" / AUTO_MEMORY_SKILL
    product_manager_skill = codex / "skills" / PRODUCT_MANAGER_SKILL
    global_agents = active_global_agents(codex)
    user_hooks = codex / "hooks.json"
    hook_runtime = codex / PLUGIN_NAME
    paths = {
        "Codex config": codex / "config.toml",
        "Global guidance": global_agents,
        "User hooks": user_hooks,
        "Hook runtime": hook_runtime,
        "Runtime config": codex / f"{PLUGIN_NAME}.json",
        "Knowledge base": vault,
        "Plugin": plugin_destination,
        "Five-role agents": role_destination,
        "Five-role skill": deliberation_skill,
        "Design baseline skill": design_skill,
        "Auto-memory skill": auto_memory_skill,
        "Product-manager skill": product_manager_skill,
        "Personal marketplace": marketplace,
    }
    confirm(args, paths)

    if args.dry_run:
        print(json.dumps({key: str(value) for key, value in paths.items()}, ensure_ascii=False, indent=2))
        return 0

    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S-%f")
    backup = codex / "backups" / PLUGIN_NAME / timestamp
    backup.mkdir(parents=True, exist_ok=False)
    state: dict[str, Any] = {
        "version": 2,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "paths": {key: str(value) for key, value in paths.items()},
        "existed": {},
        "created_vault_files": [],
    }

    backup_targets = {
        "config": (codex / "config.toml", backup / "config.toml"),
        "agents": (global_agents, backup / global_agents.name),
        "hooks": (user_hooks, backup / "hooks.json"),
        "hook_runtime": (hook_runtime, backup / "hook-runtime"),
        "runtime": (codex / f"{PLUGIN_NAME}.json", backup / f"{PLUGIN_NAME}.json"),
        "marketplace": (marketplace, backup / "marketplace.json"),
        "plugin": (plugin_destination, backup / "plugin"),
        "five_role_skill": (deliberation_skill, backup / "five-role-skill"),
        "design_skill": (design_skill, backup / "design-skill"),
        "auto_memory_skill": (auto_memory_skill, backup / "auto-memory-skill"),
        "product_manager_skill": (product_manager_skill, backup / "product-manager-skill"),
    }
    for role in sorted((plugin_root / "agents").glob("*.toml")):
        backup_targets[f"role:{role.name}"] = (
            role_destination / role.name,
            backup / "agents" / role.name,
        )
    for name, (source, destination) in backup_targets.items():
        state["existed"][name] = backup_file(source, destination)

    try:
        codex.mkdir(parents=True, exist_ok=True)
        merge_codex_config(codex / "config.toml")
        merge_agents(
            global_agents,
            plugin_root / "assets" / "templates" / "global-agents-block.md",
            vault,
        )
        vault.mkdir(parents=True, exist_ok=True)
        state["created_vault_files"] = copy_missing_tree(
            plugin_root / "assets" / "knowledge-base", vault
        )
        write_runtime(codex / f"{PLUGIN_NAME}.json", vault)
        install_role_assets(plugin_root, codex, home)
        hook_runtime.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            plugin_root / "scripts" / "memory_hook.py",
            hook_runtime / "memory_hook.py",
        )
        merge_user_hooks(user_hooks, hook_runtime / "memory_hook.py")
        if not args.skip_plugin_copy:
            install_plugin(plugin_root, plugin_destination)
            merge_marketplace(marketplace)
        atomic_write(
            backup / "state.json",
            json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        )
    except Exception:
        atomic_write(
            backup / "state.json",
            json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        )
        print(f"Installation failed. Backup retained at: {backup}", file=sys.stderr)
        raise

    result = {
        "status": "installed",
        "plugin": PLUGIN_NAME,
        "version": PLUGIN_VERSION,
        "vault": str(vault),
        "backup": str(backup),
        "next": [
            "Run: python3 scripts/verify.py",
            "Restart Codex.",
            "Review and trust the user-level hooks when prompted.",
            "Start a new chat; normal conversation automatically routes direct execution or five-role deliberation.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
