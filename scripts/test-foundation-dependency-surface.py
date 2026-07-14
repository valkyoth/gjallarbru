#!/usr/bin/env python3
"""Lock the v0.1.0 zero-third-party dependency baseline until reviewed change."""

from __future__ import annotations

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "gjallarbru-core",
    "gjallarbru-crypto",
    "gjallarbru-runtime",
    "gjallarbru-server",
    "gjallarbru-wire",
}


def main() -> None:
    lock = tomllib.loads((ROOT / "Cargo.lock").read_text(encoding="utf-8"))
    packages = lock.get("package", [])
    names = {package["name"] for package in packages}
    assert len(packages) == len(EXPECTED), "Cargo.lock gained a dependency without review"
    assert names == EXPECTED, f"unexpected Cargo.lock packages: {sorted(names - EXPECTED)}"
    for package in packages:
        assert "source" not in package and "checksum" not in package
        for dependency in package.get("dependencies", []):
            dependency_name = dependency.split(" ", 1)[0]
            assert dependency_name in EXPECTED
    print("foundation dependency surface tests passed (zero third-party crates)")


if __name__ == "__main__":
    main()
