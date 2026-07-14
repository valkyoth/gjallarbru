#!/usr/bin/env python3
"""Compare SPDX JSON documents after removing generator nondeterminism."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def canonical_json(value: object) -> str:
    """Serialize a normalized JSON value for deterministic ordering."""
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def canonicalize(value: object) -> object:
    """Sort JSON containers recursively without changing scalar values."""
    if isinstance(value, dict):
        return {key: canonicalize(item) for key, item in sorted(value.items())}
    if isinstance(value, list):
        items = [canonicalize(item) for item in value]
        return sorted(items, key=canonical_json)
    return value


def normalized_document(path: Path) -> object:
    """Load SPDX JSON and remove cargo-sbom's per-run metadata."""
    with path.open(encoding="utf-8") as handle:
        document = json.load(handle)
    if not isinstance(document, dict):
        raise ValueError(f"{path} must contain a JSON object")
    document.pop("documentNamespace", None)
    creation_info = document.get("creationInfo")
    if isinstance(creation_info, dict):
        creation_info.pop("created", None)
    return canonicalize(document)


def documents_match(expected: Path, generated: Path) -> bool:
    """Return whether two SPDX documents carry identical stable content."""
    return normalized_document(expected) == normalized_document(generated)


def main(arguments: list[str]) -> int:
    """Compare the committed and newly generated SPDX documents."""
    if len(arguments) != 3:
        print("usage: compare_sbom.py EXPECTED GENERATED", file=sys.stderr)
        return 2
    if documents_match(Path(arguments[1]), Path(arguments[2])):
        print("committed SBOM matches the current dependency graph")
        return 0
    print("SBOM is stale; run scripts/generate-sbom.sh --write", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

