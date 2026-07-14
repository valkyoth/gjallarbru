#!/usr/bin/env sh
set -eu

cargo fmt --all --check
scripts/check_shell_syntax.sh
python3 scripts/test-tooling-policy.py
python3 scripts/test-foundation-dependency-surface.py
scripts/check_doc_links.sh
scripts/validate-modularity-policy.sh
scripts/validate-security-policy.sh
scripts/validate-release-metadata.sh
python3 scripts/validate-release-plan.py
scripts/test-release-readiness.sh
python3 scripts/test-release-crates.py
python3 scripts/release_crates.py --check
scripts/check-packages.sh
python3 scripts/test-sbom-compare.py
scripts/generate-sbom.sh --check
scripts/verify-rfcs.sh
python3 scripts/test-rfc-sources.py
cargo check --workspace --all-features --locked
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
cargo test --workspace --all-features --locked
