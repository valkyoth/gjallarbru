# Changelog

All notable changes to `gjallarbru` are documented here.

## Unreleased

- Expanded the pre-1.0 plan with deterministic reducer, parser-safety,
  freestanding, cryptographic-provider, resource-accounting, model-assurance,
  buffer-ownership, batching, and fast-path revocation closure milestones.
- Added a requirement-evidence milestone that permits `verified` status only
  for semantically refined rules with resolved symbols and tests observed by CI.
- Corrected the design contract for receive-side STUN padding and legal UDP
  ChannelData alignment before wire implementation begins.
- Added explicit closures for runtime effect admission, complete client-path
  identity, encoder commit mechanics, external crypto, clock trust, transaction
  invalidation, timer debt, relay entropy/payload ownership, secure-transport
  early data, first-concurrency models, and accelerated quota leases.
- Made command-batch admission strictly atomic, moved transactional encoder
  mechanics into the initial typestate release, bounded asynchronous
  packet-crypto input, and moved clock/early-data/Loom safeguards into the
  first milestones that depend on them.
- Added explicit encoder typestates, primitive absolute-time trust/source
  domains, a linear generation-bound command-permit lifecycle, composable
  runtime effect properties, and a mandatory minimum relay-safety baseline
  before any functional Allocate/CreatePermission/Send path.
- Added exact prepared-transition permit sizing, core-only semantic operation
  IDs, a portable release/acquire publication model, pre-listener internet
  ingress budgets, canonical/effective destination handling, exact charge
  lifecycles, and plan-bound finalizer dependency slots.
- Added linear ingress-work permits with monotonic refill, reserved
  authoritative control progress, strict prepared-transition ownership and
  scrubbing, bounded non-authoritative snapshots, and generation-safe
  translation lifecycle rules backed by a checksum-locked RFC 6052 source.

## 0.2.0 - 2026-07-14

- Planned the `v0.55.1` no_std `gjallarbru` facade crate with stable `wire`,
  `crypto`, and `core` namespaces and facade-last crates.io publication.
- Added shared project branding and image navigation to each reusable support
  crate README while retaining crate-specific scope and trust-boundary docs.
- Added a JSON-schema-bound inventory of all 184 numbered RFC 8489/8656
  sections and 393 uppercase normative keyword occurrences.
- Assigned every extracted requirement to a profile, component, implementation
  milestone, test milestone, status, and security note.
- Added reviewed decisions for all six current RFC 8489/8656 errata and an
  optional official live-drift comparison.
- Added negative fixtures for missing, duplicate, invalid, unassigned,
  orphaned, falsely completed, and unsafe errata entries.

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
