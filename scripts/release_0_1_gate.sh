#!/usr/bin/env sh
set -eu

scripts/checks.sh
scripts/validate-release-readiness.sh v0.1.0
cargo deny --locked check
cargo audit
