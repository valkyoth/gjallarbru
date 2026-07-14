<p align="center">
  <b>A no_std-first, security-focused STUN and TURN implementation for Rust.</b><br>
  RFC-traceable protocol processing, bounded state, and portable relay runtimes.
</p>

<div align="center">
  <a href="https://github.com/valkyoth/gjallarbru/blob/main/docs/VERSION_PLAN.md">Version Plan</a>
  |
  <a href="https://github.com/valkyoth/gjallarbru/blob/main/docs/IMPLEMENTATION_PLAN.md">Implementation Plan</a>
  |
  <a href="https://github.com/valkyoth/gjallarbru/blob/main/docs/threat-model.md">Threat Model</a>
  |
  <a href="https://github.com/valkyoth/gjallarbru/blob/main/SECURITY.md">Security</a>
</div>

<br>

<p align="center">
  <a href="https://github.com/valkyoth/gjallarbru">
    <img src="https://raw.githubusercontent.com/valkyoth/gjallarbru/main/.github/images/gjallarbru.webp" alt="Gjallarbru STUN and TURN server overview">
  </a>
</p>

# Gjallarbru

`gjallarbru` is a Rust workspace for a modern STUN/TURN server and reusable
protocol engine. Its design center is a portable `no_std` protocol authority:
the wire implementation and state machine decide what is valid and authorized,
while replaceable runtimes perform sockets, TLS/DTLS, credential lookup,
logging, administration, and platform acceleration.

The project implements STUN/TURN decoding, encoding, validation, and server
state itself. It may use separately reviewed crates for cryptographic
primitives, TLS/DTLS, Unicode/PRECIS, system calls, and operational adapters.

## Current Status

Status: RFC requirement-ledger release candidate for `v0.2.0`.

Implemented now:

- A five-crate workspace with explicit trust and license boundaries.
- `no_std`, unsafe-free scaffolds for `gjallarbru-wire`,
  `gjallarbru-crypto`, and `gjallarbru-core`.
- Internal EUPL-1.2 runtime and server crates.
- Rust `1.90.0` MSRV with stable `1.97.0` pinned for development.
- Security, modularity, toolchain, platform, RFC-source, implementation,
  version, and release policies.
- A checksum-bound machine-readable inventory of all 184 numbered RFC 8489 and
  RFC 8656 sections and 393 uppercase normative keyword occurrences, each with
  an owning profile, component, milestone, test assignment, status, and
  security note.
- Reviewed dispositions for all six current RFC 8489/8656 errata, with live
  drift checking separated from reproducible offline validation.
- Local checks for formatting, linting, tests, Rust-version compatibility,
  file-size policy, documentation links, a committed SBOM, and locked RFC
  reference copies.
- GitHub CI, Dependabot, CODEOWNERS, funding, contribution, issue, and release
  metadata configuration.

Not implemented yet:

- No STUN decoder, encoder, Binding service, or authentication.
- No TURN allocation, permission, channel, relay, or transaction state.
- No sockets, TLS, DTLS, credential provider, or administrative endpoint.
- No production server behavior. Running the binary prints a foundation
  notice and exits.
- The requirement ledger is traceability evidence, not a protocol-conformance
  claim; every planned rule still requires implementation and test evidence.

The complete sequence to production readiness is in
[`docs/VERSION_PLAN.md`](docs/VERSION_PLAN.md). Nothing required for the
supported STUN/TURN profiles is postponed beyond `1.0.0`.

## Trust Dashboard

| Area | Foundation policy |
| --- | --- |
| Reusable crate license | `MIT OR Apache-2.0` |
| Runtime and binary license | `EUPL-1.2` |
| MSRV | Rust `1.90.0` |
| Pinned toolchain | Rust `1.97.0` |
| Protocol authority | `no_std`, Sans-I/O, bounded |
| Default external dependencies | None |
| Unsafe policy | Forbidden in the future facade, wire, crypto, and core; isolated and reviewed in future runtime modules |
| Packet-path allocation target | None after startup |
| Specification source | Checksum-locked RFC Editor text plus reviewed errata |
| Code size | Non-generated Rust files must stay below 500 lines |
| CodeQL | GitHub default setup; no advanced CodeQL workflow |
| 1.0 target | First serious production-ready STUN/TURN server application |

## Workspace

| Crate | License | `no_std` | Publication intent | Responsibility |
| --- | --- | --- | --- | --- |
| `gjallarbru-wire` | MIT/Apache-2.0 | yes | crates.io after API stability | STUN/TURN wire format and framing |
| `gjallarbru-crypto` | MIT/Apache-2.0 | yes | possible after provider stability | Integrity, credential, nonce, and token boundaries |
| `gjallarbru-core` | MIT/Apache-2.0 | yes | crates.io after API stability | Deterministic Sans-I/O protocol state |
| `gjallarbru-runtime` | EUPL-1.2 | no | internal | Portable and accelerated OS adapters |
| `gjallarbru-server` | EUPL-1.2 | no | GitHub/OS artifacts | Configuration and deployable server binary |

At `v0.55.1`, a thin MIT/Apache-2.0 `no_std` facade crate named `gjallarbru`
will become the recommended library entry point. It will expose
`gjallarbru::wire`, `gjallarbru::crypto`, and `gjallarbru::core` without
depending on the EUPL runtime or server. Its package and crate documentation
must remain identical to this repository README through an automated parity or
single-source check.

The dependency direction is inward only:

```text
gjallarbru facade -> {wire, crypto, core}
server -> runtime -> core -> {wire, crypto}
```

Core crates never depend on the runtime, an operating system, an async
executor, TLS/DTLS, a database, or another STUN/TURN implementation.

## Rust Version Support

The minimum supported Rust version is Rust `1.90.0`. New development and
release work uses pinned stable Rust `1.97.0`.

| Rust | Required evidence |
| --- | --- |
| `1.90.0` | `cargo check --workspace --all-targets --all-features --locked` |
| `1.91.0` | `cargo check --workspace --all-targets --all-features --locked` |
| `1.92.0` | `cargo check --workspace --all-targets --all-features --locked` |
| `1.93.0` | `cargo check --workspace --all-targets --all-features --locked` |
| `1.94.0` | `cargo check --workspace --all-targets --all-features --locked` |
| `1.95.0` | `cargo check --workspace --all-targets --all-features --locked` |
| `1.96.0` | `cargo check --workspace --all-targets --all-features --locked` |
| `1.96.1` | `cargo check --workspace --all-targets --all-features --locked` |
| `1.97.0` | Full local check and release gate |

Run the complete compatibility matrix with:

```bash
scripts/check-rust-version-matrix.sh
```

## Standards Baseline

The planned profiles are based on RFC 8489 (STUN), RFC 8656 (TURN), RFC 7350
(DTLS transport), RFC 6062 (TCP relaying), RFC 7635 (third-party
authorization), RFC 8016 (mobility), RFC 5780 (behavior discovery), and the
standardized shared-port demultiplexing rules. RFC 5769 supplies official STUN
test vectors.

Exact RFC Editor text is held under [`rfc/`](rfc/README.md), outside the
project software licenses, and checksum-verified by the normal test gate.
The [`requirements` ledger](requirements/README.md) maps every RFC 8489/8656
section and extracted normative keyword to its planned implementation and test
milestone, with separately reviewed errata decisions.

## Platform Direction

The portable architecture supports Linux, Windows, BSD, macOS, Android, and
iOS without allowing one platform backend to define protocol behavior. Linux
may later add `recvmmsg`, `sendmmsg`, `io_uring`, eBPF, or AF_XDP acceleration;
correctness must remain identical without them. The fixed-capacity `no_std`
path is designed so Aesynx can implement the same core interfaces when its
network and runtime APIs are ready.

See [`docs/platform-support.md`](docs/platform-support.md) for the evidence
levels required before a platform is advertised as production supported.

## Development

```bash
scripts/validate-requirements.sh
scripts/checks.sh
scripts/check-rust-version-matrix.sh
cargo deny --locked check
cargo audit
```

Networked freshness and reference updates are deliberately separate from
offline builds:

```bash
scripts/check_latest_tools.sh
scripts/fetch-rfcs.sh
scripts/rfc_errata.py --live
```

## Distribution

GitHub is the canonical project and the server's primary distribution channel.
Production releases will provide signed binaries, checksums, SBOMs,
provenance, service definitions, and later OS packages. Reusable `no_std`
support crates will be published to crates.io only after their APIs and
independent release gates are stable. They use independent versions so an
unchanged support crate is never republished merely because the application
advances. The future `gjallarbru` facade follows project milestone versions and
publishes last only when its package or dependency contract changes.
See [`docs/CRATE_VERSION_MATRIX.md`](docs/CRATE_VERSION_MATRIX.md) for the
consumer value, version rules, and current publication state.

The production distribution plan includes signed multi-architecture Wolfi and
Debian stable-slim OCI images. Both default to a fixed non-root user and use the
same qualified rootless Docker/Podman network contract and black-box STUN/TURN
relay suite. Wolfi is the minimal hardened default at `v0.100.0`; Debian at
`v0.100.1` retains a documented package/customization path for operators who
want more control. Network/source qualification remains `v0.99.0`, not an
unverified packaging side effect.

A dedicated `v0.97.1` compatibility profile tests TURN/TCP and TURN/TLS/443
through Fluxheim's raw stream load balancer with trusted PROXY v2. UDP and relay
ranges use a documented direct path until Fluxheim has a production generic UDP
mode that proves five-tuple affinity and real-source preservation.

## Security

Gjallarbru processes unauthenticated Internet traffic and is security-sensitive
from its first protocol line. Do not report exploitable issues in a public
issue. Follow [`SECURITY.md`](SECURITY.md).

## License

The deployable server and internal runtime are licensed under EUPL-1.2. Crates
intended for crates.io publication are dual-licensed under MIT OR Apache-2.0.
See [`docs/licensing.md`](docs/licensing.md) for the exact directory boundary.
RFC reference texts retain their own IETF notices and are not relicensed.
