#!/usr/bin/env python3
"""Validate static SalesPortl skill catalog and skill documents."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
REQUIRED_FRONTMATTER = ["name", "description", "version", "tags"]
REQUIRED_HEADINGS = [
    "## Purpose",
    "## Use when",
    "## Required inputs",
    "## Safety/authority",
    "## Workflow",
    "## Output format",
    "## Quality checks",
    "## Related skills",
]
SECRET_PATTERNS = [
    r"(?i)api[_-]?key\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}",
    r"\bghp_[A-Za-z0-9]{20,}\b",
    r"\bsk_(live|test)_[A-Za-z0-9]{16,}\b",
    r"-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----",
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_inline_list(value: str) -> list[str] | None:
    stripped = value.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        return None
    inner = stripped[1:-1].strip()
    if not inner:
        return []
    return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]


def parse_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    fm_block = parts[0].replace("---\n", "", 1)
    parsed: dict[str, object] = {}
    current_key = ""
    for line in fm_block.splitlines():
        if line.startswith("  - ") and current_key:
            current_value = parsed.get(current_key, [])
            if isinstance(current_value, list):
                current_value.append(line.replace("  - ", "", 1).strip())
                parsed[current_key] = current_value
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        if value == "":
            parsed[key] = []
        elif key == "tags":
            parsed[key] = parse_inline_list(value) or value
        else:
            parsed[key] = value
    return parsed


def check_secret_patterns(path: Path, text: str, secret_file_hits: set[str]) -> None:
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            secret_file_hits.add(str(path))
            return


def scan_repo_for_secrets(secret_file_hits: set[str]) -> None:
    exclude_dirs = {".git", "__pycache__"}
    exclude_files = {".pyc"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in exclude_dirs for part in path.parts):
            continue
        if path.suffix in exclude_files:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        check_secret_patterns(path, text, secret_file_hits)


def main() -> int:
    errors: list[str] = []
    secret_file_hits: set[str] = set()

    if not CATALOG_PATH.exists():
        print("ERROR: catalog.json not found")
        return 1

    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: catalog.json invalid JSON: {exc}")
        return 1

    skills = catalog.get("skills")
    if not isinstance(skills, list):
        errors.append("catalog.json: skills must be a list")
        skills = []

    total_skills = catalog.get("total_skills")
    if total_skills != len(skills):
        errors.append(
            f"catalog.json: total_skills ({total_skills}) must equal skills length ({len(skills)})"
        )

    seen_names = set()

    for idx, entry in enumerate(skills, start=1):
        missing_required_fields = False
        for field in ("name", "module", "description", "tags", "version", "path"):
            if field not in entry:
                errors.append(f"catalog.json skill[{idx}]: missing field '{field}'")
                missing_required_fields = True
        if missing_required_fields:
            continue

        name = entry.get("name", "")
        path_value = entry.get("path", "")
        if name in seen_names:
            errors.append(f"catalog.json: duplicate skill name '{name}'")
        seen_names.add(name)

        skill_path = ROOT / path_value
        if not skill_path.exists():
            errors.append(f"missing skill file: {path_value}")
            continue

        try:
            text = skill_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{path_value}: skill file is not valid UTF-8 text")
            continue

        frontmatter = parse_frontmatter(text)
        if not frontmatter:
            errors.append(f"{path_value}: missing or invalid frontmatter")
            continue

        for field in REQUIRED_FRONTMATTER:
            if field not in frontmatter:
                errors.append(f"{path_value}: missing frontmatter field '{field}'")

        fm_name = frontmatter.get("name", "")
        if fm_name != name:
            errors.append(
                f"{path_value}: frontmatter name '{fm_name}' does not match catalog name '{name}'"
            )

        folder_name = skill_path.parent.name
        expected_folder = slugify(name)
        if folder_name != expected_folder:
            errors.append(
                f"{path_value}: folder '{folder_name}' should match slugified name '{expected_folder}'"
            )

        module = entry.get("module", "")
        file_module = skill_path.parent.parent.name
        if module != file_module:
            errors.append(
                f"{path_value}: catalog module '{module}' does not match path module '{file_module}'"
            )

        tags = frontmatter.get("tags")
        if not isinstance(tags, list):
            errors.append(f"{path_value}: frontmatter 'tags' must be a list")

        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"{path_value}: missing required heading '{heading}'")

    scan_repo_for_secrets(secret_file_hits)
    if secret_file_hits:
        errors.append(
            f"potential secret patterns found in {len(secret_file_hits)} file(s); inspect listed paths"
        )

    if errors:
        print("VALIDATION FAILED")
        for err in errors:
            print(f"- {err}")
        if secret_file_hits:
            print("- files with potential secret patterns:")
            for path in sorted(secret_file_hits):
                print(f"  - {path}")
        return 1

    print("VALIDATION PASSED")
    print(f"- Skills validated: {len(skills)}")
    print(f"- Catalog path: {CATALOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
