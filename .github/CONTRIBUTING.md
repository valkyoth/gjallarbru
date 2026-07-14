# Contributing to Gjallarbru

`gjallarbru` is security-sensitive STUN/TURN infrastructure. Contributions
must keep protocol authority portable, bounded, auditable, and honest about
which RFC profiles are verified.

## License

Contributions are licensed according to the files they modify:

- reusable crates under `crates/gjallarbru-{wire,crypto,core}` use
  `MIT OR Apache-2.0`;
- runtime/server application code uses `EUPL-1.2`;
- RFC text retains its original IETF notices and must not be edited.

See [`docs/licensing.md`](../docs/licensing.md).

## Development Setup

Use the pinned Rust toolchain from `rust-toolchain.toml`.

```bash
cargo check --workspace --all-features --locked
cargo test --workspace --all-features --locked
scripts/checks.sh
```

Before a release, run the Rust compatibility, dependency, and security tools
described in `SECURITY.md`.

## Security-Sensitive Changes

Treat these areas as high risk:

- wire decoding, encoding, integrity byte ranges, and resource limits;
- authentication ordering, credentials, nonces, tokens, and key rotation;
- allocations, permissions, channels, transactions, timers, and relay ports;
- destination policy, SSRF, relay loops, quotas, and rate limits;
- runtime buffers, sockets, TLS/DTLS, platform FFI, and acceleration;
- administration, process sandboxing, CI, releases, and dependencies.

Do not post exploitable details in public issues. Follow
[`SECURITY.md`](../SECURITY.md).

## Dependency Policy

When adding or updating crates:

- verify the latest crates.io release and MSRV compatibility;
- avoid git dependencies;
- disable and review default features;
- preserve `no_std` and allocation boundaries;
- do not admit another STUN/TURN codec or state implementation;
- update `Cargo.lock` and relevant tests;
- run `cargo deny --locked check` and `cargo audit`;
- document why the crate belongs in this workspace.
