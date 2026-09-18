#!/usr/bin/env python3
"""Validate static SalesPortl skill catalog and skill documents."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
EXPECTED_SKILL_COUNT = 18
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


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    fm_block = parts[0].replace("---\n", "", 1)
    parsed: dict[str, str] = {}
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def check_secret_patterns(path: Path, text: str, errors: list[str]) -> None:
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"{path}: potential secret pattern matched: {pattern}")


def main() -> int:
    errors: list[str] = []

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

    if len(skills) != EXPECTED_SKILL_COUNT:
        errors.append(
            f"catalog.json: expected {EXPECTED_SKILL_COUNT} skills, found {len(skills)}"
        )

    seen_names = set()

    for idx, entry in enumerate(skills, start=1):
        for field in ("name", "module", "description", "tags", "version", "path"):
            if field not in entry:
                errors.append(f"catalog.json skill[{idx}]: missing field '{field}'")

        name = entry.get("name", "")
        path_value = entry.get("path", "")
        if name in seen_names:
            errors.append(f"catalog.json: duplicate skill name '{name}'")
        seen_names.add(name)

        skill_path = ROOT / path_value
        if not skill_path.exists():
            errors.append(f"missing skill file: {path_value}")
            continue

        text = skill_path.read_text(encoding="utf-8")
        check_secret_patterns(skill_path, text, errors)

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

        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"{path_value}: missing required heading '{heading}'")

    check_secret_patterns(CATALOG_PATH, CATALOG_PATH.read_text(encoding="utf-8"), errors)

    if errors:
        print("VALIDATION FAILED")
        for err in errors:
            print(f"- {err}")
        return 1

    print("VALIDATION PASSED")
    print(f"- Skills validated: {len(skills)}")
    print(f"- Catalog path: {CATALOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
