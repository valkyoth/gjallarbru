#!/usr/bin/env python3
"""Ensure every indexed Gjallarbru version has a complete release contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "docs" / "VERSION_PLAN.md"
PLAN = ROOT / "docs" / "RELEASE_PLAN.md"

INDEX_VERSION = re.compile(r"^\| `(\d+\.\d+\.\d+)` \|", re.MULTILINE)
PLAN_VERSION = re.compile(r"^### v(\d+\.\d+\.\d+) - .+$", re.MULTILINE)
REQUIRED_SECTIONS = ("Goal:", "Deliverables:", "Verification:", "Exit criteria:")


def fail(message: str) -> None:
    print(f"release plan validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def duplicates(values: list[str]) -> list[str]:
    return sorted({value for value in values if values.count(value) > 1})


def main() -> None:
    index_text = INDEX.read_text(encoding="utf-8")
    plan_text = PLAN.read_text(encoding="utf-8")
    indexed = INDEX_VERSION.findall(index_text)
    headings = list(PLAN_VERSION.finditer(plan_text))
    detailed = [heading.group(1) for heading in headings]

    if not indexed:
        fail("VERSION_PLAN.md contains no indexed versions")
    if duplicate_versions := duplicates(indexed):
        fail(f"duplicate indexed versions: {', '.join(duplicate_versions)}")
    if duplicate_versions := duplicates(detailed):
        fail(f"duplicate detailed versions: {', '.join(duplicate_versions)}")
    if indexed != detailed:
        missing = [version for version in indexed if version not in detailed]
        extra = [version for version in detailed if version not in indexed]
        fail(
            "version order or coverage differs"
            f"; missing={missing or 'none'}; extra={extra or 'none'}"
        )

    for position, heading in enumerate(headings):
        version = heading.group(1)
        end = headings[position + 1].start() if position + 1 < len(headings) else len(plan_text)
        contract = plan_text[heading.end() : end]

        cursor = -1
        section_positions: list[int] = []
        for section in REQUIRED_SECTIONS:
            found = contract.find(f"\n{section}")
            if found < 0:
                fail(f"v{version} is missing {section}")
            if found <= cursor:
                fail(f"v{version} has sections out of order at {section}")
            cursor = found
            section_positions.append(found)

        for section_position, section in enumerate(REQUIRED_SECTIONS):
            body_start = section_positions[section_position] + len(section) + 1
            body_end = (
                section_positions[section_position + 1]
                if section_position + 1 < len(section_positions)
                else len(contract)
            )
            body = contract[body_start:body_end].strip()
            bullets = [line for line in body.splitlines() if line.startswith("- ")]
            if not body:
                fail(f"v{version} has an empty {section}")
            if section in ("Deliverables:", "Verification:") and not bullets:
                fail(f"v{version} {section} must contain a concrete list")
            if section == "Exit criteria:" and len(bullets) < 2:
                fail(f"v{version} needs an exit condition plus its pentest stop")

        stop = (
            f"Stop: `v{version} implementation stop reached. "
            "Run pentest for this exact commit.`"
        )
        if contract.count(stop) != 1:
            fail(f"v{version} must contain its exact pentest stop once")

    print(f"release plan validation passed: {len(indexed)} complete version contracts")


if __name__ == "__main__":
    main()
