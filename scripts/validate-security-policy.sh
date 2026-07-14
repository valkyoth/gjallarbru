#!/usr/bin/env sh
set -eu

for file in \
    SECURITY.md \
    deny.toml \
    docs/security-controls.md \
    docs/supply-chain-security.md \
    docs/threat-model.md \
    docs/unsafe-policy.md \
    sbom/gjallarbru.spdx.json; do
    test -s "$file"
done

grep -Fq 'unknown-registry = "deny"' deny.toml
grep -Fq 'unknown-git = "deny"' deny.toml
grep -Fq 'rust-version = "1.90"' Cargo.toml
grep -Fq 'channel = "1.97.0"' rust-toolchain.toml

for crate in wire crypto core; do
    manifest="crates/gjallarbru-${crate}/Cargo.toml"
    grep -Fq 'license = "MIT OR Apache-2.0"' "$manifest"
done

for crate in runtime server; do
    manifest="crates/gjallarbru-${crate}/Cargo.toml"
    grep -Fq 'license = "EUPL-1.2"' "$manifest"
    grep -Fq 'publish = false' "$manifest"
done

if cargo tree --workspace --edges normal --prefix none | \
    rg -i '(^|[-_])(stun|turn|webrtc)([-_]|$)'; then
    echo "possible third-party STUN/TURN dependency requires explicit review" >&2
    exit 1
fi
