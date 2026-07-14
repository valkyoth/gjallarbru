# Gjallarbru Release Plan to 1.0

Status: planning document

This plan is intentionally granular. Gjallarbru parses unauthenticated
Internet traffic and controls relay access, so every version must be small
enough to implement, test, review, pentest, and stop cleanly before tagging.

[`VERSION_PLAN.md`](VERSION_PLAN.md) is the compact index. This document is the
authoritative release contract for every indexed version. The list is not a
maximum: split a release or insert a patch version immediately when review,
implementation, an RFC, or a security finding exposes additional work.

Tags use:

```text
v0.N.0      one narrow implementation or assurance milestone
v0.N.P      remediation or focused follow-up for milestone N
v1.0.0      first serious production-ready STUN/TURN server application
```

## Release Principles

Every release must have:

- one clear goal and a bounded definition of done;
- explicit deliverables and targeted verification commands;
- updated RFC requirement, errata, IANA, and conformance evidence where
  protocol behavior changes;
- positive, negative, malformed, boundary, timeout, duplicate, capacity, and
  failure tests applicable to its scope;
- dependency freshness, license, feature, MSRV, advisory, and source evidence;
- updated threat model, documentation, changelog, and release notes;
- an updated committed SBOM and package-content evidence;
- a versioned local release gate;
- completed pentest/retest evidence for a reviewed implementation commit that
  remains in the final candidate history, with later CodeQL fixes recorded;
- no hidden dependency on one platform, network service, or developer machine.

Every implementation prefers first-party STUN/TURN wire and state behavior,
reviewed provider boundaries for cryptography and secure transports, bounded
resource use, explicit platform capability errors, and a safe portable backend
as the reference for accelerated runtimes.

## Pentest Before Every Tag

Every milestone and patch version is pentested before tagging. A version is
not tag-ready until:

- `scripts/checks.sh`, `scripts/check-rust-version-matrix.sh`,
  `cargo deny --locked check`, and `cargo audit` pass;
- `scripts/generate-sbom.sh --check` confirms dependency-graph parity;
- the version-specific verification and release gate pass;
- release notes exist at `release-notes/RELEASE_NOTES_X.Y.Z.md`;
- root `PENTEST.md` is absent;
- `security/pentest/vX.Y.Z.md` records `Status: PASS`, the exact full
  `Reviewed-Commit`, tester, date, scope, methods, findings, fixes, retest, and
  residual risk;
- GitHub CI and CodeQL default setup are green for the final tag candidate;
- `scripts/validate-release-readiness.sh vX.Y.Z` passes;
- the tag does not already exist.

When a release's exit criteria are satisfied, stop and report exactly:

```text
vX.Y.Z implementation stop reached. Run pentest for this exact commit.
```

Do not create a tag at that stop.

### Pentest Handoff Flow

1. Finish, test, commit, and identify the implementation commit for pentest.
2. If pentest finds issues, the maintainer writes root `PENTEST.md`; fix and
   test them, commit the remediation, remove `PENTEST.md`, and request retest.
3. Repeat step 2 until pentest is green.
4. Create or update `security/pentest/vX.Y.Z.md` with `Status: PASS`, the
   reviewed commit, findings/fixes/retest, and residual risk, then commit it.
5. Push and wait for normal GitHub CI and CodeQL default setup.
6. If GitHub or CodeQL finds an issue, fix and test it, update the permanent
   report with the finding and remediation, commit, push, and wait again.
7. Repeat step 6 until GitHub CI and CodeQL are green.
8. Run release readiness, create the tag, and push the tag when the maintainer
   confirms the release should proceed.

The PASS report must be committed, and its `Reviewed-Commit` must remain an
ancestor of the final tag candidate. It does not need a special report-only
commit. This keeps the workflow flexible when CodeQL requires a later fix.

## Publication and Versioning

The EUPL-1.2 server is distributed primarily through GitHub Releases and
later OS packages. `gjallarbru-wire`, `gjallarbru-crypto`, and
`gjallarbru-core` use independent crates.io versions after API stability;
unchanged crates are not republished. `release-crates.toml` and
[`CRATE_VERSION_MATRIX.md`](CRATE_VERSION_MATRIX.md) distinguish unpublished,
initial, compatible code, breaking code, fixes, dependency-only, metadata-only,
and unchanged packages.
`scripts/release_crates.py` enforces dependency order and keeps the EUPL-1.2
runtime and server permanently outside crates.io publication.

## Completeness Review Register

Every planning and pentest pass checks for implied work without a release.
Current closure decisions are:

| Gap | Versioned resolution |
| --- | --- |
| Current STUN/TURN base and IPv6 could be mistaken for RFC 5389/5766/6156 layering. | RFC 8489 and RFC 8656 are the base from `v0.2.0`; IPv6 is native in `v0.48.0` and `v0.49.0`. |
| Integrity could be described as “MD5 HMAC.” | Separate legacy key derivation/HMAC-SHA-1 in `v0.18.0` and modern SHA-256 in `v0.19.0`. |
| Resource creation could occur before authentication. | Authentication and two-phase allocation are explicit in `v0.27.0`, `v0.38.0`, and `v0.39.0`. |
| Private-destination policy could be either universally blocked or accidentally open. | Explicit profiles and SSRF/loop controls in `v0.56.0` and `v0.57.0`. |
| Secure transports and crypto could become home-grown protocol code. | Provider boundaries in `v0.19.0`, `v0.73.0`, and `v0.75.0`; primitives/TLS/DTLS remain reviewed dependencies. |
| Linux acceleration could become protocol authority. | Differential portable/accelerated gates in `v0.78.0` through `v0.82.0`. |
| RFC 6062, RFC 7635, RFC 8016, REST compatibility, and RFC 5780 could be left “later.” | Each has a concrete release in `v0.83.0` through `v0.92.0`. |
| Platform and Aesynx support could be architectural slogans only. | Platform evidence in `v0.67.0` through `v0.69.0` and closure at `v0.95.0`. |
| `panic = "abort"` could turn one provider panic into indefinite whole-service loss. | `v0.66.1` adds supervised process containment, forced-abort tests, fencing, and restart SLO evidence. |
| Alternate routing, discovery, ALPN, PRECIS, DTLS 1.3, and registered optional attributes could be silently omitted. | Corrective protocol contracts are assigned to `v0.12.1`, `v0.20.1`, `v0.33.1`, `v0.54.1`, `v0.74.1`, `v0.76.1`, `v0.106.0`, and `v0.107.0`. |
| Tenant labels could exist without a security boundary. | Listener/destination/SNI realm selection and isolated authority domains are required by `v0.64.1`. |
| Pawalyze could expose a reusable browser credential. | Ephemeral OpenBao-backed issuance is `v0.91.1`; full browser and recovery closure is `v0.101.0`. |
| Multi-node service could imply impossible seamless allocation transfer or have no real node communication. | Node-local failure semantics, secure cluster communication, membership/load exchange, traffic ownership, and upgrades are `v0.96.0` through `v0.98.0`. |
| Fluxheim compatibility could be claimed through an HTTP or limited UDP path. | `v0.97.1` tests L4 TCP/TLS plus direct UDP and explicitly gates future generic UDP support. |
| A container could be promised without source identity, relay ranges, 443, performance, or operator choice. | Networking is qualified at `v0.99.0`; Wolfi and Debian images are `v0.100.0` and `v0.100.1`; unsafe topology is rejected. |
| IP-path, DDoS, capacity/cost, and privacy work could remain operator assumptions. | Dedicated production contracts are `v0.102.0` through `v0.105.0`. |
| Future readiness could be a one-time standards review. | API/config evolution, scheduled standards review, extension policy, and first-party provenance gates are `v0.108.0` through `v0.110.0`. |
| Formal, fuzz, packaging, operations, specification closure, and external audit could be postponed past 1.0. | Assigned to `v0.93.0`, `v0.94.0`, and `v0.111.0` through `v0.115.0`. |

## Phase A: Repository and Specification Foundation

### v0.1.0 - Repository Foundation

Goal: establish the serious workspace, trust boundaries, and release policy.

Deliverables:

- five focused crates with the documented `no_std` and license split;
- CI, CodeQL-default policy, dependency controls, SBOM, RFC locks, docs, and
  the versioned release gate;
- independent reusable-crate versions, publication manifest, dependency-order
  helper, tests, and explicit initial-publication admission milestones.

Verification:

- `scripts/checks.sh`
- `scripts/check-rust-version-matrix.sh`
- `scripts/release_0_1_gate.sh` after permanent pentest evidence exists

Exit criteria:

- A contributor can understand scope, trust boundaries, platform posture, and
  the pentest-before-tag process from repository evidence.
- Stop: `v0.1.0 implementation stop reached. Run pentest for this exact commit.`

### v0.2.0 - RFC Requirement Ledger

Goal: make every normative STUN/TURN rule visible before implementation.

Deliverables:

- machine-readable requirement schema with RFC, section, level, profile,
  component, symbol, test, status, and security notes;
- complete section inventories for RFC 8489 and RFC 8656 plus errata decisions.

Verification:

- `scripts/validate-requirements.sh`
- negative fixtures for missing, duplicate, invalid, and unassigned entries

Exit criteria:

- No normative base section is silently absent or marked complete without a
  test and implementation reference.
- Stop: `v0.2.0 implementation stop reached. Run pentest for this exact commit.`

### v0.3.0 - IANA Snapshot Tooling

Goal: make protocol assignments reviewed, generated, and reproducible.

Deliverables:

- dated method, attribute, error, channel, security-feature, and password
  algorithm registry snapshots with source metadata;
- manual updater, schema validator, deterministic generator, and review diff.

Verification:

- `scripts/check-iana-snapshot.sh`
- regenerate twice and compare byte-for-byte output

Exit criteria:

- Normal builds are offline and numeric assignments are not scattered as
  undocumented constants.
- Stop: `v0.3.0 implementation stop reached. Run pentest for this exact commit.`

### v0.4.0 - Primitive Domains

Goal: define OS-independent protocol, time, identity, limit, and error types.

Deliverables:

- IP/transport addresses, methods/classes, transaction IDs, channel numbers,
  paths, monotonic/absolute time, capacities, and stable errors;
- checked constructors and redacted formatting for sensitive identifiers.

Verification:

- `cargo test -p gjallarbru-wire -p gjallarbru-core`
- boundary and formatting tests for every constructor and error category

Exit criteria:

- Core APIs use explicit domains rather than OS socket types or ambiguous raw
  integers.
- Stop: `v0.4.0 implementation stop reached. Run pentest for this exact commit.`

### v0.5.0 - Checked Read and Write Cursors

Goal: centralize all untrusted offset and length arithmetic.

Deliverables:

- allocation-free checked read/write cursors and 4-byte padding helpers;
- stable failure offsets and output-unchanged-on-error contracts.

Verification:

- `cargo test -p gjallarbru-wire cursor`
- arbitrary-slice property tests and Kani candidates for every arithmetic path

Exit criteria:

- Protocol code has no unchecked direct indexing or wrapping offset math.
- Stop: `v0.5.0 implementation stop reached. Run pentest for this exact commit.`

### v0.6.0 - Generational Bounded Storage

Goal: make fixed capacity and stale-handle rejection foundational.

Deliverables:

- fixed generational slab, reservation/commit/remove transitions, and storage
  traits for later preallocated runtime slabs;
- capacity, generation wrap policy, and stale-reference tests.

Verification:

- `cargo test -p gjallarbru-core storage`
- model and Kani checks for reuse, exhaustion, and invalid generations

Exit criteria:

- No reusable core object can be addressed by an unversioned index.
- Stop: `v0.6.0 implementation stop reached. Run pentest for this exact commit.`

## Phase B: First-Party Wire Protocol

### v0.7.0 - STUN Header Decoder

Goal: decode the fixed STUN header with exact frame consumption.

Deliverables:

- method/class bit decoding, magic cookie, transaction ID, and aligned length;
- rejection of invalid high bits, truncation, overflow, and trailing bytes.

Verification:

- `cargo test -p gjallarbru-wire header`
- arbitrary 0–64 byte inputs never panic

Exit criteria:

- Every admitted header has one exact, bounded message range.
- Stop: `v0.7.0 implementation stop reached. Run pentest for this exact commit.`

### v0.8.0 - Borrowed Attribute Iterator

Goal: iterate exact attribute ranges without allocation or semantic loss.

Deliverables:

- borrowed raw attributes with header/value/padded ranges;
- duplicate/unknown preservation and truncated/padding error reporting.

Verification:

- `cargo test -p gjallarbru-wire attributes`
- property tests for arbitrary attribute sequences and deterministic failure

Exit criteria:

- Unknown and duplicate attributes remain available to later RFC-ordered
  semantic validation.
- Stop: `v0.8.0 implementation stop reached. Run pentest for this exact commit.`

### v0.9.0 - STUN and ChannelData Classifier

Goal: classify datagram and stream frame prefixes without ambiguity.

Deliverables:

- first-bit, cookie, channel-range, declared-length, and transport rules;
- explicit incomplete, invalid, STUN, and ChannelData outcomes.

Verification:

- `cargo test -p gjallarbru-wire classifier`
- exhaustive first-byte and boundary-length table tests

Exit criteria:

- No input is optimistically reclassified after a security-relevant failure.
- Stop: `v0.9.0 implementation stop reached. Run pentest for this exact commit.`

### v0.10.0 - Address Attributes

Goal: decode and encode IPv4/IPv6 mapped and XOR transport addresses.

Deliverables:

- family/port/address views with transaction-cookie XOR handling;
- exact-length, reserved-byte, unsupported-family, and round-trip tests.

Verification:

- `cargo test -p gjallarbru-wire address`
- RFC 5769 IPv4/IPv6 vectors

Exit criteria:

- Address conversion is allocation-free and never depends on host endianness.
- Stop: `v0.10.0 implementation stop reached. Run pentest for this exact commit.`

### v0.11.0 - Text and Error Attributes

Goal: expose text-bearing STUN attributes as bounded bytes before preparation.

Deliverables:

- USERNAME, REALM, NONCE, SOFTWARE, ERROR-CODE, and UNKNOWN-ATTRIBUTES views;
- length, reserved-bit, reason-size, duplicate, and non-UTF-8 behavior tests.

Verification:

- `cargo test -p gjallarbru-wire text_attributes`
- malformed UTF-8 and maximum-length fixtures

Exit criteria:

- Raw parsing never performs implicit Unicode normalization or logs secrets.
- Stop: `v0.11.0 implementation stop reached. Run pentest for this exact commit.`

### v0.12.0 - Authentication Attribute Views

Goal: preserve every byte range required for STUN integrity verification.

Deliverables:

- MESSAGE-INTEGRITY, MESSAGE-INTEGRITY-SHA256, USERHASH, PASSWORD-ALGORITHM,
  PASSWORD-ALGORITHMS, and alternate-domain views;
- ordering, duplicate, algorithm-parameter, and exact-offset tests.

Verification:

- `cargo test -p gjallarbru-wire auth_attributes`
- fixtures proving HMAC boundary reconstruction uses original bytes

Exit criteria:

- Authentication code never reconstructs a logically equivalent but
  byte-different message.
- Stop: `v0.12.0 implementation stop reached. Run pentest for this exact commit.`

### v0.12.1 - Forward-Compatible STUN Surface

Goal: expose the complete current extension surface without losing bytes or
silently assigning semantics to future protocol values.

Deliverables:

- typed views for ALTERNATE-SERVER, ALTERNATE-DOMAIN, SECURITY-FEATURES, and
  password-algorithm negotiation, with exact duplicate and ordering rules;
- raw preservation for unknown comprehension-optional attributes and bounded,
  non-panicking representation of unknown methods and classes;
- an extension boundary requiring explicit schema and security review before an
  unknown value can affect authentication, routing, state, or resources.

Verification:

- exhaustive known/unknown method, class, attribute, bit, duplicate, and truncation tests
- properties proving unknown optional bytes survive unchanged and unknown required
  attributes enter the authenticated 420 path

Exit criteria:

- Future optional values remain observable but inert, and no unknown value can acquire
  authority through a fallback or lossy decode.
- Stop: `v0.12.1 implementation stop reached. Run pentest for this exact commit.`

### v0.13.0 - TURN Allocation Attributes

Goal: decode and encode every RFC 8656 allocation-control attribute.

Deliverables:

- REQUESTED-TRANSPORT, LIFETIME, address-family, EVEN-PORT,
  RESERVATION-TOKEN, and DONT-FRAGMENT views;
- reserved-bit, length, family-combination, and token-size tests.

Verification:

- `cargo test -p gjallarbru-wire allocation_attributes`
- generated valid/invalid combination fixtures

Exit criteria:

- Wire decoding exposes values without implying semantic validity.
- Stop: `v0.13.0 implementation stop reached. Run pentest for this exact commit.`

### v0.14.0 - Permission, Channel, and ICMP Attributes

Goal: complete borrowed wire coverage needed by UDP TURN relay behavior.

Deliverables:

- XOR-PEER-ADDRESS, CHANNEL-NUMBER, DATA, and ICMP views/encoders;
- zero-length data, channel-range, padding, ICMP family/type, and oversize tests.

Verification:

- `cargo test -p gjallarbru-wire relay_attributes`
- all minimum/maximum/truncated attribute fixtures

Exit criteria:

- Every base relay attribute has one typed, bounded decode path.
- Stop: `v0.14.0 implementation stop reached. Run pentest for this exact commit.`

### v0.15.0 - ChannelData Codec

Goal: encode and decode ChannelData correctly on datagram and stream transports.

Deliverables:

- borrowed channel/payload views and caller-buffer encoder;
- channel range, declared length, datagram exactness, and stream padding rules.

Verification:

- `cargo test -p gjallarbru-wire channel_data`
- round trips across every payload length modulo four

Exit criteria:

- Stream padding is consumed correctly and never counted as peer payload.
- Stop: `v0.15.0 implementation stop reached. Run pentest for this exact commit.`

### v0.16.0 - STUN Caller-Buffer Encoder

Goal: build canonical STUN messages once into caller-provided storage.

Deliverables:

- header reservation, attribute writers, padding, length finalization, and
  transactional output behavior;
- exact-size, short-buffer, maximum-message, and failed-encode tests.

Verification:

- `cargo test -p gjallarbru-wire encoder`
- encode/decode canonical round-trip properties

Exit criteria:

- Encoding performs no temporary allocation and failure leaves output
  uncommitted.
- Stop: `v0.16.0 implementation stop reached. Run pentest for this exact commit.`

### v0.17.0 - FINGERPRINT

Goal: implement exact STUN CRC-32 fingerprint framing and verification.

Deliverables:

- provider/first-party CRC decision, final-attribute enforcement, and XOR
  constant handling;
- official, corruption, wrong-position, and duplicate vectors.

Verification:

- `cargo test -p gjallarbru-wire fingerprint`
- RFC 5769 vectors

Exit criteria:

- FINGERPRINT is calculated over the exact required bytes and can only be last.
- Stop: `v0.17.0 implementation stop reached. Run pentest for this exact commit.`

### v0.18.0 - Legacy Message Integrity

Goal: support legacy long-term credentials without making them the modern core.

Deliverables:

- reviewed MD5 key-derivation and HMAC-SHA-1 provider boundaries;
- exact adjusted-length verification/encoding and constant-time comparison.

Verification:

- `cargo test -p gjallarbru-crypto -p gjallarbru-wire legacy_integrity`
- RFC 5769 plus malformed, ordering, and wrong-key vectors

Exit criteria:

- Legacy behavior is explicit, opt-in by profile, and cannot bypass exact
  message-range checks.
- Stop: `v0.18.0 implementation stop reached. Run pentest for this exact commit.`

### v0.19.0 - SHA-256 Message Integrity

Goal: implement the preferred modern password and integrity mechanisms.

Deliverables:

- SHA-256 derivation and HMAC-SHA-256 provider boundaries;
- RFC 8489 integrity ordering, algorithm negotiation inputs, and errata decisions.

Verification:

- `cargo test -p gjallarbru-crypto -p gjallarbru-wire sha256_integrity`
- official/project KATs, downgrade, truncation, and mixed-integrity vectors

Exit criteria:

- SHA-256 is the hardened profile and legacy fallback is never implicit.
- Stop: `v0.19.0 implementation stop reached. Run pentest for this exact commit.`

### v0.20.0 - USERHASH and Text Preparation

Goal: prepare credential text exactly as required without home-grown Unicode.

Deliverables:

- reviewed no_std/PRECIS adapter boundary, canonical byte output, and limits;
- USERHASH construction/verification and invalid UTF-8/code-point tests.

Verification:

- `cargo test -p gjallarbru-crypto userhash`
- pinned Unicode/PRECIS vectors and dependency-policy gates

Exit criteria:

- Credential preparation is deterministic, bounded, and provider-versioned.
- Stop: `v0.20.0 implementation stop reached. Run pentest for this exact commit.`

### v0.20.1 - RFC 8265 PRECIS Closure

Goal: make current internationalized username and password preparation a
normative, versioned compatibility boundary rather than an implicit library detail.

Deliverables:

- RFC 8265 requirement/errata ledger, selected UsernameCaseMapped and OpaqueString
  profiles, Unicode-version policy, size ceilings, and provider-version pinning;
- migration rules across provider/Unicode changes and explicit rejection of unstable,
  disallowed, non-canonical, or expansion-over-limit input;
- byte-exact linkage from prepared strings to USERHASH and long-term key derivation.

Verification:

- RFC/provider vectors, Unicode boundary corpus, version migrations, invalid UTF-8,
  normalization, expansion-limit, and cross-version regression tests
- no_std/MSRV, dependency provenance, license, advisory, and provider-differential gates

Exit criteria:

- Authentication text has one documented RFC 8265 interpretation per profile, and an
  update cannot silently change accepted identities or derived keys.
- Stop: `v0.20.1 implementation stop reached. Run pentest for this exact commit.`

### v0.21.0 - Incremental Stream Framer

Goal: safely frame STUN and ChannelData over TCP/TLS byte streams.

Deliverables:

- incremental state, partial/coalesced frame handling, byte/frame ceilings,
  and no borrowed references across buffer mutation;
- EOF, oversized prefix, slow partial frame, and padding tests.

Verification:

- `cargo test -p gjallarbru-wire stream_framer`
- property tests over every chunk split for representative frames

Exit criteria:

- Stream framing is bounded independently of later socket backpressure.
- Stop: `v0.21.0 implementation stop reached. Run pentest for this exact commit.`

### v0.22.0 - Wire Assurance Milestone

Goal: close the first-party wire profile before stateful server work.

Deliverables:

- separate fuzz targets for header, attributes, addresses, frames, encoder,
  integrity ranges, and stream framing;
- promoted corpus, requirement links, allocation evidence, and API review.
- `gjallarbru-wire` initial-publication decision and crate-specific package gate.

Verification:

- `cargo test -p gjallarbru-wire -p gjallarbru-crypto --all-features`
- wire fuzz smoke, MSRV matrix, cargo-deny, cargo-audit, and release gate

Exit criteria:

- All claimed wire behavior is vector-backed, fuzzed, no_std, no-alloc, and
  ready for independent crates.io API review.
- Stop: `v0.22.0 implementation stop reached. Run pentest for this exact commit.`

## Phase C: STUN Server Core

### v0.23.0 - Sans-I/O Event and Command API

Goal: establish the deterministic boundary between protocol authority and I/O.

Deliverables:

- bounded client/peer/runtime/tick events and send/open/close/lookup/audit commands;
- command sink capacity errors and explicit packet-lease lifetime rules.

Verification:

- `cargo test -p gjallarbru-core sans_io`
- compile-fail/lifetime and command-capacity tests

Exit criteria:

- Core processing performs no I/O, clock read, heap allocation, or escaping borrow.
- Stop: `v0.23.0 implementation stop reached. Run pentest for this exact commit.`

### v0.24.0 - Binding State Processing

Goal: implement Binding request validation and response planning without sockets.

Deliverables:

- method/schema validation, XOR-MAPPED-ADDRESS response, optional integrity,
  fingerprint, and redacted SOFTWARE policy;
- malformed request, indication, response-class, and output-capacity tests.

Verification:

- `cargo test -p gjallarbru-core binding`
- synthetic IPv4/IPv6 event-to-command vectors

Exit criteria:

- Binding behavior is deterministic for every admitted transport path.
- Stop: `v0.24.0 implementation stop reached. Run pentest for this exact commit.`

### v0.25.0 - Stateless Authenticated Nonces

Goal: issue and validate replay-resistant nonces without a nonce database.

Deliverables:

- versioned source/path/realm/time-bound nonce format with key ID and tag;
- active/previous/revoked key handling, stale response, tamper, and cross-path tests.

Verification:

- `cargo test -p gjallarbru-crypto nonce`
- arbitrary nonce decode fuzzing and deterministic time tests

Exit criteria:

- A nonce cannot be replayed across path or realm and key rotation fails closed.
- Stop: `v0.25.0 implementation stop reached. Run pentest for this exact commit.`

### v0.26.0 - Credential Provider Boundary

Goal: resolve credentials without coupling core state to storage or blocking I/O.

Deliverables:

- bounded query/result/operation IDs, fixed provider, pending provider, timeout,
  cancellation, and derived-key record types;
- capacity, stale completion, missing identity, expiry, and redaction tests.

Verification:

- `cargo test -p gjallarbru-core credentials`
- reference-provider differential and reordered completion tests

Exit criteria:

- Credential sources cannot mutate allocations or expose plaintext passwords.
- Stop: `v0.26.0 implementation stop reached. Run pentest for this exact commit.`

### v0.27.0 - Long-Term Authentication Pipeline

Goal: encode RFC-ordered 401, 438, and successful authentication decisions.

Deliverables:

- one auditable pipeline for presence, realm, nonce, lookup, integrity, identity,
  response integrity, and error ordering;
- success/failure matrices for USERNAME and USERHASH across transports.

Verification:

- `cargo test -p gjallarbru-core authentication`
- official/project vectors plus reordered, duplicate, stale, and wrong-key cases

Exit criteria:

- Authentication failure cannot create state or reveal post-authentication policy.
- Stop: `v0.27.0 implementation stop reached. Run pentest for this exact commit.`

### v0.28.0 - Password Negotiation Profiles

Goal: make hardened and legacy-interoperability authentication explicit.

Deliverables:

- profile policy, PASSWORD-ALGORITHMS negotiation, downgrade rejection, and
  response algorithm binding;
- configuration validation preventing accidental legacy enablement.

Verification:

- `cargo test -p gjallarbru-core password_negotiation`
- cross-profile and downgrade matrix

Exit criteria:

- No request silently weakens a listener's configured authentication profile.
- Stop: `v0.28.0 implementation stop reached. Run pentest for this exact commit.`

### v0.29.0 - Unknown and Invalid Attribute Ordering

Goal: implement authenticated 420 and method-schema errors in RFC order.

Deliverables:

- bounded unknown-required accumulator and known-unexpected/duplicate schemas;
- pre/post-authentication oracle tests and response-size limits.

Verification:

- `cargo test -p gjallarbru-core attribute_validation`
- generated method/attribute matrix tests

Exit criteria:

- Unknown attributes are neither discarded too early nor disclosed before auth.
- Stop: `v0.29.0 implementation stop reached. Run pentest for this exact commit.`

### v0.30.0 - Transaction Cache

Goal: make request retransmission idempotent before side-effecting TURN methods.

Deliverables:

- bounded pending/completed/reconstructable records keyed by path, transaction,
  and method with request digests and expiry;
- exact duplicate, digest mismatch, pending timeout, eviction, and exhaustion tests.

Verification:

- `cargo test -p gjallarbru-core transaction_cache`
- model/property tests over duplicate and reordered events

Exit criteria:

- One transaction can trigger each external side effect at most once.
- Stop: `v0.30.0 implementation stop reached. Run pentest for this exact commit.`

### v0.31.0 - Portable IPv4 UDP Binding Runtime

Goal: connect real UDP sockets to the same Binding core path used in tests.

Deliverables:

- safe single-worker portable UDP listener, fixed buffer pool, path conversion,
  command execution, and clean shutdown;
- loopback integration harness with no task/timer per request.

Verification:

- `cargo test -p gjallarbru-runtime udp_binding_ipv4`
- local black-box Binding request/response smoke

Exit criteria:

- Real socket behavior matches synthetic core vectors and remains bounded.
- Stop: `v0.31.0 implementation stop reached. Run pentest for this exact commit.`

### v0.32.0 - IPv6 and Dual-Stack Binding Runtime

Goal: make IPv6 path identity and listener policy first-class.

Deliverables:

- IPv6 sockets, v6-only/dual-stack configuration, scoped-address rejection,
  mapped-address policy, and local-address preservation;
- platform-neutral IPv4/IPv6 test fixtures.

Verification:

- `cargo test -p gjallarbru-runtime udp_binding_ipv6`
- IPv4-only, IPv6-only, and dual-stack smoke tests

Exit criteria:

- Address-family behavior is explicit and does not depend on OS defaults.
- Stop: `v0.32.0 implementation stop reached. Run pentest for this exact commit.`

### v0.33.0 - STUN Errors and Retransmission Closure

Goal: finish transport-aware STUN error and duplicate-response behavior.

Deliverables:

- bounded error encoder, UDP cache/replay policy, reliable-transport no-retry
  behavior, and unauthenticated amplification ceiling;
- dropped-response, loss, duplicate, delayed, and response-ratio tests.

Verification:

- `cargo test -p gjallarbru-core -p gjallarbru-runtime stun_transactions`
- packet-loss simulation and amplification report

Exit criteria:

- STUN transaction behavior is complete for the claimed Binding transports.
- Stop: `v0.33.0 implementation stop reached. Run pentest for this exact commit.`

### v0.33.1 - Alternate Routing and Security Negotiation

Goal: implement redirection and security-feature negotiation without redirect
loops, cross-realm credential exposure, or downgrade behavior.

Deliverables:

- 300 Try Alternate policy for ALTERNATE-SERVER and ALTERNATE-DOMAIN, including
  transport, trust-domain, realm, credential, and client/server applicability rules;
- hop/loop ceilings, allowlists, DNS-rebinding defense, cache lifetime, and failure behavior;
- SECURITY-FEATURES bit negotiation with unknown-bit preservation and fail-closed
  handling for required, conflicting, stripped, or downgraded features.

Verification:

- redirect success, loop, chain, untrusted domain, cross-realm, stale DNS, missing TLS,
  unknown-bit, stripping, downgrade, amplification, and malformed-response tests
- independent-client interoperability and RFC 8489 requirement-ledger evidence

Exit criteria:

- A redirect cannot disclose credentials or escape configured trust, and security
  negotiation cannot become weaker through omission, retry, or unknown-bit handling.
- Stop: `v0.33.1 implementation stop reached. Run pentest for this exact commit.`

### v0.34.0 - `stun-base` Milestone

Goal: verify and publish the complete base STUN profile evidence.

Deliverables:

- RFC 8489 requirement/errata matrix, RFC 5769 report, interoperability matrix,
  fuzz corpus, threat-model update, and unsupported-scope statement;
- `gjallarbru-crypto` initial-publication decision and crates.io package review,
  plus API review for reusable core surfaces reached so far.

Verification:

- full STUN conformance and interoperability commands
- `scripts/release_0_34_gate.sh`

Exit criteria:

- Every claimed `stun-base` normative rule is verified with no unexplained gap.
- Stop: `v0.34.0 implementation stop reached. Run pentest for this exact commit.`

## Phase D: RFC 8656 UDP TURN

### v0.35.0 - Allocation Records and Indexes

Goal: model allocation ownership and lookups before relay sockets exist.

Deliverables:

- pending/active/closing allocation records and path/relay/identity indexes;
- one/two-family relay sets, bounded permission/channel namespaces, and counters.

Verification:

- `cargo test -p gjallarbru-core allocation_storage`
- reference-model ownership, collision, removal, and exhaustion tests

Exit criteria:

- One live relay belongs to one allocation and one path owns at most one allocation.
- Stop: `v0.35.0 implementation stop reached. Run pentest for this exact commit.`

### v0.36.0 - Hierarchical Timing Wheel

Goal: expire every TURN object without one OS timer per object.

Deliverables:

- worker-local hierarchical wheel for allocation, permission, channel, reuse,
  reservation, transaction, credential, operation, and fast-path timers;
- wrap, lag, reschedule, stale-generation, and capacity behavior.

Verification:

- `cargo test -p gjallarbru-core timing_wheel`
- model/property tests over time jumps and arbitrary expiry order

Exit criteria:

- Timer processing is bounded and stale entries cannot affect reused objects.
- Stop: `v0.36.0 implementation stop reached. Run pentest for this exact commit.`

### v0.37.0 - Randomized Relay-Port Allocator

Goal: reserve relay ports predictably in cost but unpredictably in selection.

Deliverables:

- per-IP/family/transport/shard port tables and CSPRNG-seeded bounded selection;
- free/reserved/opening/allocated transitions and atomic adjacent-port reservation.

Verification:

- `cargo test -p gjallarbru-core relay_ports`
- collision, exhaustion, randomness-health, rollback, and concurrency model tests

Exit criteria:

- Hostile requests cannot cause sequential leakage or unbounded port search.
- Stop: `v0.37.0 implementation stop reached. Run pentest for this exact commit.`

### v0.38.0 - Allocate Semantic Validation

Goal: validate Allocate completely before any relay resource is opened.

Deliverables:

- requested transport/family/lifetime/even-port/reservation/fragment schemas;
- authentication, existing allocation, quota, policy, and relay availability ordering.

Verification:

- `cargo test -p gjallarbru-core allocate_validation`
- every RFC error path asserts zero OpenRelay commands

Exit criteria:

- Invalid or unauthenticated Allocate requests cannot reserve external resources.
- Stop: `v0.38.0 implementation stop reached. Run pentest for this exact commit.`

### v0.39.0 - Two-Phase Allocation State

Goal: commit allocation state only after a matching relay-open completion.

Deliverables:

- provisional slot/port/transaction reservations and operation generations;
- success commit plus complete rollback on failure, timeout, disconnect, or stale result.

Verification:

- `cargo test -p gjallarbru-core allocate_two_phase`
- duplicate/reordered completion and fault-injection model tests

Exit criteria:

- Duplicate Allocate cannot create two relays and failed opens leak no state.
- Stop: `v0.39.0 implementation stop reached. Run pentest for this exact commit.`

### v0.40.0 - Portable Relay Socket Adapter

Goal: execute exact UDP relay open/close/send commands with safe portable sockets.

Deliverables:

- relay bind options, socket registry, peer events, buffer ownership, and error mapping;
- fixed pool/prebind extension points without changing core commands.

Verification:

- `cargo test -p gjallarbru-runtime relay_socket`
- real bind conflict, exhaustion, close, stale event, and loopback peer tests

Exit criteria:

- Runtime socket outcomes map one-to-one to explicit core completions.
- Stop: `v0.40.0 implementation stop reached. Run pentest for this exact commit.`

### v0.40.1 - Relay Address Topology

Goal: separate socket binding from the public relay identity advertised across
direct, one-to-one NAT, cloud, container, and multi-homed deployments.

Deliverables:

- explicit bind, local-destination, advertised/public, and relay-pool address types;
- validated one-to-one family mappings, multiple public relay-IP pools, listener/realm/
  tenant selection, deterministic port ownership, and conflict rejection;
- startup and continuous checks preventing unroutable, overlapping, looped, ambiguous,
  changed, or family-incompatible addresses from being advertised.

Verification:

- network-namespace tests for direct hosts, one-to-one NAT, multi-homing, multiple IP
  pools, address changes, asymmetric routes, and invalid mappings
- Allocate/relay packet captures proving the advertised endpoint is reachable while the
  runtime binds only its intended local endpoint

Exit criteria:

- Every advertised relay address has one validated ownership path, and Gjallarbru
  refuses service instead of publishing an ambiguous or unverifiable relay endpoint.
- Stop: `v0.40.1 implementation stop reached. Run pentest for this exact commit.`

### v0.41.0 - Allocate Completion and Responses

Goal: produce complete RFC 8656 Allocate success and failure responses.

Deliverables:

- actual lifetime, XOR-RELAYED-ADDRESS, XOR-MAPPED-ADDRESS, optional reservation,
  matching integrity, transaction caching, and cleanup;
- response-capacity and send-failure policy.

Verification:

- `cargo test -p gjallarbru-core allocate_completion`
- synthetic plus real relay allocation round trips

Exit criteria:

- An active allocation becomes peer-visible only after committed response state.
- Stop: `v0.41.0 implementation stop reached. Run pentest for this exact commit.`

### v0.42.0 - Refresh and Allocation Deletion

Goal: refresh or delete only the allocation owned by the authenticated path/identity.

Deliverables:

- lifetime clamp, same-identity enforcement, zero-lifetime close, and atomic
  removal of permissions, channels, relays, timers, cache, and fast-path rules;
- partial close and repeated deletion tests.

Verification:

- `cargo test -p gjallarbru-core refresh`
- model tests for 441, expiry races, and cleanup completeness

Exit criteria:

- Refresh cannot revive expired authority or leave reachable relay state after deletion.
- Stop: `v0.42.0 implementation stop reached. Run pentest for this exact commit.`

### v0.43.0 - CreatePermission

Goal: create bounded peer-IP permissions atomically.

Deliverables:

- family-aware peer-IP keys, multi-address request validation, policy/quota gates,
  300-second expiry, refresh, and all-or-none mutation;
- duplicate, mixed-family, forbidden, capacity, and rollback tests.

Verification:

- `cargo test -p gjallarbru-core permissions`
- reference-model and time-advance tests

Exit criteria:

- Peer ports do not affect permission identity and invalid batches change nothing.
- Stop: `v0.43.0 implementation stop reached. Run pentest for this exact commit.`

### v0.44.0 - Client-to-Peer Send Indication

Goal: relay client datagrams only through live authorized permissions.

Deliverables:

- exact peer/data schema, family/policy/permission/quota checks, and SendPeer command;
- RFC-required silent discard with no permission refresh or response oracle.

Verification:

- `cargo test -p gjallarbru-core send_indication`
- missing/expired permission, forbidden destination, zero/maximum data tests

Exit criteria:

- No SendPeer command exists without current allocation and permission authority.
- Stop: `v0.44.0 implementation stop reached. Run pentest for this exact commit.`

### v0.45.0 - Peer-to-Client Data Indication

Goal: deliver permitted peer UDP datagrams through bounded STUN indications.

Deliverables:

- relay ownership lookup, peer-IP permission filter, inbound limits, and Data encoder;
- unknown/stale relay, expired permission, buffer exhaustion, and send-failure tests.

Verification:

- `cargo test -p gjallarbru-core peer_data`
- real relay socket bidirectional integration test

Exit criteria:

- Unsolicited peer traffic is dropped before client output is constructed.
- Stop: `v0.45.0 implementation stop reached. Run pentest for this exact commit.`

### v0.46.0 - ChannelBind

Goal: create one-to-one channel/peer bindings under live permission policy.

Deliverables:

- dual indexes, uniqueness checks, permission creation/refresh, 600-second expiry,
  and five-minute post-expiry reuse block;
- conflict, refresh, race, capacity, and rollback tests.

Verification:

- `cargo test -p gjallarbru-core channel_bind`
- model tests for both lookup directions and reuse timing

Exit criteria:

- A channel and peer cannot be rebound inconsistently within an allocation.
- Stop: `v0.46.0 implementation stop reached. Run pentest for this exact commit.`

### v0.47.0 - ChannelData Relay

Goal: relay ChannelData in both directions with no hidden lifetime refresh.

Deliverables:

- client channel lookup plus peer exact-address channel selection;
- permission recheck, rate/byte limits, headroom/scatter plans, and stream padding.

Verification:

- `cargo test -p gjallarbru-core channel_data_relay`
- UDP/stream round trips and expiry-with-active-traffic tests

Exit criteria:

- ChannelData never outlives either its channel binding or peer-IP permission.
- Stop: `v0.47.0 implementation stop reached. Run pentest for this exact commit.`

### v0.48.0 - IPv6 Relays

Goal: make IPv6 relayed transport addresses fully interoperable.

Deliverables:

- IPv6 relay pools, family-specific port tables, peer policies, permissions,
  channels, mapped responses, and ICMP extension points;
- IPv4/IPv6 family mismatch and unavailable-family errors.

Verification:

- `cargo test -p gjallarbru-core -p gjallarbru-runtime ipv6_relay`
- IPv6-only black-box allocation and relay test

Exit criteria:

- IPv6 is a base allocation path, not a compatibility shim.
- Stop: `v0.48.0 implementation stop reached. Run pentest for this exact commit.`

### v0.49.0 - Additional Address Family

Goal: safely allocate both relay families within one RFC 8656 allocation.

Deliverables:

- atomic dual-relay provisional/commit/rollback state and family-specific permission/channel keys;
- partial-open failure, duplicate family, ordering, expiry, and response tests.

Verification:

- `cargo test -p gjallarbru-core dual_family`
- dual-stack interoperability and injected second-bind failure tests

Exit criteria:

- Dual-family allocation either commits the RFC-valid set or leaks no relay.
- Stop: `v0.49.0 implementation stop reached. Run pentest for this exact commit.`

### v0.50.0 - EVEN-PORT and Reservation Tokens

Goal: implement adjacent reservation and one-time token consumption securely.

Deliverables:

- authenticated versioned token bound to pool/family/transport/port/expiry;
- atomic reserved-to-opening-to-allocated transition and token key rotation.

Verification:

- `cargo test -p gjallarbru-core reservation_tokens`
- tamper, replay, expiry, collision, adjacent exhaustion, and rollback tests

Exit criteria:

- A reservation can be consumed once and cannot address another pool or generation.
- Stop: `v0.50.0 implementation stop reached. Run pentest for this exact commit.`

### v0.51.0 - DONT-FRAGMENT

Goal: expose fragmentation policy without pretending every platform supports it.

Deliverables:

- core request policy, runtime capability/result contract, and exact error mapping;
- platform-supported, unsupported, permission-denied, and fallback rejection tests.

Verification:

- `cargo test -p gjallarbru-core -p gjallarbru-runtime dont_fragment`
- platform capability matrix

Exit criteria:

- Unsupported fragmentation control fails explicitly and never silently weakens policy.
- Stop: `v0.51.0 implementation stop reached. Run pentest for this exact commit.`

### v0.52.0 - ICMP Error Forwarding

Goal: forward only correlated, permitted ICMP errors through bounded Data indications.

Deliverables:

- runtime error-queue normalization and core peer/original-destination correlation;
- supported family/type/code policy and forged/unrelated error rejection.

Verification:

- `cargo test -p gjallarbru-core -p gjallarbru-runtime icmp`
- synthetic and OS-supported loopback error-queue tests

Exit criteria:

- Outer ICMP source alone can never authorize client-visible error data.
- Stop: `v0.52.0 implementation stop reached. Run pentest for this exact commit.`

### v0.53.0 - TURN State Model Milestone

Goal: verify allocation, timer, transaction, permission, and channel invariants together.

Deliverables:

- simple std reference model and arbitrary event-sequence generator;
- resource-counter reconciliation, fault injection, and invariant report.

Verification:

- `cargo test -p gjallarbru-core model`
- state-sequence fuzz smoke with time jumps and reordered completions

Exit criteria:

- Production bounded state matches the reference model for all generated operations.
- Stop: `v0.53.0 implementation stop reached. Run pentest for this exact commit.`

### v0.54.0 - UDP Interoperability

Goal: prove real TURN UDP behavior against independent clients.

Deliverables:

- browser WebRTC, native ICE client, and coturn-oracle harnesses;
- IPv4/IPv6/dual-family, NAT, loss, duplication, reorder, stale credential,
  permission expiry, channel, and reservation scenarios.

Verification:

- documented interoperability runner and result matrix
- soak and packet-capture assertions with secret redaction

Exit criteria:

- The server relays media/control datagrams interoperably without relying on another TURN implementation internally.
- Stop: `v0.54.0 implementation stop reached. Run pentest for this exact commit.`

### v0.54.1 - URI, DNS, and Discovery Profile

Goal: make standardized endpoint publication and client discovery interoperable
without ambiguous transport choice or insecure downgrade.

Deliverables:

- RFC 7064 STUN/STUNS and RFC 7065 TURN/TURNS URI parsing, validation,
  normalization, transport defaults, configuration emission, and documentation;
- RFC 5928 DNS resolution and RFC 8155 auto-discovery deployment records, priority/
  weight behavior, TTL, loop bounds, DNSSEC policy, and failure/fallback rules;
- an applicability ledger where client discovery is verified with an independent
  resolver fixture rather than placed inside the server protocol core.

Verification:

- valid/invalid URI corpus and deterministic SRV/NAPTR fixtures for UDP, TCP, TLS,
  IPv4, IPv6, priorities, weights, TTL expiry, and unavailable targets
- browser/native interoperability plus downgrade, rebinding, poisoned-cache,
  cross-realm, redirect-interaction, and bounded-query tests

Exit criteria:

- Published endpoints select the intended secure transport and realm, and discovery
  failure cannot expose credentials or silently fall back to a forbidden path.
- Stop: `v0.54.1 implementation stop reached. Run pentest for this exact commit.`

### v0.55.0 - `turn-udp-base` Conformance

Goal: close every claimed RFC 8656 base requirement and erratum.

Deliverables:

- generated conformance report, unsupported/non-applicable rationale, RFC drift check,
  fuzz/interop evidence, and full base-profile threat-model review;
- independent pentest scope covering wire, auth, state, relay, runtime, and policy;
- `gjallarbru-core` initial-publication decision and crate-specific package gate.

Verification:

- complete RFC 8656 conformance command
- `scripts/release_0_55_gate.sh`

Exit criteria:

- No claimed base MUST/MUST NOT/SHOULD remains planned or merely implemented.
- Stop: `v0.55.0 implementation stop reached. Run pentest for this exact commit.`

## Phase E: Security and Operations

### v0.56.0 - Destination Policy Profiles

Goal: make peer reachability explicit for public, enterprise, custom, and test deployments.

Deliverables:

- immutable numeric prefix/profile decisions with deny reasons and rate classes;
- special-use, internal allowlist, DNS-at-load-only, policy generation, and atomic reload tests.

Verification:

- `cargo test -p gjallarbru-core destination_policy`
- generated IPv4/IPv6 special-purpose registry fixtures

Exit criteria:

- Private unicast is neither universally rejected nor accidentally public.
- Stop: `v0.56.0 implementation stop reached. Run pentest for this exact commit.`

### v0.57.0 - SSRF and Relay-Loop Prevention

Goal: prevent TURN from reaching protected infrastructure or recursively relaying.

Deliverables:

- listener, control, metadata, database, relay-pool, same-allocation, local-node,
  and configured-sensitive-prefix denial;
- source/destination loop detection and policy-epoch invalidation.

Verification:

- `cargo test -p gjallarbru-core relay_loop_policy`
- cloud metadata, local services, multi-listener, and two-node loop fixtures

Exit criteria:

- Public-server defaults fail closed for every known self/infrastructure path.
- Stop: `v0.57.0 implementation stop reached. Run pentest for this exact commit.`

### v0.58.0 - Hierarchical Quotas

Goal: charge every scarce resource to all applicable authority dimensions.

Deliverables:

- global/listener/worker/relay-IP/source-prefix/realm/tenant/identity/allocation/peer counters;
- atomic reserve/commit/release for allocations, ports, permissions, channels,
  TCP connections, lookups, transactions, buffers, and handshakes.

Verification:

- `cargo test -p gjallarbru-core quotas`
- model tests proving counters equal live resources under failures/reordering

Exit criteria:

- No resource can exceed any configured parent or child ceiling.
- Stop: `v0.58.0 implementation stop reached. Run pentest for this exact commit.`

### v0.59.0 - Deterministic Rate Limiting

Goal: bound ongoing work and traffic with injected monotonic time.

Deliverables:

- token buckets for auth, allocation, errors, packets, bytes, lookups, and admin work;
- burst/fairness classes, spoofable-source policy, saturation arithmetic, and clock-jump handling.

Verification:

- `cargo test -p gjallarbru-core rate_limit`
- deterministic burst, fairness, wrap, and prolonged-overload simulations

Exit criteria:

- Rate limiting cannot be bypassed by time anomalies or one quota dimension.
- Stop: `v0.59.0 implementation stop reached. Run pentest for this exact commit.`

### v0.60.0 - Credential Cache and Revocation

Goal: bound credential latency while making revocation promptly authoritative.

Deliverables:

- positive/negative expiring cache, identity generations, lookup deduplication,
  timeout/backoff, and revocation events;
- policy for existing allocation teardown versus refresh denial.

Verification:

- `cargo test -p gjallarbru-core credential_cache`
- stale completion, revoke race, provider outage, and cache exhaustion tests

Exit criteria:

- Revoked identities cannot allocate or refresh and stale cache data cannot restore authority.
- Stop: `v0.60.0 implementation stop reached. Run pentest for this exact commit.`

### v0.61.0 - Key Lifecycle and Rotation

Goal: rotate each cryptographic key domain independently and auditably.

Deliverables:

- credential, nonce, reservation, mobility, third-party, TLS ticket, and admin key domains;
- active/previous/revoked generations, overlap ceilings, zeroization/provider contracts,
  startup validation, and rollback prohibition.

Verification:

- `cargo test -p gjallarbru-crypto key_rotation`
- compromise, expired overlap, wrong-domain, restart, and concurrent rotation tests

Exit criteria:

- One key compromise cannot silently authorize another token or transport domain.
- Stop: `v0.61.0 implementation stop reached. Run pentest for this exact commit.`

### v0.62.0 - Bounded Metrics and Audit Sinks

Goal: expose operational evidence without creating leaks or new DoS paths.

Deliverables:

- fixed-cardinality metrics, redacted/sampled security events, bounded queues,
  drop counters, and sink-health reporting;
- prohibition tests for usernames, full addresses, transaction IDs, nonces, and tokens as labels.

Verification:

- `cargo test -p gjallarbru-runtime observability`
- cardinality, sink failure, blocking, redaction, and log-injection tests

Exit criteria:

- Telemetry failure cannot block forwarding or disclose credential/path secrets.
- Stop: `v0.62.0 implementation stop reached. Run pentest for this exact commit.`

### v0.63.0 - Configuration Model

Goal: validate all startup and reload policy before opening public listeners.

Deliverables:

- bounded configuration schema for listeners, relays, realms, credentials, quotas,
  destinations, secure transports, admin, and logging;
- duplicate/unknown/conflicting/unsafe defaults, secret indirection, and immutable snapshots.

Verification:

- `cargo test -p gjallarbru-server configuration`
- malformed, oversized, ambiguous, insecure, and reload-diff fixtures

Exit criteria:

- Invalid configuration causes a clear startup/reload rejection with no partial activation.
- Stop: `v0.63.0 implementation stop reached. Run pentest for this exact commit.`

### v0.64.0 - Administrative Control Plane

Goal: provide bounded authenticated operations outside public TURN listeners.

Deliverables:

- local Unix/private-network transport abstraction, role/capability checks, request limits,
  health/capacity/drain/reload/rotate/revoke/close/redacted-diagnostics commands;
- worker messages using immutable generations rather than direct memory mutation.

Verification:

- `cargo test -p gjallarbru-server administration`
- unauthorized, replay, malformed, oversized, slow-client, and audit tests

Exit criteria:

- Administration cannot bypass core authorization or expose mutable worker state.
- Stop: `v0.64.0 implementation stop reached. Run pentest for this exact commit.`

### v0.64.1 - Tenant and Realm Isolation

Goal: make tenant and realm labels enforceable security boundaries before an
application-specific credential issuer depends on them.

Deliverables:

- deterministic unauthenticated realm selection from listener, destination address,
  secure SNI, and configured default, with ambiguity and spoof rejection;
- separate credential, nonce, REST, reservation, mobility, certificate, destination-
  policy, quota, allocation-index, metric, and audit domains per tenant and realm;
- lifecycle operations for create, rotate, suspend, emergency revoke, drain, delete,
  tombstone, and durable usage settlement without cross-tenant state reuse.

Verification:

- cross-product tests over listener/destination/SNI/REALM and attempts to use credentials,
  nonces, tickets, allocations, relay addresses, or policies across tenants
- concurrent deletion/rotation/reload, stale-worker, cache, durable-accounting,
  certificate, and secret-isolation fault injection

Exit criteria:

- No request can select or observe another tenant's authority or state, and emergency
  revocation reaches affected allocations and caches within a tested bound.
- Stop: `v0.64.1 implementation stop reached. Run pentest for this exact commit.`

### v0.65.0 - Graceful Drain and Shutdown

Goal: stop safely without creating new authority or leaking live resources.

Deliverables:

- running/draining/forced-stop states, new-allocation policy, existing allocation expiry,
  deadline handling, command flush, and socket/key cleanup;
- restart and health/readiness semantics.

Verification:

- `cargo test -p gjallarbru-runtime drain`
- live allocation, pending open/lookup, slow stream, deadline, and restart tests

Exit criteria:

- Drain is deterministic and forced shutdown leaves no persisted accidental authority.
- Stop: `v0.65.0 implementation stop reached. Run pentest for this exact commit.`

### v0.66.0 - Process Hardening

Goal: reduce runtime privilege and local attack surface after startup.

Deliverables:

- dedicated identity, capability drop, descriptor limits, dump policy, filesystem/network
  restrictions, syscall sandbox profile, secret-file handling, and failure-to-harden policy;
- platform-specific hardening evidence and explicit unsupported controls.

Verification:

- hardened deployment smoke tests and negative filesystem/syscall/network probes
- `cargo test -p gjallarbru-server hardening`

Exit criteria:

- Production mode refuses required hardening failures and documents residual platform gaps.
- Stop: `v0.66.0 implementation stop reached. Run pentest for this exact commit.`

### v0.66.1 - Panic Blast-Radius Containment

Goal: retain release-profile `panic = "abort"` while preventing one unexpected
worker or provider panic from indefinitely removing the complete service.

Deliverables:

- explicit process-wide abort threat analysis and a supervised multi-worker process
  model with generation identity, readiness, restart rate, backoff, and crash-loop limits;
- bounded, redacted panic/crash evidence with secret-bearing core dumps disabled and no
  attempt to use `catch_unwind` as isolation in an aborting release build;
- listener/relay ownership, port-pool partition, stale-generation fencing, allocation-loss,
  client recovery, and platform/service-manager responsibilities after worker death;
- documented single-process development limitation and production minimum redundancy for
  native, container, cluster, and future Aesynx deployment profiles.

Verification:

- test-only dependency/provider and first-party panic injection in release-profile workers,
  proving process abort, supervisor detection, cleanup/fencing, and restart within the SLO
- repeated crash, simultaneous worker crash, crash loop, supervisor death, partial startup,
  secret/core-dump inspection, stale socket/completion, and healthy-worker continuity tests
- Linux, Windows, BSD, macOS, container, service-manager, and cluster fault-injection matrix
  with explicit capability exclusions where a platform cannot provide a claimed control

Exit criteria:

- An unexpected panic has a measured process-level blast radius, cannot preserve stale
  TURN authority or expose secrets, and service capacity recovers within its published SLO.
- Stop: `v0.66.1 implementation stop reached. Run pentest for this exact commit.`

### v0.67.0 - Portable Desktop and Server Runtimes

Goal: verify the safe backend on Linux, Windows, BSD, and macOS.

Deliverables:

- platform socket/event/service adapters, local-address/path identity, IPv4/IPv6,
  error normalization, secure randomness/time, and shutdown behavior;
- shared conformance suite with platform capability matrix.

Verification:

- platform CI/maintained-host commands for Linux, Windows, FreeBSD, and macOS
- common Binding/allocation/relay integration suite

Exit criteria:

- Each advertised platform has behavioral evidence, not only a cross-compile.
- Stop: `v0.67.0 implementation stop reached. Run pentest for this exact commit.`

### v0.68.0 - Android and iOS Embedding

Goal: support mobile embedding without assuming daemon or privileged-server facilities.

Deliverables:

- NDK/Apple targets, embedding lifecycle API, suspend/resume/network-change events,
  bounded background behavior, and host-provided key/config/log adapters;
- unsupported long-running server capability documentation where platform policy restricts it.

Verification:

- Android/iOS build and simulator/device integration commands
- lifecycle, network migration, resource pressure, and shutdown tests

Exit criteria:

- Mobile support claims distinguish embeddable protocol/runtime behavior from OS service policy.
- Stop: `v0.68.0 implementation stop reached. Run pentest for this exact commit.`

### v0.69.0 - Aesynx Readiness Contract

Goal: prove core operation needs only explicit fixed-capacity platform services.

Deliverables:

- fixed storage implementation and traits for time, wall time, randomness, packet I/O,
  relay handles, credentials, audit, and configuration generations;
- compile-only/mock Aesynx adapter with no `std`, OS socket, thread, or ambient allocator dependency.

Verification:

- `cargo test -p gjallarbru-core --no-default-features fixed_storage`
- Aesynx-shaped mock integration and no_std target checks

Exit criteria:

- Future Aesynx integration requires adapters, not redesign of protocol authority.
- Stop: `v0.69.0 implementation stop reached. Run pentest for this exact commit.`

### v0.70.0 - Security-Reviewed UDP Server

Goal: harden the complete UDP server before adding more transports and acceleration.

Deliverables:

- full threat-model/control review, overload/soak/fault/incident/recovery exercises,
  dependency/unsafe/platform audit, capacity guide, and external security assessment;
- regression tests and remediation register for every finding.

Verification:

- full UDP conformance/interoperability/load suite
- `scripts/release_0_70_gate.sh`

Exit criteria:

- No unresolved critical/high finding or unbounded UDP resource remains.
- Stop: `v0.70.0 implementation stop reached. Run pentest for this exact commit.`

## Phase F: Secure Client Transports and Performance

### v0.71.0 - TURN over TCP

Goal: carry the existing protocol authority over connection-oriented client paths.

Deliverables:

- accepted connection generations, incremental framing, path identity, command writes,
  disconnect cleanup, and reliable-transport transaction behavior;
- no allocation migration between connections with reused endpoints.

Verification:

- `cargo test -p gjallarbru-runtime turn_tcp`
- fragmented/coalesced frames, reconnect reuse, and real TCP interoperability tests

Exit criteria:

- A TCP connection can affect only allocations created on that exact generation.
- Stop: `v0.71.0 implementation stop reached. Run pentest for this exact commit.`

### v0.72.0 - Stream Backpressure

Goal: keep slow TCP/TLS clients from consuming unbounded memory or work.

Deliverables:

- queued frame/byte/age limits, partial-frame ceilings, read suspension, fair writes,
  hard-close thresholds, and peer-data drop policy;
- allocation/global accounting of queued bytes and leased buffers.

Verification:

- `cargo test -p gjallarbru-runtime stream_backpressure`
- slow-reader, no-reader, partial-frame, fairness, and sustained-peer-load tests

Exit criteria:

- Every stream retains bounded memory and terminates stalled work deterministically.
- Stop: `v0.72.0 implementation stop reached. Run pentest for this exact commit.`

### v0.73.0 - TLS Provider Adapter

Goal: integrate TLS without placing certificate or record logic in core.

Deliverables:

- reviewed provider dependency/feature/license/MSRV decision and plaintext connection adapter;
- certificate/key loading, handshake/result normalization, session cleanup, and provider substitution tests.

Verification:

- `cargo test -p gjallarbru-runtime tls_adapter`
- two-provider or provider/test-double differential framing tests where practical

Exit criteria:

- Core receives provider-validated decrypted transport data with no TLS implementation
  type; TURN authentication remains authoritative for client identity unless a separate,
  explicit mTLS profile is configured.
- Stop: `v0.73.0 implementation stop reached. Run pentest for this exact commit.`

### v0.74.0 - Hardened TLS Deployment

Goal: apply current BCP 195 policy and bound all TLS work.

Deliverables:

- TLS version/cipher/certificate policy, handshake prefix/global quotas, timeout,
  chain/record limits, resumption/ticket rotation, key-log/dump policy, and reload;
- interoperability profile for required legacy exceptions.

Verification:

- TLS scanner/interoperability suite plus handshake-flood and malformed-record tests
- `cargo deny --locked check` and provider advisory review

Exit criteria:

- Weak or over-budget TLS behavior is rejected explicitly and configuration is auditable.
- Stop: `v0.74.0 implementation stop reached. Run pentest for this exact commit.`

### v0.74.1 - TLS Identity and Termination

Goal: bind TLS server identity and external termination metadata to the correct
listener, realm, tenant, and path without treating TLS as TURN client authentication.

Deliverables:

- RFC 7443 `stun.turn` ALPN, SNI/certificate selection, listener/destination/SNI-
  to-realm mapping, certificate-name rules, reload, and mismatch rejection;
- direct TLS and explicitly trusted termination topologies with authenticated PROXY
  protocol, bounded headers, peer allowlists, rotation, and source-data provenance;
- TLS 1.2/1.3 policy and port-443 deployment choices that preserve five-tuple identity
  and never accept identity metadata from an untrusted peer.

Verification:

- Chromium/native certificate-name and ALPN interoperability; absent/wrong SNI,
  certificate rotation, realm ambiguity, TLS 1.2/1.3, and resumption tests
- direct, spoofed, truncated, and oversized PROXY inputs; trusted-proxy rotation,
  source preservation, passthrough/termination, and port-443 topology tests

Exit criteria:

- Provider-authenticated server transport terminates in the intended realm, TURN still
  authenticates the client, and untrusted metadata can never set source identity.
- Stop: `v0.74.1 implementation stop reached. Run pentest for this exact commit.`

### v0.75.0 - DTLS Provider Adapter

Goal: carry TURN over DTLS while preserving datagram and path semantics.

Deliverables:

- reviewed DTLS provider boundary, session IDs/generations, plaintext datagrams,
  retransmission/timer events, replay handling, and cleanup;
- migration/rebinding policy distinct from RFC 8016 mobility.

Verification:

- `cargo test -p gjallarbru-runtime dtls_adapter`
- RFC 7350 interoperability, loss/reorder/replay, and session-reuse tests

Exit criteria:

- DTLS sessions cannot inherit stale allocations or bypass client-path identity.
- Stop: `v0.75.0 implementation stop reached. Run pentest for this exact commit.`

### v0.76.0 - DTLS Anti-Abuse

Goal: prevent spoofed handshakes and retransmissions from becoming amplification/CPU attacks.

Deliverables:

- cookie/anti-amplification policy, per-prefix/global handshake and byte ceilings,
  timeouts, flight/retransmit limits, buffer accounting, and provider failure isolation;
- no allocation or credential lookup before required reachability gates.

Verification:

- handshake flood, spoofed source, loss, oversized certificate/record, and timeout tests
- response/request amplification report

Exit criteria:

- Unverified DTLS sources cannot cause unbounded memory, crypto, or amplified output.
- Stop: `v0.76.0 implementation stop reached. Run pentest for this exact commit.`

### v0.76.1 - DTLS 1.3 Policy

Goal: give RFC 9147 DTLS 1.3 an explicit provider/deployment disposition while
retaining required RFC 7350 DTLS 1.2 interoperability.

Deliverables:

- reviewed DTLS 1.2/1.3 and TLS 1.2/1.3 matrix, provider capability contract,
  cipher/certificate/resumption policy, downgrade boundary, and release criteria;
- DTLS 1.3 connection-ID, anti-replay, cookie, retransmission, key-update, migration,
  and exporter applicability decisions mapped to TURN path identity;
- explicit errors when a provider/platform cannot satisfy its selected version profile.

Verification:

- independent DTLS 1.2/1.3 interoperability where declared, plus downgrade, replay,
  loss, reorder, key-update, rebinding, resumption, and fallback tests
- provider substitution, platform matrix, BCP scan, amplification report, and reviewed
  exclusions for unavailable capabilities

Exit criteria:

- Every advertised secure transport version has provider evidence, and negotiation
  cannot weaken path identity, replay defense, or operator policy.
- Stop: `v0.76.1 implementation stop reached. Run pentest for this exact commit.`

### v0.77.0 - Standard Shared-Port Demultiplexing

Goal: implement standardized first-byte demux without inventing TURN-over-QUIC.

Deliverables:

- RFC 7983 and RFC 9443 range table, STUN/ChannelData/DTLS/QUIC classification,
  ambiguous/invalid handling, and configuration collision checks;
- docs explicitly separating shared port from transport encapsulation.

Verification:

- `cargo test -p gjallarbru-wire shared_port`
- exhaustive 256 first-byte classification plus integration fixtures

Exit criteria:

- Shared listeners route only standardized ranges and make no proprietary TURN claim.
- Stop: `v0.77.0 implementation stop reached. Run pentest for this exact commit.`

### v0.78.0 - Per-Core Ownership

Goal: remove global allocation locks while retaining one authoritative owner per flow.

Deliverables:

- worker-local stores/timers/buffers/relays, stable flow steering, bounded cross-worker control,
  immutable configuration epochs, and ownership migration prohibition;
- safe single-worker reference retained for differential tests.

Verification:

- `cargo test -p gjallarbru-runtime worker_ownership`
- concurrency/model tests proving no normal global allocation mutex or cross-worker relay path

Exit criteria:

- Every client path and relay completion reaches exactly one owning worker.
- Stop: `v0.78.0 implementation stop reached. Run pentest for this exact commit.`

### v0.79.0 - Batched I/O

Goal: improve throughput with bounded batching without changing protocol results.

Deliverables:

- portable batch abstraction plus Linux `recvmmsg`/`sendmmsg`, fairness budget,
  partial-send/error handling, and worker-local registries;
- benchmarks against safe one-packet reference behavior.

Verification:

- differential packet/result suite and batch-size fairness/load benchmarks
- syscall/error fault injection

Exit criteria:

- Batching measurably improves target workloads and never changes authorization decisions.
- Stop: `v0.79.0 implementation stop reached. Run pentest for this exact commit.`

### v0.80.0 - Buffer Pools and Scatter/Gather

Goal: prove zero allocator calls and avoid unnecessary payload copies on the hot path.

Deliverables:

- fixed buffer classes, leases/generations, headroom/tailroom, scatter packet plans,
  output padding segments, exhaustion/drop policy, and allocator instrumentation;
- sanitization policy for buffers that may carry credential material.

Verification:

- `cargo test -p gjallarbru-runtime buffer_pool`
- allocation-count, copy-count, leak, reuse, short-iovec, and exhaustion benchmarks/tests

Exit criteria:

- Claimed packet paths allocate nothing after startup and never reuse a live lease.
- Stop: `v0.80.0 implementation stop reached. Run pentest for this exact commit.`

### v0.81.0 - `io_uring` Backend

Goal: add measured Linux `io_uring` acceleration behind the unchanged runtime contract.

Deliverables:

- fixed files/buffers, multishot capability detection, bounded in-flight operations,
  generation-tagged user data, cancellation, shutdown, and portable fallback;
- isolated unsafe/syscall modules with safety evidence.

Verification:

- differential portable/batched/`io_uring` suite, Miri-safe helpers, sanitizers,
  stale completion, cancellation, unsupported-kernel, and overload tests

Exit criteria:

- Disabling `io_uring` changes performance only and unsafe invariants are reviewed.
- Stop: `v0.81.0 implementation stop reached. Run pentest for this exact commit.`

### v0.82.0 - Optional eBPF and AF_XDP Fast Path

Goal: accelerate only traffic already authorized by live core state.

Deliverables:

- ingress filtering/steering and optional rules containing allocation generation,
  endpoints, direction, channel, expiry, policy epoch, and byte/packet budgets;
- install/remove ordering, map-capacity, fail-closed miss, and reconciliation checks.

Verification:

- core-rule subset property, stale/expired/epoch mismatch tests, XDP-disabled differential suite,
  verifier/load/eviction tests, and performance report

Exit criteria:

- Kernel rules cannot create, refresh, broaden, or outlive core authorization.
- Stop: `v0.82.0 implementation stop reached. Run pentest for this exact commit.`

## Phase G: Extended TURN Profiles and Assurance Foundations

### v0.83.0 - RFC 6062 State Model

Goal: define TCP relay semantics as a deterministic sans-I/O state machine before
opening TCP relay sockets.

Deliverables:

- bounded TCP allocation, pending-connection, connection-identifier, binding,
  expiry, and generation state;
- abstract `CONNECT`, `CONNECTION-ATTEMPT`, and `CONNECTION-BIND` events and
  commands, including duplicate and timeout behavior.

Verification:

- reference-model and arbitrary-event-sequence tests for all TCP relay states
- stale generation, identifier collision, timeout, capacity, and duplicate tests

Exit criteria:

- Every RFC 6062 transition is representable without socket side effects and all
  invalid transitions fail closed.
- Stop: `v0.83.0 implementation stop reached. Run pentest for this exact commit.`

### v0.84.0 - TCP Relay Allocation and Listener

Goal: allocate a bounded TCP relay listener through the same two-phase core/runtime
contract used by UDP relay resources.

Deliverables:

- requested TCP transport validation, TCP relay-port allocation, listener
  ownership, expiry, and close commands;
- portable runtime listen/accept integration with explicit bind failure and
  rollback behavior.

Verification:

- synthetic and real-loopback allocation, bind-failure, expiry, and shutdown tests
- differential core/runtime resource-ownership and leak checks

Exit criteria:

- A TCP allocation owns exactly one accounted listener or no listener, including
  every failure, timeout, and shutdown path.
- Stop: `v0.84.0 implementation stop reached. Run pentest for this exact commit.`

### v0.85.0 - Outbound CONNECT

Goal: implement authenticated, policy-bound outbound peer connections for TCP
allocations.

Deliverables:

- exact peer-permission and policy checks, pending-connect state, bounded timeout,
  quota accounting, duplicate handling, and connection identifiers;
- runtime connect completion/failure events that cannot outlive their allocation
  generation.

Verification:

- success, refusal, timeout, duplicate, stale-completion, policy-denial, and quota tests
- real-loopback interoperability and synthetic fault-injection tests

Exit criteria:

- CONNECT cannot reach an unauthorized peer, bypass a limit, duplicate a connection,
  or leak state after failure.
- Stop: `v0.85.0 implementation stop reached. Run pentest for this exact commit.`

### v0.86.0 - Incoming Connections and CONNECTION-BIND

Goal: accept peer-initiated TCP connections only through authenticated ownership
and binding transitions.

Deliverables:

- bounded incoming-connection state and `CONNECTION-ATTEMPT` indications;
- authenticated `CONNECTION-BIND` processing with allocation ownership, path
  generation, identifier, replay, timeout, and cleanup checks.

Verification:

- model tests for accept, indication, bind, duplicate, wrong owner, stale path, and expiry
- loopback client interoperability and reordered-event tests

Exit criteria:

- No accepted connection carries application data until a valid owner binds it,
  and every unbound connection expires within its configured bound.
- Stop: `v0.86.0 implementation stop reached. Run pentest for this exact commit.`

### v0.87.0 - TCP Relay Buffering and Backpressure

Goal: relay TCP data with explicit memory, time, and fairness bounds under slow or
absent readers.

Deliverables:

- per-direction queues, pre-bind byte/time caps, partial-write handling, fair
  scheduling, close policy, and allocation-level quotas;
- deterministic backpressure and cleanup behavior for disconnects and half-closes.

Verification:

- slow-reader, absent-bind, partial-write, half-close, queue-exhaustion, and fairness tests
- memory-accounting properties and sustained overload tests

Exit criteria:

- An adversarial connection cannot create unbounded buffering, starve another
  allocation, or retain data after ownership ends.
- Stop: `v0.87.0 implementation stop reached. Run pentest for this exact commit.`

### v0.88.0 - `turn-tcp-relay` Conformance

Goal: close the declared RFC 6062 profile with complete evidence rather than a
feature-presence claim.

Deliverables:

- reviewed RFC 6062 requirement and errata matrix, interoperability corpus, fuzz
  targets, and TCP relay threat-model update;
- release notes and operator guidance for TCP relay capacity and failure behavior.

Verification:

- all RFC 6062 vectors, negative cases, fuzz targets, interoperability scenarios,
  MSRV jobs, and the versioned release gate
- adversarial connection-lifecycle and resource-exhaustion suite

Exit criteria:

- Every in-scope RFC 6062 requirement is `verified`, every exclusion is explicit,
  and the exact release candidate passes the TCP relay pentest.
- Stop: `v0.88.0 implementation stop reached. Run pentest for this exact commit.`

### v0.89.0 - RFC 7635 Third-Party Authorization

Goal: add cryptographically scoped third-party authorization without weakening
the long-term credential profiles.

Deliverables:

- bounded token parsing and provider interfaces for key identifiers, audience,
  server identity, lifetime, session keys, replay policy, and key rotation;
- explicit profile selection and failure mapping that prevents cross-profile fallback.

Verification:

- RFC/project vectors, malformed-token fuzzing, expiry, audience, replay, rotation,
  unknown-key, and downgrade tests
- integration tests with an independent authorization service fixture

Exit criteria:

- A token authorizes only its intended server, identity, scope, and lifetime, and
  token failures cannot fall back to a weaker credential mode.
- Stop: `v0.89.0 implementation stop reached. Run pentest for this exact commit.`

### v0.90.0 - RFC 8016 Mobility

Goal: allow an allocation to survive an authorized client path change without
creating a replay or allocation-theft primitive.

Deliverables:

- protected mobility tickets, old/new path transitions, bounded overlap, replay
  detection, identity/policy binding, and sharding ownership rules;
- deterministic migration cleanup and failure behavior.

Verification:

- state-model, NAT-rebinding, cross-worker, replay, theft, expiry, rollback, and
  key-rotation tests
- mobile-network interoperability scenarios with controlled path changes

Exit criteria:

- Only the authenticated allocation owner can migrate an allocation, and old paths
  lose authority within the documented overlap bound.
- Stop: `v0.90.0 implementation stop reached. Run pentest for this exact commit.`

### v0.91.0 - REST Shared-Secret Compatibility Profile

Goal: support the deployed time-limited shared-secret credential convention as an
explicit compatibility profile.

Deliverables:

- byte-exact time-scoped usernames and shared-secret derivation, bounded clock
  skew, secret rotation, replay controls, quotas, and a distinct configuration label;
- documentation that separates this de-facto profile from standards-track authentication.

Verification:

- known client/server vectors, expiry, skew, parsing, rotation, replay, abuse, and
  cross-profile confusion tests
- interoperability with commonly deployed TURN clients

Exit criteria:

- Compatibility credentials are time-, realm-, and policy-bounded and cannot be
  confused with another authentication profile.
- Stop: `v0.91.0 implementation stop reached. Run pentest for this exact commit.`

### v0.91.1 - Pawalyze Ephemeral Credential Issuance

Goal: issue browser-visible TURN credentials that are short-lived, authenticated,
application-bound, and safe to rotate without exposing a reusable password.

Deliverables:

- an authenticated issuance contract binding Pawalyze user, tenant, realm, purpose,
  audience, issue time, expiry, quota class, and nonce to a scoped TURN username;
- OpenBao-backed shared-secret generations with atomic rotation, bounded overlap,
  emergency revocation, stale-node rejection, audit events, and least privilege;
- TTL/call-duration/allocation-refresh rules, renewal, per-user allocation/bandwidth/rate
  quotas, and cryptographic prevention of use by another application;
- Pawalyze migration guidance removing permanent browser-visible TURN passwords while
  keeping signaling and WebRTC end-to-end encryption outside TURN authority.

Verification:

- issuer authentication, tamper, replay, user/tenant/realm/purpose/audience confusion,
  expiry/skew, renewal, maximum-call, rotation/overlap/revoke, and outage tests
- OpenBao compromise drills and browser/API inspection proving no long-lived TURN secret
  reaches configuration, logs, storage, JavaScript, or telemetry

Exit criteria:

- A captured credential is useful only for its bounded Pawalyze identity, realm,
  purpose, quota, and lifetime, and revocation has a measured completion bound.
- Stop: `v0.91.1 implementation stop reached. Run pentest for this exact commit.`

### v0.92.0 - RFC 5780 Diagnostic Profile

Goal: provide NAT behavior discovery only as an isolated, explicitly enabled
diagnostic profile.

Deliverables:

- alternate-address listener topology, response-origin/other-address behavior,
  change-request processing, topology validation, and separate quotas;
- secure defaults that leave the profile disabled when the required topology is absent.

Verification:

- RFC 5780 conformance cases, simulated NAT mappings/filtering, topology mismatch,
  reflection, quota, and disabled-profile tests
- multi-address integration tests on supported platforms

Exit criteria:

- The profile cannot be enabled with an invalid topology or enlarge amplification
  beyond its documented and tested limits.
- Stop: `v0.92.0 implementation stop reached. Run pentest for this exact commit.`

### v0.93.0 - Formal and Static Assurance

Goal: mechanically exercise the highest-risk state, memory, concurrency, and
platform invariants.

Deliverables:

- Kani harnesses for cursors, slabs, timers, and protocol transitions; Miri coverage
  for buffers; Loom models for queues/config publication; runtime sanitizer jobs;
- reviewed inventory mapping every unsafe block and security invariant to evidence.

Verification:

- all Kani, Miri, Loom, address/undefined/thread sanitizer, clippy, and unsafe-policy gates
- mutation or fault-injection checks proving the assurance gates detect representative faults

Exit criteria:

- Every safety-critical invariant has an executable check or a documented reviewed
  proof obligation, with no unexplained unsafe code.
- Stop: `v0.93.0 implementation stop reached. Run pentest for this exact commit.`

### v0.94.0 - Long-Duration Fuzz and Soak Closure

Goal: demonstrate stable behavior under sustained malformed input, churn,
overload, packet loss, and injected failures.

Deliverables:

- release fuzz corpus and budgets for every parser and state machine;
- reproducible soak scenarios covering allocation churn, timer wrap, overload,
  transport failures, reloads, and graceful shutdown.

Verification:

- documented long-duration fuzz campaigns and multi-day soak runs on production-like limits
- memory/descriptor growth, latency, fairness, crash, and invariant reports with replay seeds

Exit criteria:

- No unresolved crash, leak, unbounded growth, invariant violation, or security-relevant
  timeout remains from the release campaigns.
- Stop: `v0.94.0 implementation stop reached. Run pentest for this exact commit.`

### v0.95.0 - Platform and Interoperability Closure

Goal: verify the declared operating-system, transport, address-family, and client
support matrix before production release.

Deliverables:

- evidence for Linux, Windows, FreeBSD, macOS, Android, and iOS, plus a reviewed
  Aesynx portability-readiness report;
- cross-client, IPv4/IPv6, UDP/TCP/TLS/DTLS, NAT, loss, upgrade, and fallback matrix.

Verification:

- native CI/device-lab results and independent client/server interoperability runs
- differential behavior checks across supported runtime backends and platforms

Exit criteria:

- Every advertised matrix cell passes or is explicitly removed from the declared
  support profile before the release stop.
- Stop: `v0.95.0 implementation stop reached. Run pentest for this exact commit.`

## Phase H: Distributed Production Deployment

### v0.96.0 - Multi-Node Failure Contract

Goal: define an honest highly available service model without pretending a live
TURN allocation can be transferred like an HTTP request.

Deliverables:

- explicit node-local allocation, permission, channel, transaction, relay-socket, and
  timer ownership; no synchronous data-plane state replication in the initial profile;
- node health and drain states, failure detection, active-call impact, recovery SLO,
  readiness semantics, and Pawalyze ICE-restart contract against a surviving node;
- reviewed future state-transfer admission criteria that cannot weaken five-tuple,
  credential, permission, replay, port, or packet-ordering authority.

Verification:

- hard kill, process crash, host loss, network partition, delayed health, drain deadline,
  and simultaneous node-loss scenarios with active allocations
- measured detection-to-new-allocation and Pawalyze ICE-restart recovery times, including
  clear evidence that failed-node allocations and relay ports never remain authoritative

Exit criteria:

- Node loss terminates its node-local allocations, another healthy node accepts fresh
  allocations, and Pawalyze recovery meets the published SLO without state ambiguity.
- Stop: `v0.96.0 implementation stop reached. Run pentest for this exact commit.`

### v0.96.1 - Secure Cluster Protocol

Goal: let two or more Gjallarbru nodes understand one another through a private,
bounded control protocol without turning cluster traffic into data-plane authority.

Deliverables:

- first-party length-delimited protocol with cluster/node identity, protocol version,
  capability negotiation, monotonically increasing generation, sequence, and replay rules;
- internal EUPL-1.2 `gjallarbru-cluster` crate containing framing, secure-session,
  membership, health/load, and convergence modules behind narrow server interfaces;
- provider-backed mTLS with node certificate/name validation, cluster-ID binding, explicit
  trust roots, enrollment, rotation, revocation, and a separate non-public listener;
- bounded messages, queues, peers, handshakes, fan-out, retries, timeouts, backpressure,
  keepalives, diagnostics, and malformed/unknown-message behavior;
- narrowly typed messages for membership observations, health, capacity, drain, relay-pool
  lease generation, configuration digest, and key-generation identifiers—not relay media,
  allocation state, browser credentials, private key bytes, or client authorization.

Verification:

- two-node and multi-node handshake, version/capability, certificate rotation/revocation,
  wrong cluster/node, replay, reorder, duplicate, corruption, unknown message, and skew tests
- public-listener injection, untrusted certificate, stolen node identity, oversized frame,
  slow peer, reconnect storm, queue exhaustion, fan-out, and secret/payload leakage tests

Exit criteria:

- Only an authenticated member of the configured cluster can exchange bounded control
  state, and no cluster message can create or transfer a TURN allocation or relay packet.
- Stop: `v0.96.1 implementation stop reached. Run pentest for this exact commit.`

### v0.96.2 - Cluster Membership and Load Coordination

Goal: make a cluster of two or more nodes converge on useful membership, health, load,
capacity, and drain information while each node retains local allocation authority.

Deliverables:

- static bootstrap plus authenticated administrator-approved join/remove workflow; no
  unauthenticated Internet discovery or automatic trust-on-first-use;
- bounded membership views, heartbeat/suspicion/dead states, epochs, incarnation handling,
  convergence deadlines, tombstones, duplicate-node rejection, and restart semantics;
- aggregate node/region capacity signals for relay ports, allocations, packet rate,
  bandwidth, handshakes, queues, readiness, drain, and overload with freshness timestamps;
- read-only health/load export for DNS/L4 control and Fluxheim fixtures, with deterministic
  stale/partition behavior and no remote mutation of worker or allocation state.

Verification:

- 2-, 3-, and N-node join, leave, restart, rolling drain, scale out/in, overload, stale
  observation, clock skew, duplicate ID, delayed/lost messages, and convergence tests
- asymmetric partition, isolated node, reconnect storm, member churn, compromised peer,
  false load report, bounded-memory/fan-out, and recovery fault injection

Exit criteria:

- Healthy members converge within the published bound, stale/isolated members cannot be
  advertised as ready, and false cluster data cannot grant packet or allocation authority.
- Stop: `v0.96.2 implementation stop reached. Run pentest for this exact commit.`

### v0.97.0 - Traffic and Relay-Pool Distribution

Goal: route new allocations across nodes and regions while keeping each allocation
affine to exactly one authoritative node and relay-port pool.

Deliverables:

- DNS and L4 distribution profiles, health-aware admission, connection/datagram affinity,
  region selection, locality, fallback, TTL, and cache behavior;
- exclusive relay-address ownership and non-overlapping per-node port partitions with
  lease/fencing generations for replacement hosts;
- stale-node rejection, capacity-aware routing, failback policy, and an explicit boundary
  between discovery/load balancing and the node-local TURN state machine.

Verification:

- distribution, affinity, DNS TTL, L4 rebalance, region outage, stale cache, port collision,
  pool exhaustion, replacement-node, and failback tests
- packet captures and invariant checks proving one client/server five-tuple and relay
  endpoint cannot be concurrently authoritative on two nodes

Exit criteria:

- New work reaches a healthy owner, active work stays affine to its owner, and address/
  port leases prevent stale or split ownership throughout node and region changes.
- Stop: `v0.97.0 implementation stop reached. Run pentest for this exact commit.`

### v0.97.1 - Fluxheim Compatibility Profile

Goal: publish and continuously test the safe ways Gjallarbru can operate behind the
project's Fluxheim load balancer without overstating Fluxheim's current UDP capability.

Deliverables:

- pinned minimum/tested Fluxheim version and reproducible configuration for raw L4
  TURN/TCP plus TURN/TLS passthrough on 443 using stream routes and upstream PROXY v2;
- Gjallarbru trusted-proxy allowlist, pre-TLS PROXY parsing, realm/listener mapping,
  connection affinity, health/readiness, drain, timeout, byte-limit, and failure policy;
- hybrid production topology where Fluxheim balances TCP/TLS connections while TURN/UDP
  and UDP relay ranges reach Gjallarbru directly through the qualified public topology;
- explicit incompatibility statement for Fluxheim's current DNS-style/syslog UDP beta;
  full TURN/UDP proxying remains disabled unless a later Fluxheim version proves generic
  UDP five-tuple affinity, real-source identity, relay-range handling, and production load;
- operator guide, example configs, diagrams, version matrix, troubleshooting, and a
  cross-project integration runner that never imports Fluxheim protocol authority.

Verification:

- black-box Binding, Allocate, Refresh, permission, channel, bidirectional relay, long
  TCP/TLS connection, TLS certificate/ALPN, port 443, PROXY v2, health, drain, and failover
- spoofed/untrusted/malformed PROXY, wrong realm, source-IP preservation, connection
  rebalance, backend loss, timeout mismatch, slow stream, overload, and mixed-version tests
- prove UDP takes the documented direct path and the unsupported Fluxheim UDP mode is
  rejected; add the full UDP matrix only when its stated capability gate becomes true

Exit criteria:

- The tested hybrid profile preserves TURN identity and connection ownership, documentation
  matches the pinned Fluxheim release, and no operator can mistake beta UDP for support.
- Stop: `v0.97.1 implementation stop reached. Run pentest for this exact commit.`

### v0.98.0 - Coordinated Rolling Upgrades

Goal: upgrade and fail over a fleet without mixed-version ambiguity, stale authority,
or synchronized secret and certificate failure.

Deliverables:

- adjacent-version compatibility policy, feature/config capability negotiation, ordered
  drain/update/rollback, canary, schema floor, and downgrade restrictions;
- distributed certificate, nonce, REST, mobility, reservation, and administrative key
  generations with staged activation, overlap ceilings, revocation, and audit evidence;
- control-plane quorum/lease fencing, clock-skew policy, stale-node eviction, region
  isolation, split-brain prevention, and disaster-recovery bootstrap.

Verification:

- every supported adjacent-version pair under active traffic, rolling upgrade/rollback,
  partial deployment, old config, clock skew, delayed key, and certificate rotation tests
- partitions, lost quorum, stale snapshots, duplicate node identity, split brain, region
  failover/failback, and compromised-key emergency drills

Exit criteria:

- A mixed fleet exposes only its negotiated safe intersection, stale nodes cannot mint or
  accept current authority, and upgrades/rollback meet published interruption bounds.
- Stop: `v0.98.0 implementation stop reached. Run pentest for this exact commit.`

### v0.99.0 - Rootless Network Qualification

Goal: define exactly which rootless container topologies can preserve TURN identity,
publish relay ports, sustain UDP load, and provide TLS on port 443.

Deliverables:

- minimum supported Docker, RootlessKit, Podman, netavark, and pasta versions/modes,
  with a source-address/five-tuple preservation capability matrix;
- bind-versus-advertised mapping and complete UDP/TCP relay-range publication rules,
  host firewall examples, one-to-one NAT, multi-home, and public-IP prerequisites;
- documented 443 choices: host unprivileged-port sysctl, source-preserving host forward,
  direct high port, or authenticated trusted termination; no hidden capability promise;
- startup topology probe and configuration validation that rejects modes unable to
  preserve required identity or inbound relay reachability.

Verification:

- real-source-IP/five-tuple packet captures and Allocate/permission/channel relay tests
  under every supported Docker and Podman networking mode
- full relay-range reachability, UDP/TCP, public mapping, 443, IPv4/IPv6, restart, and
  native-versus-container throughput/latency/loss comparison at production load

Exit criteria:

- Every documented rootless topology preserves authoritative identity and meets its
  performance floor; unsupported topologies are detected and rejected, not guessed.
- Stop: `v0.99.0 implementation stop reached. Run pentest for this exact commit.`

### v0.100.0 - Rootless Wolfi Container

Goal: ship the complete server in a signed minimal image using only the rootless
network topologies proven by v0.99.0.

Deliverables:

- digest-pinned Wolfi/apko multi-architecture image with no compiler, package manager,
  or shell; fixed non-zero UID/GID, direct entrypoint, read-only root, and explicit writes;
- Docker/Podman and Compose examples for each qualified network/443 profile, complete
  listener/relay-range publication, health/readiness, signals, and resource limits;
- dropped capabilities, `no-new-privileges`, immutable config/secret mounts, OCI labels,
  per-platform SBOM, provenance, signature, digest, and rebuild/update policy.

Verification:

- inspect and run `linux/amd64` and `linux/arm64` under qualified rootless Docker/Podman
  with read-only root, no added capability, bounded CPU/memory/PIDs, and no hidden download
- black-box Binding, authenticated Allocate, permission, channel, bidirectional UDP/TCP
  relay, TLS/443 profile, full port range, source identity, health, restart, and shutdown
- malformed config, missing secret, port conflict, unqualified topology rejection,
  vulnerability scan, signature, SBOM, provenance, and update tests

Exit criteria:

- The signed image provides a full TURN server in every documented qualified rootless
  profile, while the docs clearly state host/network prerequisites and non-portable cases.
- Stop: `v0.100.0 implementation stop reached. Run pentest for this exact commit.`

### v0.100.1 - Rootless Debian Container

Goal: offer a familiar, customizable Debian alternative without weakening Gjallarbru's
network qualification, non-root default, artifact integrity, or support clarity.

Deliverables:

- digest-pinned Debian stable-slim multi-architecture image using the identical reviewed
  Gjallarbru binary, configuration schema, entrypoint contract, and network profiles;
- fixed non-zero default UID/GID, rootless Docker/Podman examples, complete listener/relay
  publication, health/readiness, signals, resource limits, and read-only-root example;
- retained Debian package-management/customization path, documented derived-image examples,
  package pin/update policy, writable-root opt-in, and clear Wolfi-versus-Debian tradeoffs;
- separate SBOM, provenance, signature, immutable digest, vulnerability policy, rebuild
  cadence, package allowlist, and support/version matrix for each architecture.

Verification:

- build/inspect/run Debian `linux/amd64` and `linux/arm64` under every qualified rootless
  topology and repeat the complete Wolfi black-box protocol/source/relay/443 smoke suite
- differential output/config/upgrade/signal/health/performance tests between native,
  Wolfi, and Debian images using the same Gjallarbru release
- non-root/read-only and explicitly documented customizable/writable derived-image tests,
  apt/package pinning, vulnerability, SBOM, provenance, signature, and offline-start checks

Exit criteria:

- Operators can choose hardened-minimal Wolfi or customizable Debian with identical TURN
  behavior, explicit security tradeoffs, and no unqualified network or privilege claim.
- Stop: `v0.100.1 implementation stop reached. Run pentest for this exact commit.`

### v0.101.0 - Pawalyze Integration Closure

Goal: prove real one-to-one Pawalyze browser calls recover across hostile networks and
node failure using only short-lived, purpose-bound TURN credentials.

Deliverables:

- production Pawalyze issuer/client integration with relay-only privacy mode, credential
  renewal, maximum-call behavior, ICE restart, multi-node endpoints, and redacted telemetry;
- Chromium, Firefox, and Safari matrix across UDP, TCP, TLS/443, IPv4, IPv6, IPv6-only,
  NAT64, UDP-blocked, symmetric NAT, forced relay, network change, and TURN-node loss;
- tested credential non-reuse outside Pawalyze and per-user/tenant rate, allocation, and
  bandwidth enforcement through issuance, refresh, renewal, and node recovery;
- explicit scope statement: TURN supplies connectivity relay, not Pawalyze signaling,
  WebRTC media encryption, or an SFU; group calls require a separate media architecture.

Verification:

- automated browser/device lab calls for every matrix cell with packet, ICE-state,
  credential-lifetime, quota, privacy, and recovery-SLO assertions
- capture/replay against another app/tenant/realm, renewal race, long call, OpenBao
  rotation/outage, network handoff, node kill, region loss, and forced-relay pentests

Exit criteria:

- Every supported Pawalyze matrix cell completes or recovers within its SLO without a
  reusable browser secret, privacy downgrade, cross-purpose reuse, or silent direct path.
- Stop: `v0.101.0 implementation stop reached. Run pentest for this exact commit.`

### v0.102.0 - Production IP-Path Correctness

Goal: make modern IPv6, translation, multi-address, and path-MTU behavior correct
under real Internet and mobile access networks.

Deliverables:

- IPv6-only, NAT64, DNS64, and 464XLAT deployment profiles with explicit client,
  listener, relay-family, peer-family, and discovery behavior;
- multiple public relay-IP selection, health, deprecation, rotation, source-address,
  route, and return-path validation;
- PMTU policy, ICMPv4 fragmentation-needed and ICMPv6 Packet Too Big processing,
  DONT-FRAGMENT interaction, safe MTU floors, black-hole detection, and telemetry.

Verification:

- lab and carrier/device tests for IPv6-only, NAT64/464XLAT, dual-stack, asymmetric
  routing, address failover, MTU boundaries, PTB validation, loss, and PMTU black holes
- end-to-end WebRTC and native relays across every supported client/relay/peer family
  combination with packet-size, source-address, reachability, and recovery assertions

Exit criteria:

- Every declared IP path relays within safe MTU/address rules or fails explicitly, with
  no unvalidated control packet able to redirect, fragment, or corrupt another flow.
- Stop: `v0.102.0 implementation stop reached. Run pentest for this exact commit.`

### v0.103.0 - Network DDoS Containment

Goal: address attacks that exhaust upstream links or edge state before bounded server
memory and CPU controls can help.

Deliverables:

- provider/edge scrubbing and anycast/unicast topology, ACL/rate interface, attack-mode
  admission, authenticated-user prioritization, and regional isolation policy;
- link, packet-rate, flow, handshake, allocation, reflection, and egress anomaly signals
  with automatic thresholds, operator confirmation boundaries, and emergency controls;
- tested escalation contacts, traffic-shift/blackhole procedures, evidence capture,
  false-positive rollback, and Pawalyze degradation communication.

Verification:

- authorized isolated volumetric UDP/TCP/TLS, spoofed-source, reflection, handshake,
  distributed low-rate, and link-saturation exercises with provider or lab scrubbing
- prove controls preserve established authenticated traffic where budget permits, never
  bypass core authorization, and recover cleanly without stale edge or node policy

Exit criteria:

- Saturation is detected before the published exhaustion threshold, rehearsed edge action
  bounds blast radius, and residual provider/link limits are quantified and documented.
- Stop: `v0.103.0 implementation stop reached. Run pentest for this exact commit.`

### v0.104.0 - Capacity, Cost, and Autoscaling

Goal: make relay-port and bandwidth capacity, service objectives, and egress cost
measurable and forecastable before production admission.

Deliverables:

- workload model for concurrent calls, allocations, permissions, channels, relay ports,
  packet rates, TLS/DTLS handshakes, bandwidth, regional headroom, and egress price;
- exhaustion forecasts and admission thresholds per node/pool/tenant/region, including
  reserved emergency capacity and deterministic degraded modes;
- SLI/SLO/error-budget definitions and autoscaling signals with scale-up lead time,
  hysteresis, cooldown, maximum cost, port-pool provisioning, and scale-down drain.

Verification:

- production-shape load tests and model-versus-measurement checks from idle through
  saturation, burst, skewed tenants, regional failure, scale out/in, and cost caps
- forecast backtests, port/bandwidth exhaustion alarms, SLO burn alerts, billing totals,
  fairness, admission, and Pawalyze call-quality assertions

Exit criteria:

- Operators can predict safe concurrency and cost within a published error bound, and
  scaling/admission prevents accidental port, link, or budget exhaustion.
- Stop: `v0.104.0 implementation stop reached. Run pentest for this exact commit.`

### v0.105.0 - Privacy and Durable Usage

Goal: minimize sensitive network metadata while retaining accurate tenant usage and
security evidence under regional and legal policy.

Deliverables:

- data inventory and classification for client/peer IPs, usernames, tenant IDs, call
  correlation, packet counters, logs, captures, support bundles, and audit records;
- configurable regional retention, residency, redaction/pseudonymization, encryption,
  access, legal hold, export, deletion, backup, and tombstone policies;
- durable idempotent bandwidth/allocation accounting with tenant/user attribution,
  generation/failover reconciliation, clock rules, tamper evidence, and billing export.

Verification:

- retention expiry, user/tenant deletion, legal hold, region boundary, restore, support-
  bundle, access-control, key rotation, tamper, duplicate, crash, and failover tests
- reconcile packet-path counters, durable ledger, quota decisions, and billing export under
  loss/retry without storing unnecessary full addresses or credentials

Exit criteria:

- Collected data is purpose-limited, region/retention enforceable, deletion testable, and
  usage totals reconcile within a documented bound without becoming an identity leak.
- Stop: `v0.105.0 implementation stop reached. Run pentest for this exact commit.`

## Phase I: Standards Evolution and Final Assurance

### v0.106.0 - RFC 7982 Measurement Profile

Goal: give the TRANSACTION-TRANSMIT-COUNTER loss/RTT measurement attribute an
explicit bounded and interoperable profile.

Deliverables:

- RFC 7982 requirement/errata ledger, wire views, request/response counter arithmetic,
  retransmission model, privacy classification, applicability, and enablement decision;
- bounded request/response counters and retention limits that prevent overflow,
  fingerprinting expansion, reflection, or unauthenticated resource consumption;
- explicit disabled/ignored behavior on methods and transports where the profile does
  not apply, with unknown optional bytes still preserved by the wire layer.

Verification:

- normative/project vectors, counter wrap/saturation, reordered/duplicate/lost packets,
  retransmission timing, unknown peers, privacy, and amplification tests
- independent-client interoperability where available and reviewed exclusion evidence
  for every registry attribute not enabled in the declared profile

Exit criteria:

- Measurement data is accurate within its stated model, bounded, privacy-reviewed, and
  never silently accepted as authentication, allocation, or routing authority.
- Stop: `v0.106.0 implementation stop reached. Run pentest for this exact commit.`

### v0.107.0 - RFC 6679 ECN Disposition

Goal: resolve ECN-check applicability completely instead of silently omitting the
standardized attributes present in the IANA registry.

Deliverables:

- RFC 6679 requirement/errata and status review, current platform socket capability
  matrix, STUN/TURN/WebRTC deployment value, security/privacy analysis, and decision log;
- if enabled, bounded ECN-CHECK value/V-bit handling, received IP ECN observation,
  not-ECT response marking, timers, ICE applicability, isolation, and operator controls;
- if excluded from production, full wire recognition/preservation, deterministic ignore/
  error behavior, explicit profile documentation, and executable non-admission gate.

Verification:

- valid/invalid attribute, ECN marking, bleaching, remarking, loss, NAT, platform,
  reflection, cross-allocation, timeout, and capability-detection tests
- conformance/interoperability evidence for enabled behavior or tests proving the reviewed
  exclusion cannot be accidentally enabled or misrepresented in published profiles

Exit criteria:

- Every RFC 6679 and related registry behavior is either verified in a named profile or
  explicitly excluded with tests, rationale, and no silent wire or configuration gap.
- Stop: `v0.107.0 implementation stop reached. Run pentest for this exact commit.`

### v0.108.0 - API and Configuration Evolution

Goal: make public crate APIs and production configuration evolvable without surprise
breakage, downgrade, or unrecoverable mixed-version deployment.

Deliverables:

- semver baseline/diff gates for published crates, feature unification tests, MSRV API
  fixtures, serialization stability rules, and deprecation/removal policy;
- versioned configuration schemas with generated reference, unknown-field policy,
  deterministic migrations, validation, backup, forward-read, rollback, and redaction;
- mixed-version compatibility matrix covering config, admin protocol, metrics, key
  generations, capability negotiation, artifacts, and adjacent rolling upgrades.

Verification:

- public-API snapshots, downstream compile fixtures on Rust 1.90.0 through 1.97.0,
  feature powersets, semver violation fixtures, and crate package tests
- every historical schema migrates to current and rolls back where promised; interrupted,
  repeated, malformed, future-version, secret, and mixed-fleet tests pass

Exit criteria:

- Incompatible API/config changes are detected before merge, every supported migration is
  deterministic, and a mixed fleet cannot interpret one schema in conflicting ways.
- Stop: `v0.108.0 implementation stop reached. Run pentest for this exact commit.`

### v0.109.0 - Standards and Extension Governance

Goal: install the controls that keep the server current after 1.0 rather than treating
specification closure as a one-time event.

Deliverables:

- scheduled and owner-assigned RFC, RFC errata, IANA, browser, OS, TLS/DTLS, provider,
  Rust/MSRV, dependency, advisory, and interoperability review jobs;
- extension admission template requiring status, threat model, resource budget, no_std/
  portability impact, registry changes, downgrade analysis, tests, interop, and audit scope;
- documented policy for Internet-Drafts and unsupported/private extensions, plus a gate
  forbidding draft behavior in production profiles without explicit experimental isolation;
- raw unknown optional-attribute preservation and registry-drift fixtures retained as
  permanent compatibility tests.

Verification:

- inject synthetic new RFC/erratum/registry/browser/TLS/dependency events and prove each
  creates a blocking reviewed decision with owner, evidence, due date, and release impact
- missed-schedule, stale snapshot, unsupported draft, unknown extension, downgrade, and
  post-1.0 maintenance rehearsal tests

Exit criteria:

- No monitored external change can disappear silently, and future extensions have an
  executable admission/rejection path before they can enter a production profile.
- Stop: `v0.109.0 implementation stop reached. Run pentest for this exact commit.`

### v0.110.0 - First-Party Protocol Provenance

Goal: mechanically enforce the architectural rule that shipped STUN/TURN authority is
Gjallarbru code, not an imported third-party server implementation.

Deliverables:

- deny rules for dependency names, packages, symbols, licenses, features, generated code,
  vendored sources, build scripts, dynamic libraries, images, and runtime downloads;
- reviewed allowlist for primitive crypto, TLS/DTLS, PRECIS, OS, and testing providers,
  proving each remains behind a narrow local interface with no protocol authority;
- artifact-level SBOM/source/provenance checks and oracle isolation rules ensuring coturn
  or other implementations appear only in tests and cannot enter packages or images.

Verification:

- malicious fixture dependencies, renamed packages, transitive features, build outputs,
  vendored files, dynamic loads, image layers, and network-download attempts must fail CI
- inspect every crate archive, binary linkage set, OCI layer, SBOM, and provenance record;
  run offline production startup and the complete first-party protocol test suite

Exit criteria:

- Automated gates reject third-party STUN/TURN authority in every shipped artifact while
  documented primitive providers remain replaceable, audited, and policy-compliant.
- Stop: `v0.110.0 implementation stop reached. Run pentest for this exact commit.`

### v0.111.0 - Reproducible Packaging and Provenance

Goal: make every binary, crate, image, and package traceable, license-correct, and
reproducible from reviewed source.

Deliverables:

- signed source/binary archives, checksums, SBOMs, provenance attestations, containers,
  service definitions, examples, and supported OS packages;
- EUPL-1.2 application licensing and MIT OR Apache-2.0 published-crate licensing verified
  in each artifact, with independent crate versions and dependency-ordered publishing;
- hermetic/offline build inputs, pinned toolchains/images, rebuild instructions, and
  documented reproducibility exceptions with byte/source equivalence evidence.

Verification:

- clean-environment double builds, package install/upgrade/remove, SBOM/license scans,
  signature/provenance verification, container policy, and air-gapped rebuild tests
- `cargo package`/publish dry runs for each public crate and artifact comparison across
  supported builders and architectures

Exit criteria:

- Artifacts reproduce within documented bounds and contain only reviewed source,
  dependencies, metadata, licenses, and declared platform variation.
- Stop: `v0.111.0 implementation stop reached. Run pentest for this exact commit.`

### v0.112.0 - Operational Closure

Goal: prove operators can deploy, observe, rotate, drain, upgrade, recover, control
cost, and respond to abuse without improvising unsafe procedures.

Deliverables:

- installation, network/topology, capacity/cost, SLO, monitoring, key/certificate,
  OpenBao, drain, upgrade, rollback, region-failure, privacy, and recovery runbooks;
- DDoS/link saturation, credential/certificate/key compromise, tenant deletion,
  data request, incident evidence, and provider escalation procedures;
- alerts/dashboards tied to tested failure modes, resource/port/link limits, error budgets,
  rootless prerequisites, and native/container performance baselines.

Verification:

- fresh install, rolling upgrade/rollback, node/region loss, overload, scale, dependency
  failure, secret/certificate rotation, privacy deletion, cost anomaly, and incident drills
- runbook commands against signed packages/images under least privilege, with timed SLO,
  exposure, recovery, and stale-authority assertions

Exit criteria:

- Each production-critical alert has an actionable tested runbook and every drill meets
  documented recovery, security, privacy, capacity, and cost bounds.
- Stop: `v0.112.0 implementation stop reached. Run pentest for this exact commit.`

### v0.113.0 - Specification Closure

Goal: reconcile implementation, profiles, RFCs, errata, IANA registries, deployment
standards, and exclusions with no silent standards gap.

Deliverables:

- final requirement ledgers for every locked RFC/profile, errata decisions, current IANA
  drift report, URI/discovery/deployment evidence, and explicit non-applicable exclusions;
- traceability from every normative requirement and registered method/attribute/value to
  source, tests, interop, documentation, security analysis, and verified status;
- reviewed proof that ALTERNATE behavior, security features, unknown extension handling,
  RFC 7982, RFC 6679, RFC 8265, and RFC 9147 dispositions match advertised profiles.

Verification:

- zero-gap ledger validation, fresh RFC/errata/IANA comparison, documentation links,
  registry generation, independent standards review, and every conformance/profile gate
- negative audit sampling registry values and requirements to prove omissions and stale
  `planned`/`implemented` states block closure

Exit criteria:

- Every in-scope requirement is `verified`; every exclusion is reviewed and tested; no
  registry entry, erratum, deployment rule, or extension remains implicit or ambiguous.
- Stop: `v0.113.0 implementation stop reached. Run pentest for this exact commit.`

### v0.114.0 - Independent Security Audit Closure

Goal: close independent review of protocol, crypto composition, state, runtimes,
tenancy, multi-node service, Pawalyze, containers, operations, and supply chain.

Deliverables:

- external audit and pentest reports, finding register, fixes, regression tests, retest
  evidence, rootless/HA/Pawalyze attack results, and residual-risk decisions;
- refreshed threat models covering Internet and privileged boundaries, tenant isolation,
  OpenBao/credentials, key coordination, DDoS, privacy, update, and artifacts;
- independent scope confirmation that first-party code owns all STUN/TURN authority.

Verification:

- auditor retest of every critical, high, and applicable medium finding, plus sampled
  lower findings and all exact-candidate regression evidence
- complete security, conformance, fuzz, formal, dependency, tenant, HA, network, browser,
  rootless, privacy, artifact, and release gates

Exit criteria:

- No unresolved critical or high finding remains; accepted lower risk has owner, rationale,
  compensating control, expiry/review date, and public disclosure disposition.
- Stop: `v0.114.0 implementation stop reached. Run pentest for this exact commit.`

### v0.115.0 - Final Production Release Candidate

Goal: freeze and rehearse the exact production release process and public contract after
all protocol, deployment, application, governance, and audit work is complete.

Deliverables:

- final API/config/wire/deployment/support/SLO/privacy scope and documentation freeze;
- complete signed artifacts, migration/rollback guidance, compatibility and residual-risk
  reports, maintenance calendar, and clean-environment dry-run publication;
- exact-candidate audit and pentest scope covering Pawalyze, multi-node, rootless, native,
  every declared transport/address family, and production operational controls.

Verification:

- full rehearsal from checkout through crate/artifact/image publication verification,
  deployment, upgrade, rollback, compromise response, and withdrawal
- all workspace, MSRV/platform, standards, interoperability, browser, security, formal,
  soak, capacity, privacy, package, provenance, operations, and readiness gates

Exit criteria:

- Only production-blocking fixes are allowed afterward; each creates a new candidate,
  complete regression evidence, independent retest where affected, and exact-commit pentest.
- Stop: `v0.115.0 implementation stop reached. Run pentest for this exact commit.`

### v1.0.0 - Production-Ready Gjallarbru

Goal: release the first serious production-ready STUN/TURN server application with
all declared profiles and security claims backed by pentest and final-CI evidence.

Deliverables:

- production binaries, published crates, signed packages, SBOMs, provenance,
  release notes, operator documentation, support matrix, and security advisories;
- final conformance, interoperability, audit, performance, capacity, cost, privacy,
  DDoS, cluster, Fluxheim, rootless Wolfi/Debian, Pawalyze, and residual-risk evidence;
- public node-local failure/recovery SLO, tenant/realm contract, credential lifetime,
  supported topology matrix, data policy, and ongoing standards-review schedule.

Verification:

- complete workspace and Rust 1.90.0-through-1.97.0 matrix, platform/device matrix,
  all RFC/profile gates, dependency/license policy, fuzz/formal/soak evidence,
  reproducible packaging, and `scripts/validate-release-readiness.sh v1.0.0`
- independent pentest and audit retest, plus documented later CodeQL remediation
- Chromium/Firefox/Safari Pawalyze, node/region loss, mixed-upgrade, source-preserving
  rootless/native, Wolfi/Debian parity, Fluxheim hybrid, secure-cluster, NAT64/PMTU,
  link-defense, privacy, and capacity/cost gates

Exit criteria:

- All `v1.0.0` claims are evidenced, every release blocker is closed, no critical or
  high finding remains, the reviewed commit is in tag history, and final CodeQL is green.
- Stop: `v1.0.0 implementation stop reached. Run pentest for this exact commit.`
