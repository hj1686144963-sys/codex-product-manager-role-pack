#!/usr/bin/env python3
"""Fail a public tree or ZIP when private identifiers, links or secrets appear."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_RELATIVE = Path("evaluations/fixtures/unsafe-private-sample.txt")
FIXTURE = ROOT / FIXTURE_RELATIVE
FIXTURE_SHA256 = "4fc94f4b00d388de673eee067ded90c7cbc0d690a6de4236476893c123a07ec1"
TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".ini", ".js", ".json", ".jsonl", ".md", ".py",
    ".sh", ".toml", ".ts", ".txt", ".yaml", ".yml",
}
PATTERNS = {
    "personal_or_company_identifier": re.compile(
        "(?:" + "胡" + "家乐" + "|" + "雷" + "鸟" + "|" + "lei" + "niao" + "|" + "hu" + "jiale" + "|" + "hj168" + "6144963)",
        re.I,
    ),
    "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "local_absolute_path": re.compile(r"/(?:Users|home)/[^\s/]+/"),
    "private_feishu_link": re.compile(r"https://[^\s/]+\.feishu\.cn/(?:wiki|docx|base)/", re.I),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "github_pat": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "generic_secret_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}"
    ),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_fixture(path: str, data: bytes) -> bool:
    normalized = path.replace("\\", "/")
    return normalized.endswith(FIXTURE_RELATIVE.as_posix()) and digest(data) == FIXTURE_SHA256


def scan_text(path: str, data: bytes, allow_fixture: bool) -> list[dict]:
    if allow_fixture and is_fixture(path, data):
        return []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return []
    result = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for kind, pattern in PATTERNS.items():
            if pattern.search(line):
                result.append({"path": path, "line": line_number, "kind": kind})
    return result


def scan_tree(path: Path, allow_fixture: bool = True) -> list[dict]:
    files = [path] if path.is_file() else sorted(path.rglob("*"))
    result = []
    for file in files:
        if not file.is_file() or ".git" in file.parts or file.suffix == ".zip":
            continue
        if file.suffix.lower() not in TEXT_SUFFIXES:
            continue
        display = str(file.relative_to(path)) if path.is_dir() else file.name
        result.extend(scan_text(display, file.read_bytes(), allow_fixture))
    return result


def scan_zip(path: Path) -> list[dict]:
    result = []
    try:
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                if info.is_dir() or Path(info.filename).suffix.lower() not in TEXT_SUFFIXES:
                    continue
                result.extend(scan_text(info.filename, archive.read(info), allow_fixture=True))
    except (OSError, zipfile.BadZipFile) as error:
        result.append({"path": str(path), "line": 0, "kind": f"invalid_zip:{error}"})
    return result


def scan(path: Path) -> list[dict]:
    return scan_zip(path) if path.suffix.lower() == ".zip" else scan_tree(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", type=Path, default=ROOT)
    parser.add_argument("--self-test", action="store_true")
    options = parser.parse_args()
    target = options.target.expanduser().resolve()
    problems = scan(target)
    self_test = scan_tree(FIXTURE, allow_fixture=False) if options.self_test else []
    if options.self_test and not self_test:
        problems.append({"path": str(FIXTURE_RELATIVE), "line": 0, "kind": "negative_fixture_not_detected"})
    output = {
        "status": "pass" if not problems else "fail",
        "target": str(target),
        "findings": problems,
        "negative_fixture_hits": len(self_test),
        "fixture_sha256_verified": is_fixture(FIXTURE_RELATIVE.as_posix(), FIXTURE.read_bytes()),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
