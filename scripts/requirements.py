#!/usr/bin/env python3
"""Generate and validate the checksum-bound RFC 8489/8656 requirement ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RFC_DIR = ROOT / "rfc"
REQUIREMENTS_DIR = ROOT / "requirements"
OUTPUT = REQUIREMENTS_DIR / "BASE_REQUIREMENTS.json"
SCHEMA = REQUIREMENTS_DIR / "SCHEMA.json"
CHECKED_AT = "2026-07-14"
RFCS = (8489, 8656)
PROFILES = {8489: "stun-base", 8656: "turn-udp-base"}
LEVELS = (
    "MUST NOT",
    "SHALL NOT",
    "SHOULD NOT",
    "NOT RECOMMENDED",
    "MUST",
    "REQUIRED",
    "SHALL",
    "SHOULD",
    "RECOMMENDED",
    "MAY",
    "OPTIONAL",
)
STATUSES = ("planned", "implemented", "verified", "excluded", "not-applicable")
COMPONENTS = (
    "architecture",
    "wire",
    "crypto",
    "core",
    "runtime",
    "server",
    "security",
    "registry",
    "conformance",
)
SECTION_PATTERN = re.compile(
    r"^(?:Appendix )?(?P<section>[A-Z](?:\.[0-9]+)*|[0-9]+(?:\.[0-9]+)*)\.  "
    r"(?P<title>\S.*)$"
)
LEVEL_PATTERN = re.compile(
    r"(?<![A-Z])(?:MUST NOT|SHALL NOT|SHOULD NOT|NOT RECOMMENDED|MUST|"
    r"REQUIRED|SHALL|SHOULD|RECOMMENDED|MAY|OPTIONAL)(?![A-Z])"
)
PLACEHOLDERS = ("unassigned", "tbd", "todo", "unknown")

SECURITY_NOTES = {
    "architecture": "Preserve protocol layering, explicit authority, and bounded behavior.",
    "wire": "Treat lengths, padding, and values as untrusted; preserve bounds and bytes.",
    "crypto": "Preserve authentication order, downgrade resistance, and secret boundaries.",
    "core": "Fail closed before granting relay authority; bound state, time, and amplification.",
    "runtime": "Preserve path identity, transport boundaries, cleanup, and backpressure.",
    "server": "Make deployment policy explicit and reject unsafe or ambiguous configuration.",
    "security": "Test abuse, leakage, downgrade, spoofing, and resource-exhaustion cases.",
    "registry": "Reject invalid values and preserve unknown extensions without inventing meaning.",
    "conformance": "Keep official inputs immutable and apply examples only to reviewed scope.",
}

RFC8489_ASSIGNMENTS = {
    "5": ("wire", "0.7.0"),
    "6.1": ("wire", "0.16.0"),
    "6": ("core", "0.33.0"),
    "7": ("wire", "0.17.0"),
    "8": ("runtime", "0.54.1"),
    "9.1": ("crypto", "0.18.0"),
    "9.2.1": ("crypto", "0.28.0"),
    "9.2": ("crypto", "0.27.0"),
    "9": ("crypto", "0.19.0"),
    "10": ("core", "0.33.1"),
    "11": ("core", "0.18.0"),
    "12": ("core", "0.24.0"),
    "13": ("architecture", "0.34.0"),
    "14.1": ("wire", "0.10.0"),
    "14.2": ("wire", "0.10.0"),
    "14.3": ("wire", "0.11.0"),
    "14.4": ("wire", "0.12.0"),
    "14.5": ("wire", "0.12.0"),
    "14.6": ("wire", "0.12.0"),
    "14.7": ("wire", "0.17.0"),
    "14.8": ("wire", "0.11.0"),
    "14.9": ("wire", "0.11.0"),
    "14.10": ("wire", "0.11.0"),
    "14.11": ("wire", "0.12.0"),
    "14.12": ("wire", "0.12.0"),
    "14.13": ("wire", "0.29.0"),
    "14.14": ("wire", "0.11.0"),
    "14.15": ("wire", "0.12.1"),
    "14.16": ("wire", "0.12.1"),
    "14": ("wire", "0.22.0"),
    "15": ("server", "0.34.0"),
    "16": ("security", "0.34.0"),
    "17": ("architecture", "0.34.0"),
    "18": ("registry", "0.3.0"),
    "19": ("conformance", "0.34.0"),
    "A": ("conformance", "0.7.0"),
    "B": ("conformance", "0.19.0"),
}

RFC8656_ASSIGNMENTS = {
    "3": ("architecture", "0.55.0"),
    "4": ("runtime", "0.54.1"),
    "5": ("core", "0.38.0"),
    "6": ("core", "0.35.0"),
    "7.1": ("core", "0.38.0"),
    "7.2": ("core", "0.38.0"),
    "7": ("core", "0.41.0"),
    "8": ("core", "0.42.0"),
    "9": ("core", "0.43.0"),
    "10": ("core", "0.43.0"),
    "11.1": ("core", "0.44.0"),
    "11.2": ("core", "0.44.0"),
    "11.3": ("core", "0.45.0"),
    "11.4": ("core", "0.45.0"),
    "11.5": ("core", "0.52.0"),
    "11.6": ("core", "0.52.0"),
    "12.1": ("core", "0.46.0"),
    "12.2": ("core", "0.46.0"),
    "12.3": ("core", "0.46.0"),
    "12": ("core", "0.47.0"),
    "13": ("core", "0.48.0"),
    "14": ("runtime", "0.40.0"),
    "15": ("runtime", "0.40.0"),
    "16": ("runtime", "0.40.0"),
    "17": ("wire", "0.12.1"),
    "18.1": ("wire", "0.14.0"),
    "18.2": ("wire", "0.13.0"),
    "18.3": ("wire", "0.14.0"),
    "18.4": ("wire", "0.14.0"),
    "18.5": ("wire", "0.13.0"),
    "18.6": ("wire", "0.13.0"),
    "18.7": ("wire", "0.50.0"),
    "18.8": ("wire", "0.13.0"),
    "18.9": ("wire", "0.51.0"),
    "18.10": ("wire", "0.50.0"),
    "18.11": ("wire", "0.49.0"),
    "18.12": ("wire", "0.49.0"),
    "18.13": ("wire", "0.52.0"),
    "18": ("wire", "0.14.0"),
    "19": ("core", "0.38.0"),
    "20": ("conformance", "0.55.0"),
    "21": ("security", "0.70.0"),
    "22": ("registry", "0.3.0"),
    "23": ("architecture", "0.55.0"),
    "24": ("conformance", "0.55.0"),
    "25": ("conformance", "0.55.0"),
}


class RequirementError(RuntimeError):
    """A malformed, incomplete, or stale requirement ledger."""


def checksum_manifest() -> dict[int, str]:
    checksums: dict[int, str] = {}
    pattern = re.compile(r"^([0-9a-f]{64})  rfc([0-9]+)\.txt$")
    for line in (RFC_DIR / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        match = pattern.fullmatch(line)
        if match is not None:
            checksums[int(match.group(2))] = match.group(1)
    return checksums


def extract_sections(lines: list[str], rfc: int) -> list[dict]:
    sections: list[dict] = []
    for line_number, line in enumerate(lines, 1):
        match = SECTION_PATTERN.match(line)
        if match is not None:
            sections.append(
                {
                    "rfc": rfc,
                    "section": match.group("section"),
                    "title": match.group("title").strip(),
                    "line": line_number,
                    "requirements": [],
                }
            )
    if not sections:
        raise RequirementError(f"RFC {rfc} has no body sections")
    return sections


def assignment(rfc: int, section: str) -> tuple[str, str]:
    mappings = RFC8489_ASSIGNMENTS if rfc == 8489 else RFC8656_ASSIGNMENTS
    matches = [key for key in mappings if section == key or section.startswith(f"{key}.")]
    if not matches:
        return ("architecture", "0.34.0" if rfc == 8489 else "0.55.0")
    return mappings[max(matches, key=len)]


def boilerplate(lines: list[str], index: int) -> bool:
    context = " ".join(lines[max(0, index - 5) : index + 6]).lower()
    return "key words" in context and "bcp 14" in context


def build_ledger() -> dict:
    checksums = checksum_manifest()
    documents = []
    all_sections: list[dict] = []
    all_requirements: list[dict] = []
    for rfc in RFCS:
        path = RFC_DIR / f"rfc{rfc}.txt"
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if checksums.get(rfc) != digest:
            raise RequirementError(f"RFC {rfc} differs from SHA256SUMS")
        lines = content.decode("utf-8-sig").split("\n")
        sections = extract_sections(lines, rfc)
        active = 0
        for index, line in enumerate(lines):
            while active + 1 < len(sections) and index + 1 >= sections[active + 1]["line"]:
                active += 1
            if index + 1 < sections[0]["line"] or boilerplate(lines, index):
                continue
            section = sections[active]["section"]
            if (rfc == 8489 and section.startswith("20")) or (
                rfc == 8656 and section.startswith("26")
            ):
                continue
            component, milestone = assignment(rfc, section)
            scan_line = line
            next_word = ""
            if index + 1 < len(lines):
                following = lines[index + 1].lstrip().split(maxsplit=1)
                next_word = following[0] if following else ""
            ending = line.rstrip().rsplit(maxsplit=1)
            ending_word = ending[-1] if ending else ""
            if (ending_word, next_word) in {
                ("MUST", "NOT"),
                ("SHALL", "NOT"),
                ("SHOULD", "NOT"),
                ("NOT", "RECOMMENDED"),
            }:
                scan_line = f"{line} {next_word}"
            continued_recommended = (
                index > 0
                and lines[index - 1].rstrip().endswith(" NOT")
                and line.lstrip().startswith("RECOMMENDED")
            )
            seen_on_line: dict[str, int] = {}
            for match in LEVEL_PATTERN.finditer(scan_line):
                level = match.group(0)
                if continued_recommended and level == "RECOMMENDED" and not line[: match.start()].strip():
                    continue
                seen_on_line[level] = seen_on_line.get(level, 0) + 1
                suffix = re.sub(r"[^A-Z]+", "-", level).strip("-")
                identifier = (
                    f"RFC{rfc}-S{section}-L{index + 1}-{suffix}-"
                    f"{seen_on_line[level]}"
                )
                requirement = {
                    "id": identifier,
                    "rfc": rfc,
                    "section": section,
                    "line": index + 1,
                    "level": level,
                    "profile": PROFILES[rfc],
                    "component": component,
                    "symbol": f"planned:v{milestone}",
                    "test": f"planned:v{milestone}",
                    "status": "planned",
                    "security": SECURITY_NOTES[component],
                    "source_sha256": hashlib.sha256(
                        " ".join(scan_line.split()).encode("utf-8")
                    ).hexdigest(),
                }
                sections[active]["requirements"].append(identifier)
                all_requirements.append(requirement)
        documents.append(
            {
                "rfc": rfc,
                "profile": PROFILES[rfc],
                "source": f"https://www.rfc-editor.org/rfc/rfc{rfc}.txt",
                "sha256": digest,
            }
        )
        all_sections.extend(sections)
    return {
        "schema": 1,
        "checked_at": CHECKED_AT,
        "documents": documents,
        "sections": all_sections,
        "requirements": all_requirements,
    }


def known_versions() -> set[str]:
    text = (ROOT / "docs/VERSION_PLAN.md").read_text(encoding="utf-8")
    return set(re.findall(r"^\| `(\d+\.\d+\.\d+)` \|", text, re.MULTILINE))


def validate(ledger: dict) -> None:
    if ledger.get("schema") != 1 or not SCHEMA.is_file():
        raise RequirementError("requirement schema is missing or invalid")
    if set(ledger) != {"schema", "checked_at", "documents", "sections", "requirements"}:
        raise RequirementError("ledger top-level fields differ from the schema")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", ledger.get("checked_at", "")):
        raise RequirementError("ledger checked_at date is invalid")
    requirements = ledger.get("requirements")
    sections = ledger.get("sections")
    documents = ledger.get("documents")
    if not all(isinstance(value, list) for value in (requirements, sections, documents)):
        raise RequirementError("ledger collections are missing")
    if tuple(document.get("rfc") for document in documents) != RFCS:
        raise RequirementError("ledger document set or order differs")
    checksums = checksum_manifest()
    document_fields = {"rfc", "profile", "source", "sha256"}
    for document in documents:
        rfc = document["rfc"]
        if set(document) != document_fields:
            raise RequirementError(f"RFC {rfc} document fields differ from the schema")
        if document["profile"] != PROFILES[rfc]:
            raise RequirementError(f"RFC {rfc} document profile is invalid")
        if document["source"] != f"https://www.rfc-editor.org/rfc/rfc{rfc}.txt":
            raise RequirementError(f"RFC {rfc} document source is invalid")
        if document["sha256"] != checksums.get(rfc):
            raise RequirementError(f"RFC {rfc} document checksum is invalid")
    identifiers: set[str] = set()
    versions = known_versions()
    required = {
        "id", "rfc", "section", "line", "level", "profile", "component",
        "symbol", "test", "status", "security", "source_sha256",
    }
    for item in requirements:
        if set(item) != required:
            raise RequirementError("requirement fields differ from the schema")
        identifier = item["id"]
        if not isinstance(identifier, str) or identifier in identifiers:
            raise RequirementError(f"duplicate or invalid requirement ID: {identifier}")
        identifiers.add(identifier)
        if (
            item["rfc"] not in RFCS
            or not isinstance(item["section"], str)
            or not isinstance(item["line"], int)
            or item["line"] < 1
            or item["level"] not in LEVELS
        ):
            raise RequirementError(f"invalid RFC or level for {identifier}")
        if item["profile"] != PROFILES[item["rfc"]]:
            raise RequirementError(f"invalid profile for {identifier}")
        if item["component"] not in COMPONENTS or item["status"] not in STATUSES:
            raise RequirementError(f"invalid component or status for {identifier}")
        for field in ("symbol", "test", "security"):
            value = item[field]
            if not isinstance(value, str) or not value.strip():
                raise RequirementError(f"{identifier} has empty {field}")
            normalized = value.strip().lower()
            if normalized in PLACEHOLDERS or any(
                normalized.startswith(f"{word}:") for word in PLACEHOLDERS
            ):
                raise RequirementError(f"{identifier} has unassigned {field}")
        if not re.fullmatch(r"[0-9a-f]{64}", item["source_sha256"]):
            raise RequirementError(f"{identifier} has invalid source hash")
        planned = re.fullmatch(r"planned:v(\d+\.\d+\.\d+)", item["symbol"])
        if item["status"] == "planned":
            if planned is None or item["test"] != item["symbol"]:
                raise RequirementError(f"{identifier} has invalid planned assignment")
            if planned.group(1) not in versions:
                raise RequirementError(f"{identifier} targets unknown milestone")
        elif item["status"] in ("implemented", "verified"):
            if item["symbol"].startswith("planned:") or item["test"].startswith("planned:"):
                raise RequirementError(f"{identifier} is complete without implementation evidence")
        elif item["status"] == "excluded":
            if not item["symbol"].startswith("decision:") or not item["test"].startswith(
                "evidence:"
            ):
                raise RequirementError(f"{identifier} is excluded without reviewed evidence")
        elif item["status"] == "not-applicable":
            if not item["symbol"].startswith("not-applicable:") or not item[
                "test"
            ].startswith("not-applicable:"):
                raise RequirementError(f"{identifier} lacks not-applicable evidence")
    section_keys: set[tuple[int, str]] = set()
    references: list[str] = []
    section_fields = {"rfc", "section", "title", "line", "requirements"}
    for section in sections:
        if set(section) != section_fields:
            raise RequirementError("section fields differ from the schema")
        key = (section.get("rfc"), section.get("section"))
        if (
            key in section_keys
            or key[0] not in RFCS
            or not key[1]
            or not isinstance(section.get("title"), str)
            or not section["title"].strip()
            or not isinstance(section.get("line"), int)
            or section["line"] < 1
        ):
            raise RequirementError(f"duplicate or invalid section: {key}")
        section_keys.add(key)
        listed = section.get("requirements")
        if not isinstance(listed, list) or any(item not in identifiers for item in listed):
            raise RequirementError(f"section {key} has invalid requirement assignments")
        if len(listed) != len(set(listed)):
            raise RequirementError(f"section {key} has duplicate requirement assignments")
        references.extend(listed)
    if set(references) != identifiers or len(references) != len(identifiers):
        raise RequirementError("requirements are missing or multiply orphaned from sections")


def render(ledger: dict) -> str:
    return json.dumps(ledger, indent=2, ensure_ascii=False) + "\n"


def check() -> None:
    expected = build_ledger()
    validate(expected)
    if not OUTPUT.is_file():
        raise RequirementError("generated requirement ledger is missing")
    actual = json.loads(OUTPUT.read_text(encoding="utf-8"))
    validate(actual)
    if render(actual) != render(expected):
        raise RequirementError("requirement ledger is stale; run with --write")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Regenerate the ledger")
    args = parser.parse_args()
    try:
        if args.write:
            ledger = build_ledger()
            validate(ledger)
            OUTPUT.write_text(render(ledger), encoding="utf-8")
            print(f"wrote {OUTPUT.relative_to(ROOT)}")
        else:
            check()
            ledger = json.loads(OUTPUT.read_text(encoding="utf-8"))
            print(
                "requirement ledger is complete: "
                f"{len(ledger['sections'])} sections, "
                f"{len(ledger['requirements'])} normative keywords"
            )
    except (OSError, UnicodeError, json.JSONDecodeError, RequirementError) as error:
        print(f"requirement ledger invalid: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
