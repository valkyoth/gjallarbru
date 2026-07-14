#!/usr/bin/env python3
"""Validate or live-check Gjallarbru's RFC 8489/8656 errata decisions."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "requirements/ERRATA.json"
RFCS = (8489, 8656)
STATUSES = ("Verified", "Reported", "Held for Document Update", "Rejected")
DISPOSITIONS = ("apply", "track-not-applied", "not-applicable")
ENDPOINT = "https://errata.rfc-editor.org/search/"


class ErrataError(RuntimeError):
    """A malformed or drifting RFC errata decision set."""


class ErrataTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.heading = False
        self.heading_text: list[str] = []
        self.status: str | None = None
        self.in_row = False
        self.in_cell = False
        self.cell_text: list[str] = []
        self.cells: list[str] = []
        self.records: list[dict] = []

    def handle_starttag(self, tag: str, _attrs) -> None:
        if tag == "h2":
            self.heading = True
            self.heading_text = []
        elif tag == "tr":
            self.in_row = True
            self.cells = []
        elif tag == "td" and self.in_row:
            self.in_cell = True
            self.cell_text = []

    def handle_data(self, data: str) -> None:
        if self.heading:
            self.heading_text.append(data)
        if self.in_cell:
            self.cell_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self.heading:
            heading = "".join(self.heading_text).strip()
            self.status = next(
                (status for status in STATUSES if heading.startswith(status)), None
            )
            self.heading = False
        elif tag == "td" and self.in_cell:
            self.cells.append(" ".join("".join(self.cell_text).split()))
            self.in_cell = False
        elif tag == "tr" and self.in_row:
            self.in_row = False
            if self.cells and self.status is not None:
                self._record_row()

    def _record_row(self) -> None:
        match = re.fullmatch(r"RFC([0-9]+) \(([0-9]+)\)", self.cells[0])
        if match is None or len(self.cells) != 7:
            raise ErrataError(f"unrecognized errata table row: {self.cells}")
        identifier = int(match.group(2))
        self.records.append(
            {
                "rfc": int(match.group(1)),
                "id": identifier,
                "source": f"https://errata.rfc-editor.org/eid{identifier}/",
                "status": self.status,
                "section": self.cells[1],
                "type": self.cells[2],
                "reported": self.cells[6],
            }
        )


def fetch_rfc(number: int) -> list[dict]:
    query = urllib.parse.urlencode(
        {"rfc_number": number, "status": "any", "presentation": "table"}
    )
    request = urllib.request.Request(
        f"{ENDPOINT}?{query}",
        headers={"User-Agent": "gjallarbru-requirements/0.2.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8")
    except OSError as error:
        raise ErrataError(f"cannot fetch RFC {number} errata: {error}") from error
    parser = ErrataTableParser()
    parser.feed(html)
    if any(record["rfc"] != number for record in parser.records):
        raise ErrataError(f"RFC {number} response contained another RFC")
    return sorted(parser.records, key=lambda record: record["id"])


def official_fields(record: dict) -> dict:
    keys = ("rfc", "id", "source", "status", "section", "type", "reported")
    return {key: record[key] for key in keys}


def load() -> dict:
    try:
        snapshot = json.loads(OUTPUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ErrataError(f"cannot load {OUTPUT.name}: {error}") from error
    validate(snapshot)
    return snapshot


def validate(snapshot: dict) -> None:
    if snapshot.get("schema") != 1 or snapshot.get("source") != ENDPOINT:
        raise ErrataError("errata schema or source is invalid")
    if set(snapshot) != {"schema", "checked_at", "source", "errata"}:
        raise ErrataError("errata top-level fields are invalid")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", snapshot.get("checked_at", "")):
        raise ErrataError("errata checked_at date is invalid")
    records = snapshot.get("errata")
    if not isinstance(records, list):
        raise ErrataError("errata decision list is missing")
    seen: set[int] = set()
    covered = {number: 0 for number in RFCS}
    record_fields = {
        "rfc", "id", "source", "status", "section", "type", "reported",
        "disposition", "implementation", "security",
    }
    previous_key = (0, 0)
    for record in records:
        if set(record) != record_fields:
            raise ErrataError("errata record fields are invalid")
        identifier = record.get("id")
        rfc = record.get("rfc")
        if not isinstance(identifier, int) or identifier in seen:
            raise ErrataError(f"duplicate or invalid errata ID: {identifier}")
        if rfc not in RFCS or record.get("status") not in STATUSES:
            raise ErrataError(f"invalid RFC or status for erratum {identifier}")
        seen.add(identifier)
        key = (rfc, identifier)
        if key <= previous_key:
            raise ErrataError("errata records are not in stable RFC/ID order")
        previous_key = key
        covered[rfc] += 1
        if record.get("source") != f"https://errata.rfc-editor.org/eid{identifier}/":
            raise ErrataError(f"invalid source for erratum {identifier}")
        if record.get("type") not in ("Technical", "Editorial"):
            raise ErrataError(f"invalid type for erratum {identifier}")
        if not isinstance(record.get("section"), str) or not record["section"].strip():
            raise ErrataError(f"missing section for erratum {identifier}")
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", record.get("reported", "")):
            raise ErrataError(f"invalid reported date for erratum {identifier}")
        disposition = record.get("disposition")
        implementation = record.get("implementation")
        security = record.get("security")
        if disposition not in DISPOSITIONS:
            raise ErrataError(f"invalid disposition for erratum {identifier}")
        if not isinstance(implementation, str) or not implementation.strip():
            raise ErrataError(f"missing implementation decision for erratum {identifier}")
        if not isinstance(security, str) or not security.strip():
            raise ErrataError(f"missing security decision for erratum {identifier}")
        if record["status"] == "Verified" and disposition == "track-not-applied":
            raise ErrataError(f"verified erratum {identifier} is not applied")
        if record["status"] != "Verified" and disposition == "apply":
            raise ErrataError(f"unverified erratum {identifier} is applied")
        planned = re.fullmatch(r"planned:v([0-9]+\.[0-9]+\.[0-9]+)", implementation)
        not_applicable = implementation.startswith("not-applicable:")
        if planned is None and not not_applicable:
            raise ErrataError(f"unassigned implementation for erratum {identifier}")
        if planned is not None:
            plan = (ROOT / "docs/VERSION_PLAN.md").read_text(encoding="utf-8")
            if f"| `{planned.group(1)}` |" not in plan:
                raise ErrataError(f"unknown milestone for erratum {identifier}")
    if set(covered) != set(RFCS) or any(count == 0 for count in covered.values()):
        raise ErrataError("each base RFC needs an explicit errata decision set")


def live_check(snapshot: dict) -> None:
    local = sorted(
        (official_fields(record) for record in snapshot["errata"]),
        key=lambda record: (record["rfc"], record["id"]),
    )
    current = []
    for rfc in RFCS:
        current.extend(fetch_rfc(rfc))
    current.sort(key=lambda record: (record["rfc"], record["id"]))
    if local != current:
        raise ErrataError("official errata differ from the reviewed decision set")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Compare with RFC Editor")
    args = parser.parse_args()
    try:
        snapshot = load()
        if args.live:
            live_check(snapshot)
            print("official RFC 8489/8656 errata match reviewed decisions")
        else:
            print(f"RFC errata decisions are valid ({len(snapshot['errata'])} records)")
    except ErrataError as error:
        print(f"RFC errata invalid: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
