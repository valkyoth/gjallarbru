# Changelog

All notable changes to `gjallarbru` are documented here.

## Unreleased

- Planned the `v0.55.1` no_std `gjallarbru` facade crate with stable `wire`,
  `crypto`, and `core` namespaces and facade-last crates.io publication.
- Added shared project branding and image navigation to each reusable support
  crate README while retaining crate-specific scope and trust-boundary docs.

## 0.1.0 - 2026-07-14

- Initialized the five-crate Rust workspace.
- Pinned Rust stable `1.97.0` with an MSRV of `1.90.0`.
- Added the security, modularity, platform, licensing, RFC-source,
  implementation, version, and release policy baseline.
- Added checksum-locked tooling and local copies for 23 RFC references.
- Added 130 complete version contracts through the production `1.0.0` release,
  including exact-commit pentest stops for every version.
- Added a tested pentest/retest → PASS report → final CodeQL → tag workflow
  that permits documented CodeQL remediation without a report-only commit rule.
- Added independent reusable-crate version and publication tooling while
  keeping the runtime, cluster, and server application private.
- Planned secure clustering, Pawalyze credentials, Fluxheim interoperability,
  and qualified Wolfi and Debian rootless containers before `1.0.0`.
- Hardened the foundation release after pentest with locked Cargo resolution,
  clean package-list checks, interpreter-aware shell validation, and a planned
  supervised-process panic-containment milestone.
- Added GitHub CI and repository governance files based on the established
  Valkyoth project pattern.
