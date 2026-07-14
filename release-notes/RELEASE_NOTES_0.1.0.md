# Gjallarbru 0.1.0 Release Notes

Release type: repository and security foundation

## Scope

`0.1.0` establishes the repository, trust boundaries, documentation, local
checks, GitHub configuration, licensing model, and RFC reference process.

## Security

- Reusable wire, crypto, and core crates are `no_std` and forbid unsafe code.
- There are no third-party runtime dependencies.
- A committed SPDX 2.3 SBOM is checked semantically against the Cargo graph.
- The runtime and server remain non-functional scaffolds.
- Dependency, advisory, source, modularity, and RFC-integrity policies are
  defined before network parsing begins.
- Twenty-three RFC Editor documents are locally checksum-locked.
- The complete pre-1.0 sequence contains individually testable release
  contracts with an exact-candidate pentest stop for every tag.
- Reusable crate publication uses independent versions and admission gates;
  the EUPL runtime, future cluster crate, and server remain private.

## Known Limitations

- No STUN or TURN packet is parsed or emitted.
- No listener or relay socket is opened.
- No compliance profile is claimed.
- This version must not be deployed as a server.

## Verification

```bash
scripts/checks.sh
scripts/check-rust-version-matrix.sh
cargo deny check
cargo audit
```

Tagging requires a green pentest/retest report, final green GitHub CI and
CodeQL, and the release-readiness flow in `docs/RELEASE_PLAN.md`.
