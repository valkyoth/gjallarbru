#!/usr/bin/env python3
"""Prevent support-crate branding and planned facade documentation drift."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    "gjallarbru-wire": "allocation-free, zero-copy",
    "gjallarbru-crypto": "provider-neutral integrity",
    "gjallarbru-core": "deterministic, bounded",
}
IMAGE = (
    '<img src="https://raw.githubusercontent.com/valkyoth/gjallarbru/main/'
    '.github/images/gjallarbru.webp" '
    'alt="Gjallarbru STUN and TURN server overview">'
)
PROJECT_LINE = (
    "RFC-traceable protocol processing, bounded state, and portable relay runtimes."
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_support_readmes() -> None:
    assert (ROOT / ".github/images/gjallarbru.webp").is_file()
    for package, purpose in PACKAGES.items():
        crate = ROOT / "crates" / package
        readme = (crate / "README.md").read_text(encoding="utf-8")
        manifest = (crate / "Cargo.toml").read_text(encoding="utf-8")
        assert readme.startswith('<p align="center">\n')
        assert PROJECT_LINE in readme
        assert IMAGE in readme
        assert f'<a href="https://docs.rs/{package}">Docs.rs</a>' in readme
        assert 'href="https://crates.io/crates/gjallarbru"' in readme
        assert "docs/RELEASE_PLAN.md" in readme
        assert "docs/threat-model.md" in readme
        assert "blob/main/SECURITY.md" in readme
        assert f"# {package}" in readme
        assert "Support crate for the planned `gjallarbru` facade" in readme
        assert purpose in readme
        assert 'gjallarbru = "0.55.1"' in readme
        assert 'readme = "README.md"' in manifest


def assert_facade_plan() -> None:
    version_plan = read("docs/VERSION_PLAN.md")
    release_plan = read("docs/RELEASE_PLAN.md")
    matrix = read("docs/CRATE_VERSION_MATRIX.md")
    implementation = read("docs/IMPLEMENTATION_PLAN.md")
    root_readme = read("README.md")

    assert "| `0.55.1` | `gjallarbru` facade crate |" in version_plan
    assert "### v0.55.1 - `gjallarbru` Facade Crate" in release_plan
    assert "`wire -> crypto -> core -> gjallarbru`" in release_plan
    assert "root-README parity" in release_plan
    assert "`gjallarbru-wire`, `gjallarbru-crypto`," in matrix
    assert "`gjallarbru-core`, then `gjallarbru`" in matrix
    assert "### `gjallarbru`" in implementation
    assert "`gjallarbru::wire`, `gjallarbru::crypto`, and" in root_readme
    assert "`gjallarbru::core`" in root_readme


def main() -> None:
    assert_support_readmes()
    assert_facade_plan()
    print("crate documentation policy tests passed")


if __name__ == "__main__":
    main()
