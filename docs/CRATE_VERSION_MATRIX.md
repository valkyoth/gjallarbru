# Crate Version Matrix

Status: all reusable crates are intentionally unpublished while their APIs and
independent release gates are being established.

Gjallarbru uses independent versions for crates.io packages. The server release
version remains the workspace milestone, while a reusable crate changes version
only when its own package contents require a crates.io release.

## Why Publish Reusable Crates

The executable remains the primary outcome. Publishing the narrow `no_std`
crates also lets other projects use the security-reviewed protocol boundaries
without adopting Gjallarbru's EUPL-1.2 server, operating-system runtime,
configuration model, or deployment choices:

- `gjallarbru-wire` can provide bounded STUN/TURN parsing, encoding, framing,
  typed attributes, and official-vector behavior to clients, proxies, test
  tools, embedded systems, or another server runtime;
- `gjallarbru-crypto` can provide provider-neutral STUN/TURN integrity, nonce,
  token, key-generation, and secret-handling composition without supplying
  cryptographic primitives;
- `gjallarbru-core` can provide a deterministic Sans-I/O STUN/TURN state engine
  for a different executor, appliance, simulator, mobile embedding, or future
  Aesynx adapter.

crates.io gives those consumers immutable package versions, Cargo-native
dependency resolution, checksums, documentation hosting, discoverability, and
a clear semver contract. GitHub remains the canonical source and issue tracker;
crates.io is a verified distribution channel, not a second development home.

## Version Rules

| Change kind | Version rule | Publish? |
| --- | --- | --- |
| `unpublished` | Keep the manifest version while the first public API is not admitted. | No |
| `initial` | Publish the reviewed manifest version after the independent crate gate passes. | Yes |
| `code` | Increment the crate's own minor version and reset patch to zero for a backward-compatible feature or material API addition. | Yes |
| `breaking` | Before 1.0, increment minor and reset patch; after 1.0, increment major and reset minor/patch. | Yes |
| `fix` | Increment only the existing patch version for a compatible code correction. | Yes |
| `dependency` | Increment only the existing patch version. | Yes |
| `metadata` | Increment only the existing patch version because crates.io package metadata is immutable. | Yes |
| `unchanged` | Keep the previous published version. | No |

`dependency` means first-party code did not materially change, but the package
manifest must reference a newly published internal dependency. `metadata`
means package contents such as the license expression, README, or manifest
metadata require correction without a code/API change.

`scripts/release_crates.py --check` validates `release-crates.toml`, independent
manifest versions, private-package publication denial, and dependency order.
Only crates marked `publish = true` are selected.

## Initial Publication Admission

Initial publication is versioned work, not an unspecified future action:

| Crate | Earliest admission milestone | Required scope |
| --- | --- | --- |
| `gjallarbru-wire` | `v0.22.0` | Wire API review, vectors, no-allocation evidence, fuzzing, MSRV matrix, package review, and exact-candidate pentest |
| `gjallarbru-crypto` | `v0.34.0` | Provider API review, authentication composition vectors, secret-handling review, package review, and exact-candidate pentest |
| `gjallarbru-core` | `v0.55.0` | Sans-I/O API review, RFC 8489/8656 conformance, state-model evidence, package review, and exact-candidate pentest |

An admission milestone is the earliest allowed publication, not an automatic
publish command. The permanent pentest report and crate-specific release gate
must pass first, and publication still requires explicit maintainer approval.

## v0.1.0 Tracking Table

| Crate | Published | Planned | Change | Publish | Reason |
| --- | --- | --- | --- | --- | --- |
| `gjallarbru-wire` | No | `0.1.0` | `unpublished` | No | Wire API and crate-specific gate are not stable. |
| `gjallarbru-crypto` | No | `0.1.0` | `unpublished` | No | Provider API and crate-specific gate are not stable. |
| `gjallarbru-core` | No | `0.1.0` | `unpublished` | No | Sans-I/O API and crate-specific gate are not stable. |

Update this table and `release-crates.toml` together whenever a crate changes
release state. Published crates must be processed in the dependency-safe order
`gjallarbru-wire`, `gjallarbru-crypto`, then `gjallarbru-core`.
