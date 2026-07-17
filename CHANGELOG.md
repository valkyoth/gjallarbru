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
- Added reservation-versus-attempt ingress accounting, transitive control-effect
  closure, post-publication crash reconciliation, no-atomic publication
  adapters, typed authorized endpoint capabilities, and one shared token-bucket
  model from ingress through hierarchical rate limiting.
- Added deterministic terminal-mailbox races, whole-process authority-loss
  semantics, just-in-time ingress reservation fairness, execution-time endpoint
  capability fences, and common per-frame work accounting across every client
  transport.
- Added acknowledged authority-sequence fences, two-stage pre-parse ingress
  classification, symmetric typed client-delivery capabilities, canonical
  incoming-peer checks, and per-packet capability ownership across partial
  batched sends.
- Added bounded coalesced fence watermarks, nonterminal timeout observations,
  charged cached-retransmission substates, and TCP/TLS partial-frame
  completion-or-close semantics with exact provider handoff boundaries.
- Added strict fence-versus-physical-ownership separation, bounded unresolved
  provider recovery, live peer/permission/channel authority for client-bound
  relay media, and pre-activation TLS/DTLS provider memory qualification.
- Added typed execution-domain quiescence evidence, an explicit cache-timing
  threat model, core-only queued-media reauthorization, and pre-plaintext
  TLS/DTLS control-work budgets with cross-provider closure.
- Added early executable reducer and crate-authority gates, adapter-neutral
  admission, complete locked-profile ledger passes, deterministic storage and
  sparse wire workspaces, honest nonce replay semantics, UDP GRO/GSO closure,
  and named allocation/copy profiles.
- Closed reducer commit/crash, canonical-state, caller-memory aliasing, scalar
  UDP truncation, terminal stream framing, runtime validation, constructible
  quiescence, bounded key-lease, `io_uring`, and AF_XDP lifecycle contracts.
- Added canonical ingress/ancillary metadata and unwind-poisoning releases, and
  confined state projections, 64-bit `io_uring` tokens, response-source
  selection, and eBPF epoch reclamation before their first production use.

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
