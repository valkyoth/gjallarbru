#!/usr/bin/env python3
"""Regression tests for Gjallarbru's locked RFC source baseline."""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RFC = ROOT / "rfc"
SOURCE_PATTERN = re.compile(
    r"^(\d+) https://www\.rfc-editor\.org/rfc/rfc(\d+)\.txt ([a-z0-9-]+)$"
)
CHECKSUM_PATTERN = re.compile(r"^([0-9a-f]{64})  (rfc(\d+)\.txt)$")
REQUIRED = {
    2119,
    5769,
    5780,
    5928,
    6062,
    6679,
    7064,
    7065,
    7350,
    7376,
    7443,
    7635,
    7982,
    7983,
    8016,
    8155,
    8174,
    8265,
    8489,
    8656,
    9147,
    9325,
    9443,
}


def parse_sources() -> dict[int, str]:
    sources: dict[int, str] = {}
    for line in (RFC / "SOURCES").read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        match = SOURCE_PATTERN.fullmatch(line)
        assert match is not None, f"invalid source line: {line!r}"
        number, repeated, role = match.groups()
        assert number == repeated
        key = int(number)
        assert key not in sources
        sources[key] = role
    return sources


def parse_checksums() -> dict[int, str]:
    checksums: dict[int, str] = {}
    for line in (RFC / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        match = CHECKSUM_PATTERN.fullmatch(line)
        assert match is not None, f"invalid checksum line: {line!r}"
        digest, filename, number = match.groups()
        path = RFC / filename
        assert path.is_file() and path.stat().st_size > 0
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        key = int(number)
        assert key not in checksums
        checksums[key] = digest
    return checksums


def main() -> None:
    sources = parse_sources()
    checksums = parse_checksums()
    assert set(sources) == REQUIRED
    assert set(checksums) == REQUIRED
    subprocess.run(["scripts/verify-rfcs.sh"], cwd=ROOT, check=True)
    print(f"RFC source baseline tests passed ({len(REQUIRED)} documents)")


if __name__ == "__main__":
    main()
