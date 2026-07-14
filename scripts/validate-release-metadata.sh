#!/usr/bin/env sh
set -eu

test -s CHANGELOG.md
test -s release-notes/RELEASE_NOTES_0.2.0.md
test -s docs/IMPLEMENTATION_PLAN.md
test -s docs/VERSION_PLAN.md
test -s docs/RELEASE_PLAN.md
test -s docs/CRATE_VERSION_MATRIX.md
test -s release-crates.toml
test -s sbom/gjallarbru.spdx.json
test -s requirements/SCHEMA.json
test -s requirements/BASE_REQUIREMENTS.json
test -s requirements/ERRATA.json
test ! -e PENTEST.md

grep -Fq 'version = "0.2.0"' Cargo.toml
grep -Fq 'first serious production-ready STUN/TURN server application' \
    docs/VERSION_PLAN.md

cargo metadata --locked --format-version 1 --no-deps >/dev/null
