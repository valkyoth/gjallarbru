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
| Private-destination policy could be either universally blocked or accidentally open, while address aliases, mapping changes, runtime reinterpretation, or queued stale authority could retain unintended authority. | `v0.37.2` canonicalizes generation-bound destinations, `v0.37.3` closes translation lifecycle, `v0.37.4` seals approved endpoints into typed capabilities, `v0.37.5` bounds their execution-time authority, `v0.37.6` installs mandatory relay defenses, and `v0.56.0`/`v0.57.0` add configurable profiles and comprehensive SSRF controls. |
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
| Separate public crates could leave users without a coherent `gjallarbru::` entry point or allow facade documentation to drift. | `v0.55.1` admits a no_std facade, stable namespaced re-exports, root-README parity, and facade-last publication. |
| Determinism, time, entropy, storage, command atomicity, and buffer ownership could remain implicit until the sans-I/O API is frozen. | `v0.2.1` freezes the contract, `v0.2.4` makes its kernel executable early, and `v0.23.1` proves the full reducer with byte-identical all-or-nothing transitions. |
| A protocol or credential name without a standard or project specification could silently acquire authority. | `v0.2.1` requires a reviewed mechanism registry; names such as `STUN-DEREF` remain unsupported until a threat model, key domain, wire assignment, and requirement evidence exist. |
| `no_std` could compile on hosts while still requiring an allocator, OS import, large stack copy, blocking storage, or unsafe feature combination. | `v0.6.1` adds a freestanding no-allocator/no-atomic local fixture; `v0.6.2` closes deterministic storage, debt, width, and wrap behavior. |
| Receive padding, post-integrity attributes, repeated scans, oversized inventories, or ChannelData datagram alignment could be implemented with subtly incorrect semantics. | `v0.5.1`, `v0.8.1`/`v0.8.2`, `v0.15.1`, and `v0.22.1` close cursor progress, sparse authenticated views, legal UDP forms, complexity, and operation ceilings. |
| Broad crypto traits or ordinary secret types could hide allocation, key export, variable output, timing, or provider-failure behavior. | `v0.17.1`, `v0.19.1`, and `v0.26.1` define capability-specific providers, secret wrappers, scatter integrity, fail-closed errors, opaque handles, and timing qualification. |
| Transaction equality or response caching could rely on a weak digest or item count while ignoring collision, tombstone, iteration, and byte-exhaustion risk. | `v0.6.2` and `v0.30.1` require bounded table structure, keyed identity, collision evidence, and independent cached byte budgets. |
| Allocation/copy/task accounting and formal state evidence could arrive only after the first real packet and relay paths. | `v0.31.1` instruments the first runtime hot path; `v0.39.1`/`v0.39.2` move reference and lifecycle model checking before real relay sockets. |
| Zero-copy relay output could return a borrow after its receive buffer is reused. | `v0.47.1` requires generation-tagged leases and completion-aware scatter plans before relay performance claims. |
| Batching or kernel acceleration could treat partial sends, capability consumption, stale completions, map loss, revocation, or expiry differently from scalar core behavior. | `v0.79.1` closes completion truth, `v0.79.2` closes per-entry authority/ownership, and `v0.82.1` closes acknowledged fast-path revocation, reuse, expiry, and reconciliation. |
| Keyword anchors could be marked verified by plausible-looking strings without semantic refinement, a real symbol, or an executed test. | `v0.2.2` adds semantic child requirements and a CI evidence manifest that resolves implementation symbols and records observed test execution. |
| A successful core transition could still overrun adapter capacity, repeat expensive work while sizing a reservation, or be only partly visible. | `v0.23.2` creates one exact prepared transition, `v0.23.3` closes adapter reservation/operation-ID authority, and `v0.23.4` defines adapter-owned publication. |
| Client identity could survive listener, socket, configuration, proxy, interface, or worker reuse. | `v0.4.1` makes every relevant path/provenance generation part of authorization identity. |
| An opaque synchronous crypto provider could conceal blocking HSM/KMS I/O, allocation, mutable state, ambient entropy, or nondeterministic output. | `v0.17.2` separates bounded deterministic packet crypto from asynchronous external-crypto command/completion operations. |
| Stale timing-wheel entries and large time jumps could create unbounded expiration debt or accidentally extend authorization. | `v0.36.1` bounds live/dead entries, rescheduling, expiration work, overdue fairness, and time-jump behavior. |
| Configuration reload and emergency revocation could conflict with transaction retransmission idempotence. | `v0.30.2` pins ordinary transactions to their decision generation and gives every revocation class an explicit replay/error/discard/teardown rule. |
| TLS/DTLS resumption could admit replayable early application data for state-changing STUN/TURN methods. | Initial rejection is mandatory in `v0.73.0` and `v0.75.0`; `v0.76.2` proves cross-provider/topology closure and requires a future method-level proof for any exception. |
| “Output uncommitted” could ambiguously mean unchanged bytes or merely no returned length, while finalizer slots could be reused, transferred, or executed out of dependency order. | `v0.16.0` introduces plan-bound exact-once slots and an integrity-before-FINGERPRINT graph across `EncodeDraft -> ValidatedPlan -> FinalizedEncodePlan -> commit`; `v0.17.0` through `v0.19.0` add protocol-specific finalizers. |
| Send/Data relay could transfer borrowed payloads before zero-copy lease ownership is implemented. | `v0.43.1` requires bounded runtime-owned copies for early relay paths; `v0.47.1` later admits generation-tagged zero-copy leases. |
| Fast-path packet/byte counters could become independently refillable quota authority. | `v0.82.2` models kernel budgets as finite generation-bound leases reconciled by core before renewal. |
| Relay-port randomness could conflict with deterministic reducer inputs or repeat biased candidates after fork/restart. | `v0.37.1` specifies explicit worker-seed/completion policy, unbiased unique search, seed independence, and deterministic exhaustion. |
| Absolute-time rollback handling alone could leave forward jumps, uninitialized clocks, and recovery ambiguous or make nonce work depend on a later type. | `v0.4.0` defines absolute time, trust, source, and generation; `v0.25.1` adds production clock-health transitions and recovery without altering monotonic lifetimes. |
| Concurrency models could arrive only after cross-worker queues and configuration publication are already entrenched. | Initial focused Loom evidence is an exit condition of `v0.78.0`; `v0.78.1` expands the inventory and `v0.93.0` remains comprehensive closure. |
| Command admission could allow a committed reducer transition followed by partial runtime acceptance. | `v0.23.2` requires one exact adapter reservation and caller arena from immutable prepared requirements; adversarial partial arena acceptance remains uncommitted, while later execution is completion-driven. |
| Treating every output as one mutually exclusive effect class could exhaust operation tables or lose ownership/audit duties on a best-effort send. | `v0.23.5` composes semantic authority, resource ownership, delivery guarantee, and durability/audit properties in one effect envelope. |
| Asynchronous packet HMAC could retain an escaping borrow or undocumented unbounded packet copy. | `v0.17.3` keeps base-profile packet HMAC synchronous and defines immutable generation-tagged lease/copy ceilings before any asynchronous packet-crypto profile can be admitted. |
| A safeguard closure could arrive after the first feature that depends on it. | Clock trust is mandatory in `v0.25.0`, TLS/DTLS early data is rejected in `v0.73.0`/`v0.75.0`, and initial Loom models gate `v0.78.0`; later patch milestones expand cross-provider and model closure. |
| A public Binding listener could expose uncharged parse, HMAC, lookup, preparation, or error-response work, or recover capacity through failure refunds. | `v0.30.3` requires one finite linear ingress permit before parsing, with global/listener/worker limits and monotonic token-bucket refill before `v0.31.0`. |
| Queue occupancy, reserved allowance, attempted work, successful completion, and retries could be refunded or charged inconsistently. | `v0.23.6` defines general accounting modes, while `v0.30.3` converts only started ingress stages from reservation to non-refundable attempt charge. |
| Packet queues could consume the capacity needed for transitive completion, compensation, revocation, shutdown, audit, or ownership-release effects. | `v0.23.7` reserves the complete bounded acyclic control-effect closure and coalesces duplicate/stale terminal events. |
| A prepared transition or observation snapshot could escape its worker, retain secrets/buffers, or create unbounded reader retention. | `v0.23.2` closes prepared ownership/scrubbing and `v0.23.8` bounds redacted non-authoritative snapshot publication and reclamation. |
| NAT64 prefix validation could cite RFC 6052 without locking the normative source used for implementation and vectors. | RFC 6052 is checksum-locked in the source baseline and its mapping rules are versioned in `v0.37.3`. |
| A ready batch could be lost or partly executed across a crash, leaving an opened OS resource, lease, or stale completion unaccounted. | `v0.23.9` defines accepted-batch reconciliation, deterministic cancellation, resource fencing, and old-epoch rejection. |
| Threaded release/acquire publication could leak atomics or Send/Sync requirements into the portable no_std core. | `v0.23.10` keeps concurrency in runtime adapters and proves local/no-atomic and threaded adapters equivalent. |
| Policy could approve one canonical peer while a runtime reconstructs or substitutes another raw endpoint. | `v0.37.4` requires typed generation-bound authorized peer/relay capabilities in every policy-sensitive runtime command. |
| Cancellation request, OS success, failure, and duplicate terminal observations could race without one authoritative outcome. | `v0.23.11` defines a bounded terminal-mailbox state machine where cancellation is intent, identical terminals coalesce, and conflicts enter deterministic uncertainty/reconciliation. |
| A whole-process restart could mistakenly adopt prior node-local allocations or replay non-idempotent delivery with unknown status. | `v0.23.9` limits reconciliation to surviving authority, fences and closes old resources after process loss, preserves attempt charges, and forbids base-profile adoption. |
| Maximum-stage reservations could be pre-acquired for queued or batched packets and starve other listeners or authenticated traffic. | `v0.30.5` requires just-in-time, short-lived, per-packet permits with bounded outstanding reservations and deterministic listener/work-class fairness. |
| A valid endpoint capability could wait in a queue past permission expiry or revocation and become indefinite runtime authority. | `v0.37.5` makes delivery capabilities single-use, execution-deadline/queue-age/command/charge bound, generation-checked, and revocation-fenced before reuse. |
| TCP, TLS, DTLS, trusted termination, or shared-port dispatch could bypass the UDP ingress work budget. | Initial transport milestones inherit `v0.30.3`-`v0.30.5`; `v0.77.1` proves every admitted plaintext frame uses one normalized ingress permit after transport-specific handshake/framing admission. |
| Pre-parse fairness could reserve HMAC/lookup capacity before the request method or work class is knowable. | `v0.30.4` separates charged fixed-header classification from irreversible bounded conversion into one finite method/work-class permit. |
| Peer-bound commands could use typed endpoint authority while client responses and indications still use raw or stale paths. | `v0.30.6` requires one `AuthorizedClientPath` for every client send; `v0.45.0`/`v0.47.0` canonicalize incoming peer identity before permission/channel lookup. |
| A revocation fence could rely on FIFO assumptions without proving every queue, submission ring, or kernel lane stopped older authority. | `v0.23.12` defines monotonic authority sequences, per-domain acknowledgements, reuse barriers, and disjoint-generation fallback. |
| Partial `sendmmsg` or provider batches could consume all single-use capabilities even though only a prefix reached the OS. | `v0.79.2` consumes only handed-off entries; unsent packets retain exclusive ownership and revalidate authority/fences before charged retry. |
| Repeated revocations could allocate unbounded fence operations or invalidate unrelated worker commands while an earlier fence remains pending. | `v0.23.13` coalesces fixed per-lane high-water marks, freezes bounded lane membership, defines acknowledgement precisely, and separates ordering from semantic generations. |
| A local timeout could be mistaken for proof that an external operation failed or was cancelled. | `v0.23.14` makes deadline expiry nonterminal, initiates cancellation/reconciliation, and preserves operation-policy handling of valid late success. |
| Fixed-header classification could claim to identify cached retransmissions before paying the transaction-cache lookup needed to prove them. | `v0.30.7` charges the ordinary method class and one bounded lookup before entering a cached-response substate, with no work refunds or cheap collision oracle. |
| A partially written TCP/TLS frame could expire or be revoked with its tail dropped while the connection remains open, corrupting stream framing. | `v0.79.3` keeps the frame at the write-ledger head and requires bounded completion or connection close with an exact TLS/provider handoff boundary. |
| Fence acknowledgement could be misread as releasing buffers, descriptors, leases, or provider storage still reachable by already-handed-off operations. | `v0.23.15` separates ordering acknowledgement, in-flight tracking, semantic generation reuse, and terminal physical ownership release. |
| A silent provider could leave `DeadlineExceeded`/`CancelRequested` operations and terminal mailboxes unresolved forever. | `v0.23.16` bounds attempts, rounds, age, counts, escalation, quarantine, non-aliasing storage, and saturation recovery. |
| Client-bound Data or ChannelData could bind only the client path while peer permission/channel authority changes before final handoff. | `v0.43.2` chooses live final-handoff semantics before relay media activates and binds canonical peer plus permission/channel generations, expiry, refresh, revoke, and rebind behavior. |
| TLS/DTLS adapters could hide unbounded provider buffers or per-record allocations despite precise protocol handoff semantics. | `v0.72.1` gates every adapter before activation; `v0.76.3` closes lifecycle/hot-path allocation, provider byte ceilings, backpressure, cleanup, and zeroization across all selected providers. |
| An adapter could claim execution-domain destruction without proving kernel, DMA, provider-thread, or registered-memory quiescence. | `v0.23.17` requires typed generation-bound adapter evidence before quarantined physical ownership is released. |
| Cache hit/miss latency could be specified as impossible constant-time equality, encouraging artificial authentication work and a new DoS cost. | `v0.30.8` defines cache-membership secrecy, bounded envelopes, secret comparisons, semantic equivalence, and optional release scheduling without repeated expensive work. |
| A runtime could inspect snapshots or reconstruct authority when queued relay-media permission/channel generations become stale. | `v0.43.3` makes stale-drop mandatory by default and permits replacement only through one bounded core-owned reauthorization event. |
| TLS/DTLS control records that never become STUN frames could consume uncharged post-handshake crypto, output, timers, or state. | `v0.72.2` defines pre-plaintext control budgets and disabled features; `v0.76.4` closes equivalent enforcement across all selected providers. |
| The documented crate graph could hide runtime's direct wire dependency and permit framing code to construct authenticated or method-authorized views. | `v0.2.3` documents the real graph and mechanically confines semantic promotion and wire/crypto composition to core. |
| Determinism could remain an architectural promise until the full STUN core, allowing layout, word width, capacity, or correlation IDs to harden into APIs first. | `v0.2.4` lands a minimal executable reducer kernel and differential replay harness before protocol APIs. |
| Queue-shaped permits, generations, or publication types could force core consumers to adopt Gjallarbru's runtime topology. | `v0.2.5` separates semantic preparation/commit from adapter-owned reservation and publication. |
| Locked extension/deployment RFC text could remain only downloaded reference material until immediately before a conformance claim. | `v0.2.6` and `v0.2.7` complete semantic ledgers for every locked non-base profile before implementation authority. |
| Storage layout, tombstone debt, `usize` width, generation wrap, or ambiguous Tick comparison could change deterministic results or exceed constrained-target bounds. | `v0.6.2` fixes probes/load/debt/order/width/wrap/horizon contracts with model evidence. |
| A one-pass attribute inventory could allocate or retain one descriptor per tiny attribute and misclassify its own capacity limit as malformed input. | `v0.8.2` uses sparse fixed metadata plus caller-bounded unknown-required accumulation and a distinct resource outcome. |
| Encoder dependency/finalizer plans could be logically bounded yet still allocate vectors, closures, trait objects, or grown scatter lists per message. | `v0.16.1` requires fixed arrays/caller workspace and fail-allocator/copy evidence before finalizers. |
| A global zero-copy/allocation-free claim could conceal different warm-up, security-copy, stream, and provider behavior. | `v0.80.1` defines transport/phase-specific allocation, copy, retention, and qualification profiles. |
| UDP GRO/GSO could accidentally authenticate or charge a coalesced super-packet once or invent per-segment completion truth unavailable from the provider. | `v0.79.4` preserves scalar identity/admission/accounting per original datagram and disables ambiguous segmentation paths. |
| Reference tests could miss lifecycle interleavings spanning allocation open, timeout/cancel, fence, quarantine, and quiescence before real sockets arrive. | `v0.39.2` model-checks the complete external-effect lifecycle and promotes every counterexample. |

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

### v0.2.1 - Deterministic Architecture Contract

Goal: freeze every input, side-effect, ownership, and failure boundary required
for a deterministic sans-I/O reducer before protocol APIs become compatibility
constraints.

Deliverables:

- an ADR defining identical output/state for identical initial state,
  immutable configuration, ordered events, supplied monotonic/absolute times,
  entropy completions, provider completions, storage seed/layout inputs, output
  capacity, path/event identity, and every security-relevant generation;
- all-or-nothing command and encoded-output preflight, explicit equal-tick,
  duplicate/decreasing/wrapping time rules, and wall-clock rollback isolation;
- generation-tagged entropy request/completion, buffer-lease, provider, and
  runtime-operation contracts with purpose and length domains;
- synchronous bounded callback-free storage requirements, complexity/capacity
  guarantees, capability-shaped runtime commands, and typestate boundaries;
- prohibition on semantic dependence on collection iteration/insertion order,
  pointer/address layout, `usize` width, platform endianness, allocator placement,
  runtime correlation IDs, or other inputs absent from the reducer envelope;
- a mechanism-admission register requiring a specification, threat model, key
  domain, wire identifier, and requirement entries before an internal name can
  acquire protocol authority; `STUN-DEREF` is explicitly unsupported/unassigned.

Verification:

- executable architecture examples replayed twice for byte-identical command/state
  output, followed by the minimal real core artifact required by `v0.2.4`
- ADR review matrix covering capacity failure, equal/decreasing time, entropy
  failure, stale completion, lease reuse, storage misbehavior, and unknown names

Exit criteria:

- No core API can hide time, entropy, blocking work, allocation, partial side
  effects, buffer lifetime, or an unspecified protocol mechanism.
- Stop: `v0.2.1 implementation stop reached. Run pentest for this exact commit.`

### v0.2.2 - Executed Requirement Evidence

Goal: ensure `verified` means a semantically reviewed rule is connected to
real implementation and test execution, not merely populated metadata.

Deliverables:

- a refinement format linking extracted keyword anchors to one or more semantic,
  independently testable requirements without losing source-line provenance;
- repository symbol resolution for every implemented/verified requirement and
  rejection of missing, private-to-the-wrong-component, generated-only, or stale symbols;
- a deterministic CI evidence manifest recording the exact named tests observed
  in the release run, with profile, feature, target, and toolchain context;
- status-transition rules requiring reviewed semantic scope, real symbol,
  executed positive/negative tests, and applicable RFC/errata evidence before
  `verified`, while exclusions retain explicit decision evidence;
- negative fixtures for invented symbols, unexecuted/renamed tests, duplicate
  semantic children, orphan anchors, and evidence from a different profile.

Verification:

- `scripts/validate-requirements.sh` against synthetic real/missing/stale symbol
  and executed/unexecuted test manifests
- a fixture test intentionally removed from execution must prevent its
  requirement from becoming or remaining `verified`

Exit criteria:

- No requirement can claim verification unless CI for the exact candidate
  resolves its implementation and observes its declared tests in the right profile.
- Stop: `v0.2.2 implementation stop reached. Run pentest for this exact commit.`

### v0.2.3 - Crate Authority and Dependency Boundary

Goal: document and mechanically enforce the real crate graph before framing,
crypto, or runtime APIs can accidentally acquire semantic protocol authority.

Deliverables:

- one authoritative dependency graph matching Cargo metadata:
  `server -> runtime -> {core, wire}`, `core -> {wire, crypto}`, with `wire` and
  `crypto` independent and the later facade depending only on reusable crates;
- runtime access to `wire` limited to byte classification, transport framing,
  exact frame consumption, and raw untrusted views needed for buffer handling;
- only core can upgrade raw/basic wire input into authenticated, method-valid,
  allocation/permission/channel/policy-authorized states or construct semantic
  runtime commands;
- sealed constructors/module visibility preventing runtime from constructing
  authenticated/method-valid views, integrity success, policy decisions, or
  capability-bearing commands from raw fields;
- core-owned orchestration translating wire range/segment descriptions into
  crypto provider input so neither `wire -> crypto` nor `crypto -> wire` is
  required and no dependency cycle or exported-key bridge appears;
- runtime-produced metadata and typed frame views remain explicitly untrusted
  reducer inputs, generation-bound to their source buffer/path where applicable;
- capability and quiescence types documented as evidence-bearing contracts for
  reviewed conforming adapters, not cryptographic protection against a runtime
  that already has syscall authority;
- README, crate READMEs, architecture docs, Cargo metadata allowlists, and
  generated dependency diagrams checked for exact agreement.

Verification:

- Cargo-metadata dependency/feature-policy tests rejecting new reverse edges,
  cycles, or runtime access to forbidden reusable-crate modules
- compile-fail/public-API fixtures proving runtime cannot construct or promote
  authenticated, method-valid, authorized endpoint, or quiescence values
- raw-frame-to-core-to-command integration test proving runtime classification
  remains untrusted until core performs the semantic transition
- documentation graph parity and provider substitution tests proving wire/
  crypto composition remains core-owned without key export or fallback

Exit criteria:

- The documented graph matches the build, and no runtime framing or crypto
  dependency can bypass core to create authentication, state, policy, or send authority.
- Stop: `v0.2.3 implementation stop reached. Run pentest for this exact commit.`

### v0.2.4 - Executable Reducer Kernel

Goal: turn deterministic architecture from prose into a minimal protocol-neutral
core artifact before STUN/TURN API details become compatibility constraints.

Deliverables:

- a small no_std reducer kernel using caller-owned state, input, workspace, and
  command arena, with no protocol parsing claim and no heap/clock/I/O/random access;
- one canonical explicit input envelope containing ordered event identity,
  complete path/generations, monotonic and absolute-time observations, entropy
  bytes, provider completions, configuration generation, storage seed/layout
  inputs, and output/workspace capacity;
- byte-identical resulting state and commands for identical envelopes, with
  adapter queue/provider/transport correlation IDs excluded from semantic input;
- deterministic ordering rules forbidding output/state dependence on hash-table
  iteration, insertion/tombstone layout, pointer/address layout, `usize` width,
  platform endianness, allocator behavior, or unspecified collection order;
- capacity/fault points proving insufficient workspace/command/output storage
  leaves caller state, visible output, operation counters, and effects unchanged;
- fixed canonical test snapshots and a replay harness reusable by every later
  reducer milestone, including failure offset and first-divergence diagnostics;
- a deliberately tiny behavioral implementation and nonzero unit/property test
  suite without implying Binding, authentication, allocation, or conformance.

Verification:

- `cargo test -p gjallarbru-core reducer_kernel`
- repeated identical-envelope replay plus event-order permutations proving order
  is explicit, entropy/provider result substitution, time-source generation, and every capacity
- 32-/64-bit or equivalent width fixtures plus storage seed, insertion order,
  tombstone layout, memory-address, and runtime-correlation differential tests
- fail-at-every-write instrumentation proving observationally unchanged state,
  arena, and output on failure
- no_std/no-allocator link check and traps for ambient time, entropy, callback,
  thread-local, blocking, unwinding, or hosted-OS access

Exit criteria:

- Determinism and atomic absence on failure have executable evidence in core;
  they are no longer claims inferred from an empty crate or documentation alone.
- Stop: `v0.2.4 implementation stop reached. Run pentest for this exact commit.`

### v0.2.5 - Adapter-Neutral Capacity Admission

Goal: preserve atomic semantic preparation and commit without forcing a
microkernel, simulator, bare-metal loop, or OS runtime to adopt one queue model.

Deliverables:

- four explicit layers: core prepares a semantic transition in caller workspace;
  adapter reserves its own effect/output capacity; core commits into a caller-
  supplied bounded command arena; adapter publishes the completed arena;
- `TransitionRequirements` describes semantic command kinds/counts, bytes,
  retained ownership, terminal/control obligations, and alignment only—not queue
  topology, wakeups, atomics, executor tasks, provider lanes, or OS submissions;
- adapter-owned non-clone capacity reservation/token opaque to semantic logic,
  with core observing only exact sufficiency, arena identity/capacity, and
  single-consume validity;
- queue/listener/worker generations, reservation ledgers, correlation IDs,
  publication state, and release/acquire mechanics kept in adapter envelopes and
  unable to affect reducer output, operation identity, or authorization;
- local in-place adapter, simulated/custom-queue adapter, and later threaded
  adapter able to implement equivalent reserve/commit/publish semantics without
  core types depending on concurrency primitives;
- exact release on failed/stale commit and prohibition of partial command-arena
  publication, while post-publication OS partial execution remains completion-driven;
- forward requirements updating `v0.23.2`-`v0.23.4` to consume this separation
  rather than exposing a queue-shaped `CommandBatchPermit` in core.

Verification:

- `cargo test -p gjallarbru-core adapter_neutral_admission`
- compile/API checks that core public types contain no atomics, queue/provider
  IDs, wakeups, tasks, OS handles, runtime reservation ledgers, or topology enums
- local, ring-buffer, deliberately unusual simulator, and threaded-test adapter
  differential replays with distinct layouts/correlation IDs and identical semantics
- insufficient/stale/dropped reservation, arena substitution, partial capacity,
  commit failure, pre-publication crash, and adapter publication-invariant tests
- freestanding fixture proving caller arenas and opaque capacity tokens require
  neither global allocation nor a project-specific executor/queue implementation

Exit criteria:

- Core owns semantic atomicity while every consumer remains free to choose its
  bounded capacity and publication mechanics without changing protocol behavior.
- Stop: `v0.2.5 implementation stop reached. Run pentest for this exact commit.`

### v0.2.6 - Core and Deployment Standards Ledgers

Goal: expand semantic traceability before non-base authentication, addressing,
discovery, URI, and deployment profiles can claim implementation or conformance.

Deliverables:

- complete section/keyword inventories, errata decisions, semantic child
  requirements, profile ownership, milestones, symbols/tests placeholders, and
  explicit exclusions for locked RFC 5780, RFC 5928, RFC 6052, RFC 7064,
  RFC 7065, RFC 7376, RFC 7443, RFC 8155, RFC 8265, and RFC 9325;
- RFC 5769 classified as vector/evidence provenance rather than a protocol
  conformance profile, with every usable vector mapped to its consumer milestone;
- RFC 2119/RFC 8174 interpretation rules applied consistently without treating
  their boilerplate as an independently advertised feature;
- cross-RFC conflict/supersession links and decisions where base STUN/TURN,
  authentication security, address translation, discovery, and TLS policy overlap;
- no profile status beyond `planned` until `v0.2.2` resolves real symbols and
  observes executed semantic positive/negative tests.

Verification:

- zero-gap validation and negative fixtures for every added locked document,
  semantic child, erratum, exclusion, supersession, and evidence-only source
- sampled manual source-to-ledger review plus deterministic regeneration and
  exact requirement-count drift reports
- feature/profile gates proving an unverified or incomplete ledger prevents the
  corresponding release milestone and conformance documentation

Exit criteria:

- Every locked core/deployment standard has complete semantic planning evidence
  before its profile can enter implementation or public support claims.
- Stop: `v0.2.6 implementation stop reached. Run pentest for this exact commit.`

### v0.2.7 - Extension and Transport Standards Ledgers

Goal: complete semantic traceability for every locked TURN extension and secure/
shared transport before any extension-specific wire number or behavior activates.

Deliverables:

- complete section/keyword inventories, errata decisions, semantic child
  requirements, profile ownership, milestones, symbols/tests placeholders, and
  explicit exclusions for locked RFC 6062, RFC 6679, RFC 7350, RFC 7635,
  RFC 7982, RFC 7983, RFC 8016, RFC 9147, and RFC 9443;
- explicit cross-profile requirements for TCP allocations, ECN, DTLS, third-
  party authorization, transaction measurement, shared-port demultiplexing,
  mobility, DTLS 1.3, and TURN-over-QUIC applicability/non-claims;
- assignment-provenance requirements prepared for the later reviewed `v0.3.0`
  IANA snapshot, with no numeric value entering code before that gate; standardized,
  reserved, unassigned, and vendor-specific values remain distinct/inert;
- extension admission fails when its specification, threat model, key domain,
  wire assignment, semantic requirements, or interoperability role is missing;
- no extension status beyond `planned` until `v0.2.2` evidence gates pass.

Verification:

- zero-gap validation and negative fixtures for every added document/profile,
  erratum, exclusion, numeric assignment, and cross-RFC dependency
- IANA schema/assignment negative fixtures ready for `v0.3.0`, proving ledger
  completion alone cannot activate or generate a numeric protocol assignment
- configuration/wire fixtures proving vendor or unassigned methods/attributes
  stay observable-but-inert and cannot alias a standardized profile

Exit criteria:

- Every locked extension/transport claim has complete semantic planning before
  `v0.3.0` locks assignment provenance and implementation can grant authority.
- Stop: `v0.2.7 implementation stop reached. Run pentest for this exact commit.`

### v0.3.0 - IANA Snapshot Tooling

Goal: make protocol assignments reviewed, generated, and reproducible.

Deliverables:

- dated method, attribute, error, channel, security-feature, and password
  algorithm registry snapshots with source metadata;
- explicit standardized, reserved, unassigned, and vendor-specific states;
  vendor/unassigned values stay raw and inert unless `v0.2.7` extension admission
  evidence separately assigns an implementation profile;
- manual updater, schema validator, deterministic generator, and review diff.

Verification:

- `scripts/check-iana-snapshot.sh`
- regenerate twice and compare byte-for-byte output
- live-versus-locked drift and vendor/unassigned-alias negative fixtures

Exit criteria:

- Normal builds are offline and numeric assignments are not scattered as
  undocumented constants.
- Stop: `v0.3.0 implementation stop reached. Run pentest for this exact commit.`

### v0.4.0 - Primitive Domains

Goal: define OS-independent protocol, time, identity, limit, and error types.

Deliverables:

- IP/transport addresses, methods/classes, transaction IDs, channel numbers,
  paths, monotonic time, capacities, and stable errors;
- `AbsoluteTime` with an observation, explicit trusted/uncertain/unavailable
  status, source identity, and generation, kept distinct from monotonic time;
- checked constructors and redacted formatting for sensitive identifiers.

Verification:

- `cargo test -p gjallarbru-wire -p gjallarbru-core`
- boundary and formatting tests for every constructor and error category
- absolute-time equality/order/source-generation tests proving untrusted or
  cross-source observations cannot be silently treated as trusted timestamps

Exit criteria:

- Core APIs use explicit domains rather than OS socket types or ambiguous raw
  integers.
- Stop: `v0.4.0 implementation stop reached. Run pentest for this exact commit.`

### v0.4.1 - Complete Client-Path Identity

Goal: ensure authorization identity cannot survive reuse of a listener,
endpoint, configuration, proxy relationship, interface, connection, or worker.

Deliverables:

- `ClientPath` domains for remote/local transport addresses, stable
  `ListenerId`, listener/configuration generation, and local socket/endpoint ID;
- ingress provenance distinguishing direct packets, trusted proxy metadata,
  TLS termination, and DTLS sessions with their authenticated generations;
- platform interface/scope identity where required, connection/session
  generation, worker ownership epoch, and explicit equality/hash semantics;
- realm/tenant/path selection rules that never infer identity from an address
  alone when multiple listeners or provenance domains share it;
- stale-listener, socket-reuse, proxy-trust-change, configuration-reload,
  interface-reuse, connection-reuse, and worker-migration invalidation policy.

Verification:

- constructor/equality/hash/redaction tests for every identity dimension
- generated cross-product tests proving any security-relevant generation or
  provenance change prevents allocation, transaction, nonce, and cache reuse

Exit criteria:

- No stateful authority is keyed only by a remote/local address tuple when a
  listener, endpoint, provenance, interface, connection, or worker can be reused.
- Stop: `v0.4.1 implementation stop reached. Run pentest for this exact commit.`

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

### v0.5.1 - Hostile-Input Parser Foundation

Goal: make linear progress, termination, and resource ceilings executable
properties before higher-level wire parsing begins.

Deliverables:

- one checked offset/length/padding implementation with structural padding
  validation, receive-side padding-value ignorance, and zero-only encoding;
- parser-local single-cursor APIs whose successful loop step advances by at
  least the applicable minimum header, whose first failure permanently fuses,
  and whose offsets cannot reset or jump without checked addition before slicing;
- no recursion or attacker-controlled backtracking/reparse, exact permitted
  datagram-frame consumption, and stream consumption that retains no borrow
  across mutable buffer compaction/reuse;
- explicit message/attribute ceilings;
- fixed scan and cryptographic-operation budgets plus an admission rule against
  repeated attribute rescans that create attacker-controlled quadratic work;
- first-change fuzz smoke harnesses, no-panic boundary corpus, and allocation/
  copy counters available to every later wire milestone.

Verification:

- arbitrary byte and offset/length/padding property tests, including nonzero padding
- fuzz smoke proving success advances, failure terminates, and configured work
  ceilings cannot be exceeded
- compile/API and Kani candidates proving loops cannot clone/reset the cursor,
  failure is fused, and stream borrows cannot outlive buffer mutation

Exit criteria:

- Later parsers have one bounded mechanical foundation and cannot reinterpret
  padding-value bytes as a receive-side validity condition.
- Stop: `v0.5.1 implementation stop reached. Run pentest for this exact commit.`

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

### v0.6.1 - Freestanding and Storage Qualification

Goal: prove that `no_std` means usable without an operating system or global
allocator, not merely compilable for a hosted target.

Deliverables:

- a freestanding downstream fixture with no global allocator, no OS imports,
  caller-owned stores/command buffers, in-place initialization, and fixed panic handling;
- no pointer-width atomics on the local path, callbacks, hidden blocking,
  unwinding, thread-local storage, ambient clocks, or executor/runtime imports;
- `--no-default-features`, every supported feature combination, and representative
  bare-metal target builds with measured stack/static-memory footprints;
- qualified storage implementations whose operations are synchronous, bounded,
  callback-free, non-blocking, and documented with maximum complexity/capacity;
- construction rules preventing large fixed arrays from being copied through the
  stack and production-claim gates excluding unqualified custom storage;
- integration with `v0.6.2` deterministic iteration, tombstone debt, word-size,
  generation-wrap, and maximum Tick-comparison-horizon contracts.

Verification:

- compile/link fixture with allocator symbols forbidden and OS imports scanned
- symbol/import traps for atomics, TLS, unwinding, callbacks, clocks, blocking,
  executors, and hosted runtime initialization
- stack-size, in-place construction, capacity/exhaustion, feature-matrix, and
  malicious storage-contract fixture tests

Exit criteria:

- The portable core can be integrated with caller-owned memory on a freestanding
  target, and production claims name only qualified storage implementations.
- Stop: `v0.6.1 implementation stop reached. Run pentest for this exact commit.`

### v0.6.2 - Deterministic Indexes and Wrap Closure

Goal: make bounded storage layout, iteration, generation reuse, and time
comparison deterministic across constrained targets and adversarial churn.

Deliverables:

- fixed load-factor and maximum-probe contracts for every first-party open-
  addressed index, with insertion/lookup/removal outcomes independent of pointer
  addresses, allocator placement, or platform-default hashing;
- explicit tombstone/stale-entry count and byte debt, bounded cleanup/rehash
  work, deterministic saturation outcome, and no hidden full-table scan;
- storage APIs separate keyed lookup from iteration; protocol output, semantic
  operation identity, audit order, and authorization cannot depend on bucket,
  slab, insertion, tombstone, or unspecified trait iteration order;
- any required enumeration uses a declared stable order or bounded canonical
  selection in caller workspace, with exact overflow behavior and no heap sort;
- stored widths, wire conversion, hashing inputs, counters, and snapshot formats
  produce identical semantics on 16-/32-/64-bit `usize` and both endiannesses
  supported by Rust targets, or reject an unsupported target at compile time;
- wide generation/epoch domains with explicit exhaustion and fail-closed reuse;
  modular `Tick` comparisons declare a maximum horizon below ambiguity and reject
  schedules/lifetimes outside it;
- fixed maximum stack/static memory/alignment for each index and iterator, no
  pointer-width atomics on the local path, no thread-local storage, callback,
  unwinding, ambient clock, hidden allocation, or blocking operation;
- reference models and worst-case operation counts reusable by transactions,
  timers, allocations, permissions, channels, and fast-path inventories.

Verification:

- `cargo test -p gjallarbru-core deterministic_storage`
- Kani/property checks for every load/probe/tombstone boundary, collision chain,
  cleanup interruption, stale handle, generation exhaustion, and Tick wrap horizon
- insertion/bucket/hash-seed/tombstone-layout/word-width/endianness differential
  traces proving byte-identical semantic output and canonical snapshots
- no-allocator freestanding fixtures with stack/static/alignment measurements
  and traps for forbidden atomic/TLS/callback/blocking/unwinding imports
- malicious storage fixtures returning unstable iteration or over-budget work
  must fail qualification without influencing committed core state

Exit criteria:

- Storage churn, layout, target width, and wrap cannot change protocol results or
  exceed declared work/memory bounds; ambiguous reuse/time comparisons fail closed.
- Stop: `v0.6.2 implementation stop reached. Run pentest for this exact commit.`

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
- duplicate/unknown preservation and structural truncation/padding reporting
  without rejecting nonzero receive padding octets.

Verification:

- `cargo test -p gjallarbru-wire attributes`
- property tests for arbitrary attribute sequences and deterministic failure

Exit criteria:

- Unknown and duplicate attributes remain available to later RFC-ordered
  semantic validation.
- Stop: `v0.8.0 implementation stop reached. Run pentest for this exact commit.`

### v0.8.1 - Authenticated Attribute Boundary

Goal: separate byte-preserving diagnostics from the attributes permitted to
influence authenticated STUN semantics.

Deliverables:

- structural padding presence/length validation that accepts arbitrary receive
  padding octets while retaining original covered bytes and emitting zeros;
- a fused iterator whose success always advances by at least one attribute
  header and whose first failure permanently terminates iteration;
- one bounded inventory/pass for duplicates, unknowns, method validation, and
  integrity positions rather than repeated attacker-controlled rescans;
- raw diagnostic visibility for attributes after MESSAGE-INTEGRITY, while the
  authenticated semantic view ignores them except for the RFC-permitted later
  integrity and FINGERPRINT attributes;
- typestate transitions from raw frame through basic STUN and authenticated
  request, preventing unauthenticated values from acquiring method authority.

Verification:

- nonzero padding, truncation, duplicate, post-integrity, and permitted-later-
  attribute corpora with exact original-byte assertions
- iterator progress/fusion properties and scan-count instrumentation at maximum
  attribute count

Exit criteria:

- Diagnostic bytes remain observable without allowing ignored or unauthenticated
  attributes to affect 420 responses, method schemas, policy, or state.
- Stop: `v0.8.1 implementation stop reached. Run pentest for this exact commit.`

### v0.8.2 - Sparse Attribute Inventory

Goal: preserve one-pass semantic evidence without turning a maximum-size STUN
message into a descriptor object for every small attribute.

Deliverables:

- raw borrowed fused iteration remains the complete byte-preserving visibility
  surface and stores no per-attribute heap object or escaping descriptor list;
- fixed bitsets/counters for known presence, duplicate, and schema facts, plus
  exact offsets only for the bounded integrity, fingerprint, and other fields
  that later stages must revisit;
- caller-sized fixed accumulator only for unknown comprehension-required types,
  with deduplication/order policy, exact maximum entries/bytes/work, and no
  accumulation of unknown optional values needed only for raw diagnostics;
- inventory/workspace exhaustion reported as a distinct deterministic resource
  outcome, never mislabeled as structurally malformed wire input and never
  silently truncating a 420 response obligation;
- implementation ceilings below the wire-format theoretical maximum documented
  as profile/resource limits with transport-appropriate drop/error behavior and
  amplification/accounting constraints;
- semantic validators consume the sparse inventory or raw iterator under one
  shared scan budget and cannot trigger backtracking or a second unbounded pass;
- fixed inventory footprint/alignment and operation counts exposed to the
  `v0.2.5` prepared-requirement workspace and later allocation instrumentation.

Verification:

- `cargo test -p gjallarbru-wire sparse_attribute_inventory`
- maximum-count tiny-attribute, all-known, all-unknown-required, all-unknown-
  optional, duplicate-heavy, integrity-position, and mixed-order corpora
- fail-at-every-accumulator-slot tests distinguishing capacity from malformed,
  preserving raw iteration, and producing no partial/truncated semantic view
- allocation/copy/object-count instrumentation proving memory is proportional
  to fixed known metadata plus caller-selected unknown-required capacity, not
  total attribute count
- single-pass/scan-count properties and differential method-validation results
  against a deliberately simple unbounded test oracle

Exit criteria:

- One bounded pass retains every semantic fact needed by core without allocating
  or storing one descriptor per attribute, and capacity limits remain explicit.
- Stop: `v0.8.2 implementation stop reached. Run pentest for this exact commit.`

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
- channel range, declared length, both legal UDP datagram lengths, and stream
  padding rules.

Verification:

- `cargo test -p gjallarbru-wire channel_data`
- round trips across every payload length modulo four

Exit criteria:

- Stream padding is consumed correctly and never counted as peer payload.
- Stop: `v0.15.0 implementation stop reached. Run pentest for this exact commit.`

### v0.15.1 - UDP ChannelData Alignment Closure

Goal: implement RFC 8656 datagram alignment without confusing legal optional
padding with arbitrary trailing data.

Deliverables:

- transport-aware datagram decoding that accepts exactly the declared frame or
  its legal four-byte-aligned padded form;
- byte-preserving diagnostics for legal datagram padding, zero-padding encoding,
  and strict rejection of every other excess length;
- stream behavior kept distinct so mandatory stream alignment cannot leak into
  UDP exactness or payload length.

Verification:

- exhaustive payload-length modulo-four tests for unpadded UDP, padded UDP,
  stream padding, nonzero received padding, and every short/excess length
- datagram/stream differential properties proving payload bytes and consumed
  lengths remain transport-correct

Exit criteria:

- Both RFC-legal UDP encodings interoperate and no arbitrary trailing octet is
  admitted as ChannelData.
- Stop: `v0.15.1 implementation stop reached. Run pentest for this exact commit.`

### v0.16.0 - STUN Encoder Typestate Engine

Goal: build canonical STUN messages through explicit structural typestates so
only a fully finalized plan can transactionally modify caller-visible output.

Deliverables:

- `EncodeDraft -> ValidatedPlan -> FinalizedEncodePlan -> committed output`,
  with construction/validation failures unable to produce a writable plan;
- validation that resolves canonical ordering, exact lengths, capacity,
  padding, adjusted integrity boundaries, every borrowed segment, and typed
  finalizer slots without claiming tags have already been computed;
- plan-bound, non-transferable finalizer slots carrying plan identity, exact
  output length, algorithm/purpose, authenticated range, and dependency node;
- exact-once slot filling plus a bounded acyclic dependency graph requiring
  integrity finalizers in wire order before FINGERPRINT and rejecting missing,
  duplicate, foreign-plan, transferred, substituted, or cyclic finalization;
- sizing, prescribed future HMAC/CRC prefix/range views, finalizer-slot
  placement, and final writing derived from the same validated segment plan;
- a generic bounded finalizer interface and deterministic test finalizers only;
  FINGERPRINT and integrity algorithms populate it in `v0.17.0`-`v0.19.0`;
- only `FinalizedEncodePlan` may write caller-visible bytes, and its fixed
  prepared outputs cannot be changed during the commit operation;
- all provider finalization and every other fallible operation completed before
  caller-visible direct output is modified;
- byte-for-byte unchanged caller output on transactional failure, commit-length
  publication as the final infallible action, and no valid partial frame exposure;
- an explicit fixed caller-provided staging alternative for providers/profiles
  that cannot seal final outputs before writing, separately named and typed;
- accounting that distinguishes expected staging copies from the direct
  sealed-plan path, plus overlap, alias, zeroization, and credential-byte rules.

Verification:

- `cargo test -p gjallarbru-wire encoder`
- compile-fail typestate/slot-transfer fixtures plus sentinel-filled output
  comparisons after failure injected at every planning, dependency, finalization,
  staging, writing, and commit boundary
- missing/duplicate/wrong-plan/wrong-length/wrong-order/cycle properties proving
  only the complete integrity-before-FINGERPRINT graph can finalize
- segment-plan/range equivalence for sizing/HMAC/CRC/write, canonical round trips,
  exact/short/maximum buffers, overlap, and direct-versus-staged copy counters

Exit criteria:

- No draft or merely validated plan can write output; every committed frame
  comes from one exact-once dependency-complete finalized segment plan, and
  failure cannot change caller-visible bytes.
- Stop: `v0.16.0 implementation stop reached. Run pentest for this exact commit.`

### v0.16.1 - Fixed-Workspace Encoder Planning

Goal: prove the encoder's segment/finalizer dependency graph is allocation-free
and caller-bounded before cryptographic finalizers consume it.

Deliverables:

- fixed arrays or caller-provided workspace for segments, padding, borrowed
  ranges, dependency nodes, finalizer slots, prepared fixed outputs, and optional
  scatter entries, with exact size/alignment requirements;
- no per-message `Vec`, `Box`, reference-counted object, dynamically grown
  scatter list, captured closure, heap-created trait object, or recursive graph;
- generic finalizers represented by fixed-size capability/function/state forms
  whose maximum storage, alignment, invocation count, and failure behavior are
  known during validation;
- deterministic `PlanCapacity`/workspace exhaustion distinct from malformed
  protocol input, leaving caller output and all slots unchanged;
- one sizing pass that computes exact nodes/segments/finalizers/output/staging
  bytes without allocating, guessing, retry growth, or repeating attribute scans;
- fixed maximum stack footprint with large plans initialized in place and never
  copied through return values, temporary arrays, or error formatting;
- allocation, copy, segment, dependency-edge, finalizer-call, and retained-byte
  counters available from this milestone rather than deferred to runtime closure.

Verification:

- `cargo test -p gjallarbru-wire encoder_workspace`
- fail allocator enabled before every draft/validate/finalize/commit path plus
  exact/short/zero/maximum caller workspace and output-buffer tests
- compile/API checks rejecting growable containers, captured closures, recursive
  nodes, clone/copy of large plans, and per-message dynamic trait objects
- maximum-segment/dependency/finalizer graphs, capacity failure at each slot,
  cycle/error injection, direct/staged/scatter variants, and unchanged sentinels
- stack/static/alignment and copy-count evidence on supported word widths/MSRV

Exit criteria:

- Every encoder plan and finalizer graph fits declared fixed/caller storage,
  performs no hidden allocation, and fails transactionally at exact capacity.
- Stop: `v0.16.1 implementation stop reached. Run pentest for this exact commit.`

### v0.17.0 - FINGERPRINT Finalization

Goal: implement exact STUN CRC-32 fingerprint framing and integrate it with the
encoder finalization typestate.

Deliverables:

- provider/first-party CRC decision, final-attribute enforcement, and XOR
  constant handling;
- a CRC finalizer that consumes the validated range view, fills the typed
  plan-bound fingerprint slot exactly once, requires all preceding integrity
  nodes, and alone advances that dependency-complete plan toward
  `FinalizedEncodePlan`;
- official, corruption, wrong-position, and duplicate vectors.

Verification:

- `cargo test -p gjallarbru-wire fingerprint`
- RFC 5769 vectors

Exit criteria:

- FINGERPRINT is calculated over the exact required bytes, can only be last,
  and cannot be inserted after caller-visible commit begins.
- Stop: `v0.17.0 implementation stop reached. Run pentest for this exact commit.`

### v0.17.1 - Crypto Provider and Secret Contract

Goal: define narrow, allocation-free cryptographic capabilities and secret
ownership before integrity algorithms become public APIs.

Deliverables:

- separate fixed-output traits for HMAC-SHA-1, HMAC-SHA-256, MD5, SHA-256, and
  entropy, with fixed-size contexts/outputs and incremental fixed-segment input;
- opaque key-handle support plus explicit `Unsupported`, `InvalidKey`,
  `Unavailable`, `StaleGeneration`, and `InternalFailure` outcomes that always fail closed;
- associated purpose-specific key types for message integrity, nonce,
  transaction, reservation, mobility, token, and later domains, without
  `AsRef<[u8]>`, ordinary `Debug`, `Clone`, or equality;
- fixed public validated tag-length types and combined derivation-and-MAC suite
  support so externally held keys need not be exported between providers;
- provider verification or mandatory first-party constant-time comparison for
  public valid tag lengths after computing the complete required MAC and
  comparing every offered byte, with no callback access to protocol policy/state;
- non-Copy/non-Clone-by-default secret wrappers with redacted formatting,
  tightly scoped byte exposure, no ordinary equality, and documented
  best-effort zeroization limits;
- provider qualification rules covering internal allocation, blocking,
  key-copying, logging, output length, and constant-time claims.

Verification:

- compile-time secret trait assertions, redaction/log tests, provider
  substitution, fixed-output mismatch, unavailable/failure, and opaque-key tests
- cross-purpose key substitution, prohibited export/Debug/Clone/equality,
  complete-MAC/all-tag-byte comparison, public invalid-length, stale generation,
  combined-suite, and no-algorithm-fallback tests
- no_std/MSRV checks plus allocation instrumentation for every first-party provider path

Exit criteria:

- Protocol code cannot select arbitrary algorithms through one broad enum,
  export secrets by convenience, or treat provider failure as authentication.
- Stop: `v0.17.1 implementation stop reached. Run pentest for this exact commit.`

### v0.17.2 - Synchronous and External Crypto Split

Goal: prevent synchronous packet cryptography from hiding I/O, blocking,
ambient entropy, allocation, or nondeterministic external-provider behavior.

Deliverables:

- packet hash/HMAC/derivation providers required to be deterministic,
  synchronous, bounded, nonblocking, allocation-qualified, and free of ambient entropy;
- opaque handles permitted only when their synchronous use satisfies the same
  contract and never conceals HSM/KMS/network/storage I/O;
- external HSM/KMS operations represented as bounded generation-tagged
  command/completion operations with timeout, cancellation, retry, and stale handling;
- provider-local mutable state and nondeterministic results prohibited from
  affecting the reducer unless their exact result arrives as an explicit event;
- qualification metadata distinguishing software packet providers, local
  synchronous hardware, and asynchronous external key services.

Verification:

- blocking/allocation/ambient-randomness trap providers must fail qualification
- asynchronous HSM/KMS model tests for duplicate/reordered/stale completions,
  timeout, cancellation, shutdown, unavailable service, and deterministic replay

Exit criteria:

- An opaque key handle cannot weaken reducer determinism or conceal an external
  operation inside a packet-path trait call.
- Stop: `v0.17.2 implementation stop reached. Run pentest for this exact commit.`

### v0.17.3 - External Packet-Crypto Input Ownership

Goal: close message ownership before any asynchronous external provider can
authenticate packet bytes.

Deliverables:

- the base STUN/TURN profiles keep packet HMAC and digest work in qualified
  synchronous providers; external HSM/KMS is limited to key provisioning,
  wrapping, rotation, or management unless a separate packet-crypto profile is enabled;
- any admitted asynchronous packet-crypto operation retains the exact immutable
  authenticated segment sequence through a generation-tagged message lease or
  bounded runtime-owned copy;
- byte, operation, tenant, worker, timeout, cancellation, retry, and shutdown
  ceilings for pending packet-crypto input and prepared output;
- completion bound to message, path, transaction, algorithm, key generation,
  operation generation, buffer generation, and provider generation;
- no borrowed receive/input slice escaping a transition, no buffer reuse before
  completion, and deterministic cleanup on stale, cancelled, timed-out, failed,
  disconnected, or shutdown operations;
- copy/lease accounting distinguishes asynchronous provider retention from the
  synchronous direct packet path.

Verification:

- compile-fail borrow fixtures plus message-buffer reuse, stale completion,
  timeout, cancellation, retry, provider restart, disconnect, and shutdown models
- exact-segment differential HMAC tests and byte/operation/copy/lease exhaustion
  assertions for every admitted asynchronous profile

Exit criteria:

- Base packet authentication remains synchronous, and no asynchronous exception
  can outlive, alias, or exceed the bounded ownership of its exact message bytes.
- Stop: `v0.17.3 implementation stop reached. Run pentest for this exact commit.`

### v0.18.0 - Legacy Message Integrity

Goal: support legacy long-term credentials without making them the modern core.

Deliverables:

- reviewed MD5 key-derivation and HMAC-SHA-1 provider boundaries;
- exact adjusted-length verification/encoding and constant-time comparison;
- a legacy-HMAC finalizer that consumes only validated segment/range views and
  fills its plan-bound typed slot exactly once before FINGERPRINT and before
  `FinalizedEncodePlan` may commit.

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
- RFC 8489 integrity ordering, algorithm negotiation inputs, and errata decisions;
- a SHA-256 finalizer that consumes only validated segment/range views and
  fills its plan-bound slot exactly once and proves every required integrity
  dependency precedes the final FINGERPRINT slot before commit.

Verification:

- `cargo test -p gjallarbru-crypto -p gjallarbru-wire sha256_integrity`
- official/project KATs, downgrade, truncation, and mixed-integrity vectors

Exit criteria:

- SHA-256 is the hardened profile and legacy fallback is never implicit.
- Stop: `v0.19.0 implementation stop reached. Run pentest for this exact commit.`

### v0.19.1 - Integrity Failure Closure

Goal: make every integrity range, truncation, provider, and response-key
uncertainty explicit and fail closed.

Deliverables:

- scatter input over original header bytes, synthetic adjusted length, and
  original bytes through the exact integrity boundary without packet mutation/copy;
- MESSAGE-INTEGRITY-SHA256 length policy admitting only usage-permitted
  16-to-32-byte values in four-byte increments;
- mixed legacy/modern attribute, ordering, algorithm, key-generation, key-ID,
  output-length, and downgrade rejection matrices;
- mandatory failure when a required response-integrity key cannot be selected
  or a provider returns unsupported, unavailable, stale, or internal failure;
- constant-time comparison claims scoped to valid public lengths and backed by
  provider review rather than inferred from a trait signature; the complete
  required MAC is computed and every offered byte compared without early exit,
  while structurally invalid public lengths may fail before secret work.

Verification:

- original-byte scatter versus reference-copy differential vectors, including
  adjusted header lengths and post-integrity bytes
- every truncation length, provider error, stale key, mixed-integrity ordering,
  downgrade, and missing-response-key negative fixture
- instrumentation/test-provider evidence for complete MAC computation and
  all-offered-byte comparison on every valid public tag length

Exit criteria:

- No malformed length, provider ambiguity, or key-selection failure can produce
  an authenticated request or an unauthenticated success response.
- Stop: `v0.19.1 implementation stop reached. Run pentest for this exact commit.`

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

### v0.22.1 - Wire Resource and Typestate Closure

Goal: close algorithmic, allocation, copy, and validation-stage hazards before
stateful server work consumes the wire APIs.

Deliverables:

- enforced message, attribute, scan, cryptographic-operation, recursion, and
  backtracking ceilings with linear-work evidence for admitted frames;
- fail-after-startup allocator and copy counters covering errors, unknown lists,
  stream retention, integrity, Unicode adapters, and response construction;
- `v0.8.2` sparse fixed known-attribute bitsets/counters/selected offsets plus
  caller-bounded unknown-required accumulation, never one descriptor per attribute;
- `v0.16.1` fixed/caller-workspace segment, dependency, finalizer, and scatter
  planning with transactional `PlanCapacity` behavior;
- typed transitions from `FrameView` through basic, authenticated, and
  method-valid views;
- fuzz targets promoted from every parser milestone plus corpora for nonzero
  padding, post-integrity attributes, truncated tags, and all boundary lengths.

Verification:

- maximum-size work counters and adversarial repeated-attribute complexity tests
- fail-allocator/copy-count tests, typestate compile-fail fixtures, fuzz smoke,
  Miri-safe borrowed-view tests, and guaranteed iterator termination
- maximum-attribute sparse-inventory and maximum encoder-graph workspace tests
  proving capacity outcomes remain distinct from malformed protocol input

Exit criteria:

- Wire APIs expose only bounded validation stages, and claimed no-allocation/
  zero-copy paths have executable evidence rather than convention.
- Stop: `v0.22.1 implementation stop reached. Run pentest for this exact commit.`

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

### v0.23.1 - Atomic Deterministic Reducer

Goal: implement the v0.2.1 reducer contract so a transition is either fully
planned or observationally absent.

Deliverables:

- byte-identical command and resulting-state replay for identical configuration,
  ordered event/path identities and generations, supplied times, entropy bytes,
  provider completions, storage seed/layout inputs, output capacities, and every
  other field frozen by the `v0.2.4` executable input envelope;
- preflight of command count, encoded bytes, leases, and reservations before
  mutation, with `OutputCapacity` leaving state and outputs unchanged;
- runtime execution rule forbidding command consumption until `step` succeeds,
  including rollback-free response encoding failure;
- explicit ordered time events with equal/decreasing/wrap behavior and separation
  of monotonic lifetimes from absolute credential validity;
- purpose-bound entropy request/completion and generation-tagged lease/operation
  events that make duplicate, delayed, and stale results inert;
- capability command types constraining the endpoints, lifetime, quota, key
  domain, and other fields available to conforming adapters, with safe-reference
  differential verification rather than a claim about malicious runtime behavior.
- iteration/insertion/tombstone order, hash layout, pointer addresses, `usize`
  width, endianness, allocator placement, and runtime correlation IDs forbidden
  from affecting command/state bytes or semantic operation identity.

Verification:

- snapshot/replay properties across event sequences and every capacity boundary
- `v0.2.4` replay corpus across storage layouts, word widths, correlation IDs,
  configuration/path generations, and reordered arrival with explicit event order
- fault injection at each preflight/encode/entropy/provider/lease stage proving
  state, counters, command sinks, and runtime side effects remain unchanged

Exit criteria:

- Partial command emission, implicit randomness/time, and adapter-widened
  authority are unrepresentable to conforming adapters through the core
  transition API and differentially verified at runtime boundaries.
- Stop: `v0.23.1 implementation stop reached. Run pentest for this exact commit.`

### v0.23.2 - Prepared Transition and Atomic Admission

Goal: compute exact semantic effect requirements once before adapter capacity acquisition
without repeating parsing, authentication, encoding, or attacker-controlled scans.

Deliverables:

- one bounded preparation pass into caller-provided fixed workspace producing a
  non-`Clone` `PreparedTransition` with immutable planned state changes, commands,
  and exact `TransitionRequirements`;
- single-consume, worker-local, normally `!Send`/`!Sync` ownership that cannot
  survive an await, callback return, receive-buffer reuse, or synchronous
  prepare/acquire/commit scope without an explicit bounded message/workspace lease;
- binding to input-buffer, derived-key, output-plan, state, configuration, and
  worker generations, with stale/reused generations unable to commit;
- deterministic scrubbing of derived keys, integrity tags, nonces, and
  credential-derived response material on discard, failure, cancellation, or commit;
- explicit stack/static footprint and alignment ceilings with compile-time
  non-copy/non-clone assertions for large preparation workspaces;
- preparation bound to event identity, state revision, configuration generation,
  and worker epoch so stale plans cannot commit after any relevant change;
- exact requirements for command kinds/counts, encoded bytes, retained leases/
  buffers, semantic/control obligations, alignment, and commit workspace, with
  no queue topology, wakeup, atomic, executor, provider-lane, or OS-submission type;
- adapter-owned capacity acquisition only after preparation, with bounded
  declared work and no
  retry loop that reparses, reauthenticates, re-HMACs, rescans, or replans input;
- fixed limits for preparation workspace/time/operations and deterministic
  failure when the event cannot be represented within them;
- one commit API consuming the prepared transition into an exactly sufficient
  caller command arena under the opaque `v0.2.5` adapter reservation; partial
  arena acceptance is prohibited while later OS execution remains non-atomic.

Verification:

- instrumentation proving each parser, integrity, policy, lookup-planning,
  encoder-planning, and requirement calculation runs at most once per event
- exact-requirement properties across every event kind and capacity boundary
- compile-fail escape/Send/Sync/Copy fixtures plus buffer-reuse, await/callback,
  derived-key/output-plan generation, scrubbing, stack-size, and lease tests
- stale-plan, adapter-reservation race, insufficient arena, oversized-workspace, and
  adversarial partial-accept tests leaving state and queues unchanged

Exit criteria:

- Every adapter reservation is sized from one worker-local single-consume prepared
  transition; core remains topology-neutral and admission never repeats attacker
  work, leaks a borrow/secret, or guesses by retry.
- Stop: `v0.23.2 implementation stop reached. Run pentest for this exact commit.`

### v0.23.3 - Linear Capacity Reservation and Operation-ID Authority

Goal: make adapter capacity reservation single-use and generation-bound while
assigning all semantic operation identity exclusively to deterministic core.

Deliverables:

- a non-`Clone`, non-reusable adapter-owned capacity reservation exactly matching
  one prepared transition and caller command arena, opaque to semantic core logic;
- explicit limits for outstanding reservations and total reserved bytes/slots at
  global, worker, and queue scopes, with bounded acquisition work and no
  incremental reservation/queue-capacity hoarding;
- queue/provider generations, topology, wakeups, publication state, and runtime
  correlation IDs remain in the adapter envelope; core validates only opaque
  reservation/arena identity, exact sufficiency, and single-consume state;
- automatic exactly-once release after failed commit, cancellation, reservation
  drop, shutdown, queue restart/resize, worker replacement, or stale rejection;
- semantic operation IDs generated only by core from an explicit engine/worker
  epoch plus bounded generational counter, with exhaustion/wrap failing closed;
- runtime, queue, provider, and transport correlation IDs kept outside reducer
  equality and forbidden from changing protocol behavior or authorization;
- exact reservation capacity and topology hidden from semantic decisions beyond
  successful requirement satisfaction, preserving byte-identical replay.

Verification:

- compile-time non-clone/single-consume checks plus reuse, double-release,
  reservation-drop, failed-commit, cancellation, shutdown, queue-resize/restart,
  worker-replacement, stale-generation, and reservation-hoarding models
- semantic-ID uniqueness, epoch change, counter exhaustion/wrap, stale
  completion, and correlation-ID substitution tests
- replay tests proving runtime correlation IDs and queue layout cannot change
  state, commands, semantic IDs, or authorization

Exit criteria:

- No capacity reservation can be reused, leaked, or hoard capacity, core depends
  on no queue design, and no runtime-provided identifier becomes protocol authority.
- Stop: `v0.23.3 implementation stop reached. Run pentest for this exact commit.`

### v0.23.4 - Atomic Publication Memory Model

Goal: define portable state/command visibility without requiring a transaction
across independently mutable memory structures.

Deliverables:

- mutable core state exclusively owned by one worker, with no concurrent direct
  state reads or writes from runtime consumers;
- commands written into the adapter-reserved caller arena before the prepared
  state mutation is completed, without core knowing its eventual queue topology;
- one adapter-owned infallible ready-arena publication after state mutation;
  threaded adapters use release ordering and acquire consumption while local/
  custom adapters use equivalent mechanics without atomics;
- owner-generated immutable/versioned snapshots as the only cross-thread state
  inspection path, published independently without widening command authority;
- worker epoch invalidation for crashes before publication, abandoned reserved
  slots, stale snapshots, restarts, and ownership transfer;
- a safe single-thread reference adapter plus Loom/model representation of the
  publication protocol and memory-order assumptions.

Verification:

- Loom/model tests for every interleaving around reserved-arena writes, state
  mutation, ready publication, acquire consumption, snapshot, crash, and restart
- fault injection before and after every publication boundary proving consumers
  never observe commands without committed owner state or partial batches
- safe-reference differential tests and platform concurrency sanitizer runs

Exit criteria:

- Cross-thread consumers observe only complete ready batches, core state remains
  worker-owned, and pre-publication crashes invalidate both prepared sides.
- Stop: `v0.23.4 implementation stop reached. Run pentest for this exact commit.`

### v0.23.5 - Composable Runtime Effect Envelope

Goal: compose semantic authority, resource ownership, delivery guarantee, and
durability/audit obligations without forcing one mutually exclusive class.

Deliverables:

- one typed composite envelope with orthogonal semantic-authority,
  retained-resource ownership, delivery-guarantee, durability/audit, and
  chargeable-work properties, plus validation of legal/illegal combinations;
- authoritative relay open/close, credential lookup, external crypto, and
  similar state decisions with core-owned operation IDs and semantic completions;
- retained buffer/lease ownership that releases exactly once on completion,
  delivery failure, cancellation, stale result, permit rollback, or shutdown
  without implying protocol success;
- best-effort datagram delivery whose runtime acceptance may be terminal for
  semantic state while still retaining a buffer, charging quota, and producing
  bounded security-audit evidence;
- bounded lossy observability with drop counters and separately configured
  durable/bounded security-audit policy and explicit overload behavior;
- per-property idempotency, queue, byte, timeout, cancellation, shutdown, retry,
  completion, terminal-accounting, and cross-property composition rules.

Verification:

- property cross-product tests proving only semantic authority changes pending
  protocol state and only ownership retains/releases payload resources
- delivery-failure tests proving one retained buffer is released exactly once
  without manufacturing a semantic delivery completion
- packet-flood tests proving delivery/metrics do not exhaust authoritative
  operation tables; audit overload/durability/fail-closed policy tests

Exit criteria:

- Hot-path sends can combine delivery, ownership, quota, and audit obligations
  without inventing protocol authority or losing any terminal accounting.
- Stop: `v0.23.5 implementation stop reached. Run pentest for this exact commit.`

### v0.23.6 - Chargeable-Work Accounting

Goal: make occupancy, attempted work, valid completion usage, and retries charge
the correct authority exactly once without attacker-controlled refunds.

Deliverables:

- occupancy reservations charged at resource admission and released exactly
  once only when the buffer, slot, lease, or other occupancy actually ends;
- attempt charges consumed when work is accepted and never refunded because a
  send/provider/OS action later fails, times out, or is cancelled;
- completion usage recorded only from a valid generation-bound semantic
  completion, with duplicates, stale results, and correlation-only events inert;
- retry policy making every retry a new attempt charge unless an explicit
  bounded idempotency budget ties it to the original semantic operation;
- separate counters/ledgers for reserved occupancy, consumed attempts,
  completion-derived usage, retry consumption, refunds, and rejected work;
- saturation, rollback, compensation, shutdown, and reconciliation rules that
  cannot double-charge, undercharge, or revive released quota authority.

Verification:

- send/provider failure and cancellation matrices proving occupancy releases
  once while attempt charges remain consumed and no false completion is recorded
- duplicate/stale/reordered completion plus retry/idempotency properties across
  quota exhaustion, counter saturation, crash, shutdown, and reconciliation
- adversarial tests attempting refund loops, retry bypass, double completion,
  correlation-ID substitution, and occupancy leaks

Exit criteria:

- Every charge has one declared lifecycle, and failures or retries cannot refund
  attacker-driven work, bypass quota, or double-count valid usage.
- Stop: `v0.23.6 implementation stop reached. Run pentest for this exact commit.`

### v0.23.7 - Authoritative Control-Lane Progress

Goal: guarantee bounded terminal progress for admitted authoritative work even
when hostile packet traffic fills ordinary delivery and ingress capacity.

Deliverables:

- event classification separating droppable client ingress/delivery from
  authoritative completions, revocations, expiries, cancellations,
  compensation, shutdown reconciliation, and ownership releases;
- admission of every authoritative external operation reserves its worst-case
  terminal completion, compensation, cancellation, and resource-release slots;
- reservation for the complete transitive effect closure: completion-generated
  commands, compensation of compensation, completion/cancellation races,
  ownership release, audit consequences, and required terminal error responses;
- an acyclic effect graph with explicit maximum depth, nodes, commands, bytes,
  retained resources, and terminal paths calculated at operation admission;
- one bounded per-operation terminal mailbox/coalescer so duplicate, stale, or
  racing completion observations do not consume new control slots indefinitely;
- separate finite control-lane reserves for expiry/revocation progress and
  shutdown, with global, worker, and operation ceilings;
- packet sends, new client events, metrics, and best-effort delivery forbidden
  from consuming control-lane capacity;
- deterministic reserve consume/release/refill, stale/duplicate event handling,
  and fail-closed operation admission when terminal progress cannot be reserved;
- fairness among control event kinds without an unbounded priority queue or
  starvation of cleanup needed to free ordinary queues.

Verification:

- queue-saturation models where relay/credential/crypto completions,
  revocations, expiry, cancellation, compensation, shutdown, and ownership
  release arrive while every ordinary packet/delivery slot is full
- reserve exhaustion, duplicate/stale completion, nested compensation,
  compensation-of-compensation, completion/cancellation race, terminal mailbox,
  graph-depth/node/byte limit, operation admission rollback, and fairness properties
- proof that packet floods cannot consume or indefinitely postpone reserved
  terminal work and that every admitted operation reaches one accounted terminal state

Exit criteria:

- No authoritative operation is admitted without bounded terminal progress
  for its complete acyclic effect closure, and packet pressure cannot deadlock cleanup.
- Stop: `v0.23.7 implementation stop reached. Run pentest for this exact commit.`

### v0.23.8 - Bounded Observation Snapshots

Goal: expose cross-thread operational state without granting authority or
creating unbounded RCU-style retention under slow readers.

Deliverables:

- fixed maximum snapshot bytes, item counts, publication frequency, and
  generation count per worker/listener/tenant observation domain;
- redaction excluding keys, credentials, packet bodies, raw tenant identities,
  capability-bearing handles, and other authorization/completion material;
- binding to schema, configuration generation, and worker epoch, with explicit
  stale/overrun results after reload, restart, ownership replacement, or retention expiry;
- bounded reader leases/references, reclamation work, and stalled-reader policy
  that cannot pin unbounded snapshot generations or worker resources;
- snapshots forbidden as authorization, reducer input, completion validation,
  recovery input, or proof of current allocation/resource existence;
- owner-only construction and immutable release/acquire publication compatible
  with the `v0.23.4` memory model.

Verification:

- size/frequency/cardinality/redaction tests plus secret/capability scanning of
  serialized and in-memory snapshot fixtures
- stalled/crashed/slow reader, generation rollover, reload, restart, ownership
  transfer, and reclamation-budget models
- compile/API tests proving snapshots cannot be passed where live authority,
  semantic IDs, capabilities, or completion evidence are required

Exit criteria:

- Observation remains fixed, redacted, stale-detectable, and non-authoritative,
  and no reader can force unbounded state retention or worker cleanup work.
- Stop: `v0.23.8 implementation stop reached. Run pentest for this exact commit.`

### v0.23.9 - Post-Publication Crash Reconciliation

Goal: account for every accepted batch and external resource across crashes
after ready publication, including partial execution and lost completions.

Deliverables:

- an explicit recovery matrix for crash after ready publication but before
  execution, during partial batch execution, and after an OS resource opens
  before its completion reaches core;
- declared queue-survival and queue-loss behavior for worker-thread, worker-
  process, and whole-process restart boundaries;
- accepted-batch state tracking sufficient to execute/reconcile idempotent
  surviving work or emit deterministic cancellation/uncertain-result events;
- reconciliation/cancellation events only when authoritative core state
  survives a thread or worker-runtime restart and can consume those events;
- whole-process base-profile restart explicitly loses all prior allocation,
  permission, channel, transaction, relay, and delivery authority rather than
  adopting or reconstructing it;
- surviving relay sockets, provider operations, descriptors, buffers, and
  leases fenced, quarantined, inventoried, and closed after process loss;
- non-idempotent datagram delivery with unknown execution status never replayed,
  attempt charges kept consumed, and no delivery success inferred;
- any future persistent accepted-batch journal classified as runtime
  infrastructure requiring a separate durable-authority release profile, never
  as a requirement of the portable no_std engine;
- runtime resource fencing and bounded restart inventory for relay sockets,
  descriptors, provider operations, buffers, leases, and other external ownership;
- exactly-once buffer/lease cleanup across runtime crash, queue loss, stale
  completion, restart, cancellation, and reconstructed resource discovery;
- worker-epoch rejection of stale published batches, correlation IDs,
  completions, resource handles, and ownership releases;
- foundational adapter contract only; production supervision and availability
  SLO implementation remain in `v0.66.1`.

Verification:

- crash injection at every instruction boundary from ready publication through
  command start, partial execution, OS success, completion enqueue, core receipt,
  ownership release, and terminal accounting
- queue survives/queue lost, resource survives/resource lost, worker restart,
  process restart, stale batch/completion, duplicate inventory, and fencing models
- process-death tests proving old allocation/relay authority is never adopted,
  unknown non-idempotent sends are not replayed, surviving resources close, and
  consumed attempt charges are not refunded or converted into success
- differential reference-runtime tests proving every accepted batch ends in
  execution/reconciliation or deterministic cancellation while authority
  survives, or fenced cleanup without adoption after whole-process loss

Exit criteria:

- No accepted batch, opened resource, buffer, lease, or old-epoch completion
  becomes unaccounted after any post-publication crash boundary, and whole-
  process restart cannot inherit node-local authority from the dead process.
- Stop: `v0.23.9 implementation stop reached. Run pentest for this exact commit.`

### v0.23.10 - Portable Publication Adapters

Goal: keep concurrency and memory-order machinery out of the portable core API
while preserving one publication contract across threaded and local runtimes.

Deliverables:

- `gjallarbru-core` requirements, prepared transitions, state, events, commands,
  capabilities, and snapshots contain no adapter reservation/topology types or
  atomics and require neither `Send` nor `Sync`;
- publication/consumption traits owned by runtime adapters, not the reducer or
  public no_std core data model;
- a single-thread/no-atomic adapter committing and consuming locally with no
  fences, atomic types, threads, tasks, or synchronization dependency;
- threaded adapters selected behind `target_has_atomic` capability checks with
  explicit release/acquire ready-marker behavior;
- compile support for representative targets without pointer-width atomics and
  clear unsupported accelerated/runtime feature diagnostics;
- scalar/local versus threaded/atomic differential semantics for acceptance,
  ordering, crash reconciliation, snapshots, and control-lane progress.

Verification:

- no-atomic target compile fixtures and source/API checks excluding atomics,
  `Send`/`Sync` bounds, and threading imports from publishable core crates
- local adapter unit/model tests plus Loom/threaded adapter interleavings
- identical event/state/command/semantic-ID snapshots across local and threaded
  adapters, including failure and crash-reconciliation traces

Exit criteria:

- Bare-metal and single-thread consumers need no atomics or thread traits, while
  threaded runtimes provide equivalent publication and recovery behavior.
- Stop: `v0.23.10 implementation stop reached. Run pentest for this exact commit.`

### v0.23.11 - Terminal Mailbox Race Semantics

Goal: give every cancellation/completion race one bounded deterministic
terminal outcome without treating cancellation intent as OS cancellation proof.

Deliverables:

- a mailbox state machine with `Pending`, `CancelRequested`, `Succeeded`,
  `Failed`, `Cancelled`, and `Uncertain` states plus an explicit legal
  transition table for every external-operation class;
- cancellation request records intent, blocks forbidden new handoff, and emits
  cancellation work where supported, but never alone proves that OS/provider
  execution stopped;
- per-operation policy declaring whether a generation-valid success after
  `CancelRequested` wins, becomes uncertain, or is rejected as impossible;
- identical duplicate terminal observations coalesced without new slots,
  charges, cleanup, audit, or state transitions;
- conflicting generation-valid terminal observations fail closed into one
  deterministic `Uncertain` reconciliation path rather than first-arrival wins;
- exact ownership release, attempt/completion accounting, response, audit,
  compensation, and late-event behavior for every legal and illegal transition;
- terminal state immutable except through an explicitly modeled reconciliation
  result that cannot revive expired/revoked semantic authority.

Verification:

- exhaustive state/transition table tests for every operation class and
  permutation of cancel request, OS handoff, success, failure, cancellation,
  timeout, duplicate, stale, and contradictory observations
- model checking of cancellation/success races proving one cleanup, one audit,
  no false cancellation, no false success, no attempt refund, and bounded slots
- crash/restart and control-lane saturation tests integrating `v0.23.7` and
  `v0.23.9` uncertainty/reconciliation behavior

Exit criteria:

- Cancellation intent is never confused with external cancellation, duplicate
  terminals are inert, and conflicting valid evidence reaches one bounded
  fail-closed reconciliation outcome.
- Stop: `v0.23.11 implementation stop reached. Run pentest for this exact commit.`

### v0.23.12 - Acknowledged Authority Fences

Goal: make revocation-before-reuse an explicit acknowledged protocol across
every runtime execution lane rather than an assumption about FIFO queue order.

Deliverables:

- a monotonic `FenceId`/authority sequence per execution domain, with wrap,
  restart, persistence, and domain-replacement behavior defined fail closed;
- every delivery, resource, provider, and fast-path command bound to the
  authority sequence current at authorization/publication;
- revocation advances the sequence and emits one bounded fence command whose
  completion requires acknowledgement from every applicable queue, submission
  ring, provider lane, socket worker, and kernel/accelerated lane;
- identifier, endpoint, permission/allocation slot, connection/session,
  operation, lease, and buffer-generation reuse remains invisible until all
  required ordering acknowledgements are validated and `v0.23.15` separately
  proves any externally reachable physical ownership releasable;
- acknowledgements bound to execution-domain, worker, configuration, command,
  and fence generations, with duplicate/stale/forged/wrong-lane results inert;
- missing, timed-out, lost, or uncertain acknowledgement destroys/quarantines
  the old execution domain or advances to a disjoint generation whose identity
  space cannot alias the unacknowledged domain; physical release after
  destruction requires `v0.23.17` typed quiescence evidence;
- no safety dependence on FIFO ordering, best-effort cancellation, queue drain,
  provider convention, or wall-clock delay;
- portable core fence values and state require no atomics; local and threaded
  runtime adapters implement equivalent acknowledgement semantics.

Verification:

- `cargo test -p gjallarbru-core authority_fence`
- model tests across multiple queues, reordered fence/data commands, full
  queues, worker/provider/kernel loss, duplicate/stale acknowledgement,
  generation wrap, restart, and identifier/buffer reuse
- local versus threaded adapter differential traces plus Loom models proving
  reuse is never visible while an older execution lane may retain authority
- fault tests proving missing acknowledgement causes quarantine plus typed
  quiescence/domain destruction or disjoint-generation replacement, never
  optimistic continuation or storage reuse

Exit criteria:

- Every authority revocation is acknowledged by all relevant execution lanes
  before semantic reuse; physical reuse additionally requires terminal
  ownership release under `v0.23.15`.
- Stop: `v0.23.12 implementation stop reached. Run pentest for this exact commit.`

### v0.23.13 - Bounded Fence Watermarks

Goal: keep revocation storms bounded and scoped while one or more execution
lanes are still acknowledging an earlier authority fence.

Deliverables:

- one fixed-capacity pending high-water `FenceId` per registered execution lane,
  with no per-revocation queue item, waiter, future, or control-slot growth;
- monotonic coalescing: repeated advances replace the required watermark with
  the newest value while preserving every older reuse barrier;
- acknowledgement of fence `F` defined precisely as every command through `F`
  being handed off and tracked, rejected before handoff, or terminally
  reconciled—not merely read, dequeued, cancelled, or submitted—and never as
  proof that tracked in-flight ownership has ended;
- a fixed-capacity execution-lane registry with lane identity/generation,
  maximum lanes per domain, and deterministic exhaustion behavior;
- a lane added during a pending fence starts beyond the captured watermark and
  cannot receive commands from the older authority interval;
- lane removal requires acknowledgement/drain or destruction/quarantine of its
  execution domain before semantic identity reuse, while physical resources
  additionally require `v0.23.17` typed quiescence evidence;
- ordering `FenceId` separated from allocation, permission, channel, path,
  policy, buffer, and other semantic object generations;
- explicit fence scope and blast radius per execution-domain type, with coarse
  worker-wide invalidation permitted only when deliberately configured,
  documented, capacity-tested, and never implied by sequence comparison;
- control-lane reserve/accounting for the one coalesced fence state and its
  acknowledgements integrated with `v0.23.7`.

Verification:

- `cargo test -p gjallarbru-core fence_watermark`
- revocation-storm models with repeated/nested object invalidation while every
  lane is delayed, reordered, lost, replaced, or acknowledging older watermarks
- lane add/remove/reuse, registry exhaustion, generation wrap, domain restart,
  coalescing, and wrong-lane/stale acknowledgement tests
- mixed unrelated allocations/permissions proving narrow revocation does not
  stale unrelated commands unless the declared coarse blast radius requires it
- fixed-slot/counter assertions proving revocation frequency cannot increase
  pending fence memory, tasks, queues, or control-lane operations without bound

Exit criteria:

- Each lane has one bounded coalesced required watermark, acknowledgement has
  one exact meaning, and semantic authority outside the declared fence scope
  remains unaffected.
- Stop: `v0.23.13 implementation stop reached. Run pentest for this exact commit.`

### v0.23.14 - Nonterminal Timeout Observations

Goal: ensure local deadline expiry initiates recovery without inventing proof
that an external operation failed, stopped, or was successfully cancelled.

Deliverables:

- `DeadlineExceeded` as a nonterminal mailbox observation/state distinct from
  `Failed`, `Cancelled`, and `Uncertain`;
- operation-specific transition from `Pending` to `DeadlineExceeded` and then
  cancellation request and/or reconciliation work under reserved control capacity;
- timeout never records external failure/completion usage, releases external
  ownership prematurely, refunds an attempt, or proves OS/provider cancellation;
- generation-valid success/failure/cancel observations arriving after timeout
  handled by the same declared operation policy as observations racing an
  explicit `CancelRequested`;
- repeated local timers and duplicate deadline observations coalesced without
  additional terminal slots, audit events, cancellation commands, or charges;
- timeout versus shutdown, revocation, crash, fence, resource inventory, and
  compensation ordering integrated with `v0.23.7`, `v0.23.9`, and `v0.23.11`;
- distinct external/provider timeout completions allowed only when the provider
  contract proves their terminal meaning rather than inheriting local timer semantics.

Verification:

- exhaustive mailbox transitions for timeout before/after handoff, cancellation
  request, success, failure, provider cancellation, crash, and reconciliation
- valid late-success policies for send, open, close, credential, crypto, and
  provider operations plus contradictory-result uncertainty tests
- repeated/stale timer, clock jump, shutdown, revocation, and full-control-lane
  models proving one cancellation/reconciliation path and one final terminal state

Exit criteria:

- A local timeout is never terminal evidence; it starts bounded recovery while
  preserving truthful handling of every later generation-valid observation.
- Stop: `v0.23.14 implementation stop reached. Run pentest for this exact commit.`

### v0.23.15 - Fence and Ownership Separation

Goal: ensure fence acknowledgement stops future handoff without prematurely
releasing physical resources still reachable by external in-flight work.

Deliverables:

- four separate lifecycle facts represented explicitly: fence ordering
  acknowledgement, external in-flight tracking, semantic identity/generation
  reuse eligibility, and physical ownership release;
- acknowledgement of `FenceId F` means no command through `F` remains capable
  of a new handoff in the acknowledged lane, but says nothing by itself about
  completion or external reachability of already-handed-off commands;
- buffers, descriptors, sockets, leases, provider plaintext/ciphertext storage,
  operation slots, registered files/buffers, and kernel references remain
  pinned while an old external operation may read, write, complete, or cancel;
- physical release occurs only after a generation-valid terminal result,
  deterministic reconciliation/inventory proof, or a `v0.23.17` typed
  quiescence proof establishes that the external domain is unreachable;
- semantic identifiers may advance to a disjoint generation after ordering is
  fenced, but backing storage, descriptor numbers, pointer-bearing leases, and
  provider slots cannot alias old externally reachable objects;
- separate bounded ledgers/counters for fence-acknowledged work, external
  in-flight work, logically retired identities, quarantined physical ownership,
  and finally reusable storage;
- shutdown, crash, timeout, provider loss, partial batch, and fast-path
  reconciliation preserve the same separation without optimistic release.

Verification:

- `cargo test -p gjallarbru-core fence_ownership`
- state/model tests for every ordering/in-flight/semantic/physical combination,
  including acknowledgement before late success/failure/cancel/uncertain results
- buffer/descriptor/provider-slot reuse adversary tests proving disjoint
  identifiers cannot alias still-reachable storage
- local, threaded, batched, `io_uring`, provider, and fast-path differential
  traces with exact ownership counters and one terminal release

Exit criteria:

- Fence acknowledgement can permit only safe semantic progress; no physical
  resource becomes reusable until external reachability has ended and ownership
  is terminally reconciled.
- Stop: `v0.23.15 implementation stop reached. Run pentest for this exact commit.`

### v0.23.16 - Bounded Unresolved Recovery

Goal: prevent nonresponsive runtimes/providers from retaining every terminal
mailbox, resource, and admission slot indefinitely after timeout/cancellation.

Deliverables:

- per-operation maximum cancellation attempts, reconciliation rounds, unresolved
  monotonic age, retained bytes/resources, and terminal control work;
- fixed global, worker, execution-domain, provider, tenant, and operation-class
  counts for `DeadlineExceeded`, `CancelRequested`, and unresolved `Uncertain` work;
- deterministic escalation to `Uncertain` when any attempt/round/age budget is
  exhausted, without inventing success, failure, or cancellation evidence;
- quarantine or destruction/restart of the affected provider/execution domain,
  with new work blocked until the domain is healthy or replaced by a disjoint generation;
- logical state/capacity retirement rules that keep externally reachable
  buffers/descriptors/leases/provider storage physically non-aliasing under `v0.23.15`;
- a separate fixed emergency/replacement reserve allowing bounded service
  recovery without reusing quarantined storage or silently evicting another
  unresolved operation;
- deterministic admission failure when unresolved/emergency capacity is full,
  plus operator/audit signals and recovery only through terminal reconciliation,
  inventory proof, or `v0.23.17` typed quiescence proof;
- no LRU/age eviction, forced false terminal result, counter reset, or mailbox
  overwrite used to regain capacity.

Verification:

- `cargo test -p gjallarbru-core unresolved_recovery`
- providers that never respond, ignore cancellation, return indefinitely late,
  crash repeatedly, or lose inventory across every operation class
- maximum attempt/round/age/count and emergency-reserve exhaustion models,
  including fairness and recovery without victim eviction
- long-running tests proving terminal mailboxes/resources remain bounded,
  quarantined storage never aliases, and healthy domains continue within policy
- restart/destruction tests proving capacity returns only when old external
  reachability is impossible or explicitly reconciled

Exit criteria:

- Every unresolved operation reaches bounded `Uncertain` escalation and domain
  containment; silence cannot retain unbounded state or force unsafe reuse.
- Stop: `v0.23.16 implementation stop reached. Run pentest for this exact commit.`

### v0.23.17 - Typed Execution-Domain Quiescence Proof

Goal: make external-domain destruction an executable, generation-bound proof
that no kernel, DMA engine, provider thread, or registered object can still
access quarantined physical storage.

Deliverables:

- sealed `QuiescenceProof`/`DomainDestroyed` completion types constructible
  only by a reviewed runtime adapter and bound to execution-domain, adapter,
  worker, provider, resource-inventory, shutdown-attempt, and fence generations;
- an adapter-specific proof taxonomy covering ordinary socket operations,
  provider worker threads, asynchronous cryptography, `io_uring` queues and
  registered files/buffers, eBPF/AF_XDP maps and UMEM/DMA frames, and secure-
  transport provider-owned plaintext/ciphertext storage;
- explicit distinction between closing a descriptor/provider handle and
  proving drain, unregister, thread join/process death, queue teardown, DMA
  cessation, completion consumption, and loss of every external reference;
- a fixed manifest of resources covered by each proof; omitted, extra,
  duplicated, already-reused, or generation-mismatched resources fail closed;
- stale, duplicate, forged, wrong-adapter, wrong-domain, partial, or reordered
  destruction evidence is inert and cannot release ownership or capacity;
- adapters unable to prove in-process quiescence retain storage in bounded
  quarantine until process termination, or run the external provider inside a
  supervised isolation boundary whose confirmed death supplies the proof;
- proof acceptance atomically transitions the covered `v0.23.15` physical-
  ownership ledger exactly once and is the only domain-destruction path that
  replenishes `v0.23.16` quarantined/emergency capacity;
- portable no-OS core representation plus first-party adapter evidence
  contracts; a Boolean, closed descriptor, dropped object, timeout, or fence
  acknowledgement alone can never satisfy the type.

Verification:

- `cargo test -p gjallarbru-core execution_domain_quiescence`
- compile/API tests proving runtime code cannot forge a proof from a handle,
  fence acknowledgement, local timeout, provider drop, or free-form snapshot
- adapter/test-double matrices for late kernel completion, live provider thread,
  failed unregister, pending DMA, partial inventory, process death, and clean drain
- stale/duplicate/wrong-domain/wrong-generation proof tests with exact physical-
  ownership and emergency-capacity counters
- model tests proving storage becomes reusable exactly once only after terminal
  completion, deterministic inventory reconciliation, or valid complete quiescence

Exit criteria:

- No claim of domain destruction can release physical storage unless typed,
  adapter-specific evidence proves every declared external accessor quiescent.
- Stop: `v0.23.17 implementation stop reached. Run pentest for this exact commit.`

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

### v0.25.0 - Context-Bound Stateless Authenticated Nonces

Goal: issue context-bound authenticated nonces with a finite replay window
without claiming stateless validation can detect same-context reuse.

Deliverables:

- versioned source/path/realm/time-bound nonce format with key ID and tag;
- absolute-time trust status/generation required for issuance and validation,
  with uncertain/unavailable time failing closed;
- active/previous/revoked key handling, stale response, tamper, cross-path,
  rollback, forward-jump, and uninitialized-clock behavior.
- explicit replay semantics: capture/reuse inside the same accepted path/realm/
  time/key context may validate, while authentication, transaction idempotence,
  quotas, allocation rules, and short lifetime contain its effect;
- metrics, errors, docs, and APIs reserve “replay detected” for mechanisms with
  actual replay state and describe these nonces as context-bound/replay-window-limited.

Verification:

- `cargo test -p gjallarbru-crypto nonce`
- arbitrary nonce decode fuzzing and deterministic trusted/uncertain/unavailable
  time, rollback, forward-jump, and recovery-generation tests
- same-context replay acceptance/containment plus cross-path/realm/time/key-
  generation rejection tests with no false single-use/replay-detected signal

Exit criteria:

- A nonce cannot be issued from untrusted wall time or reused across path,
  realm, time-trust, or key generations; same-context reuse is honestly bounded
  by its acceptance window and surrounding authenticated/idempotent controls.
- Stop: `v0.25.0 implementation stop reached. Run pentest for this exact commit.`

### v0.25.1 - Absolute-Clock Trust Model

Goal: implement production clock-health transitions for the `AbsoluteTime`
primitive defined by `v0.4.0`, without coupling wall time to monotonic lifetimes.

Deliverables:

- runtime transitions among the established `Trusted`, `Uncertain`, and
  `Unavailable` states, with bounded skew/jump policy and source generations;
- failure to issue or newly validate time-based credentials, nonces, and tokens
  when required absolute time is not trusted;
- large forward-jump, rollback, resynchronization, and clock-source replacement
  events with deterministic key/cache/token invalidation decisions;
- existing allocation/permission/channel monotonic lifetimes unaffected by
  wall-clock correction unless a separate policy revocation explicitly ends them;
- generation-changing recovery from uncertainty so stale provider completions
  or cached time decisions cannot acquire authority after trust returns.

Verification:

- unavailable-at-start, uninitialized epoch, rollback, forward jump, oscillation,
  source replacement, recovery, and concurrent credential-operation traces
- differential tests proving identical monotonic event sequences retain the
  same lifetimes across wall-clock changes except for explicit revocation

Exit criteria:

- Untrusted absolute time cannot mint or extend credential authority, and wall
  correction alone cannot silently change monotonic relay authorization.
- Stop: `v0.25.1 implementation stop reached. Run pentest for this exact commit.`

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

### v0.26.1 - Credential Timing and Provider Assurance

Goal: minimize identity-dependent timing leakage and qualify credential
providers without overstating what a trait can guarantee.

Deliverables:

- known-user and unknown-user paths performing equivalent derivation/HMAC work
  with a per-domain dummy derived key and normalized failure ordering;
- bounded positive/negative caches with equivalent lookup, timeout, retry, and
  eviction policy where security permits;
- opaque key handles, provider substitution, stale-generation, cancellation,
  output-size, unavailable, and internal-failure behavior;
- a qualification profile distinguishing first-party constant-time comparison
  from provider/database/network latency that cannot be guaranteed constant;
- logging/metrics tests ensuring identities, keys, dummy-path distinctions, and
  provider timing classes are not exposed.

Verification:

- statistical known/unknown-user leakage tests under controlled providers plus
  deterministic work-counter equality
- provider differential, HSM-style opaque-handle, cache hit/miss/negative,
  timeout, stale completion, cancellation, and failure-path matrices

Exit criteria:

- Unknown identity handling performs equivalent cryptographic work, provider
  failure never authenticates, and timing claims state their measured boundary.
- Stop: `v0.26.1 implementation stop reached. Run pentest for this exact commit.`

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
- two independent legacy gates: compile-time provider/feature availability and
  explicit listener/profile configuration, with a Cargo feature alone unable
  to enable network negotiation or downgrade;
- configuration validation preventing accidental legacy enablement and refusing
  a configured profile whose required provider capability is absent.

Verification:

- `cargo test -p gjallarbru-core password_negotiation`
- cross-feature/profile/provider and downgrade matrix, including legacy feature
  compiled but listener disabled and listener requested but feature unavailable

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
  and method with request identities and expiry;
- exact duplicate, digest mismatch, pending timeout, eviction, and exhaustion tests.

Verification:

- `cargo test -p gjallarbru-core transaction_cache`
- model/property tests over duplicate and reordered events

Exit criteria:

- One transaction can trigger each external side effect at most once.
- Stop: `v0.30.0 implementation stop reached. Run pentest for this exact commit.`

### v0.30.1 - Transaction Identity and Byte Budgets

Goal: prevent digest collision or response-byte exhaustion from confusing
transaction equality and replay behavior.

Deliverables:

- per-process keyed cryptographic-strength request identity with sufficient
  width, domain separation, and method/path/transaction binding;
- exact-byte or collision-resolving semantic evidence sufficient to distinguish
  same-key different-request input without trusting a collision-prone digest;
- independent item, retained-request-byte, and cached-response-byte ceilings
  with deterministic admission, eviction, and reconstructable-response policy;
- `v0.6.2` fixed load factor, maximum probes, tombstone/stale debt, bounded
  cleanup work, and saturation outcome for the transaction index;
- lookup/equality constant-time only for secret-bearing keyed evidence, not
  ordinary public transaction IDs, while collision resolution remains bounded;
- protocol output, response order, semantic operation identity, and eviction
  choice independent of bucket/insertion/tombstone iteration order;
- cached response identity bound to authentication/profile/configuration
  generation so stale policy cannot be replayed after change.

Verification:

- forced-collision test provider, same-key/different-byte corpus, digest-domain,
  configuration-generation, eviction, and expiry properties
- response-size/exhaustion tests proving byte ceilings hold independently of
  record count and no mismatched response is replayed
- reference-model collision, expiry, reload, revocation, load/probe/tombstone,
  cleanup interruption, iteration-layout, and generation/Tick-wrap tests

Exit criteria:

- Transaction idempotence never relies solely on a weak/colliding digest, and
  cached bytes cannot exceed their explicit resource budget.
- Stop: `v0.30.1 implementation stop reached. Run pentest for this exact commit.`

### v0.30.2 - Transaction Invalidation Semantics

Goal: preserve exact retransmission behavior across ordinary reloads while
making security revocation explicitly authoritative.

Deliverables:

- ordinary configuration/profile changes pin each live transaction to its
  original decision generation until normal expiry;
- exact retransmissions normally replay the original response and at-most-once
  state result rather than re-evaluating against unrelated new policy;
- separate invalidation classes for credential/key revocation, tenant removal,
  allocation teardown, path invalidation, listener retirement, and emergency policy;
- for every class, an explicit outcome of replay, replacement error, silent
  discard, allocation teardown, or path termination;
- cached successes prevented from claiming a live allocation after the
  allocation was explicitly revoked or destroyed;
- transaction reference-model integration for reload/revocation races,
  reordered invalidations, stale completions, and cached-response generations.

Verification:

- model/property tests crossing transaction expiry with normal reload, key
  rotation, emergency revoke, tenant delete, listener retire, and allocation teardown
- exact retransmission assertions for response bytes, side-effect count, live
  state truth, chosen invalidation outcome, and amplification bounds

Exit criteria:

- Normal reload cannot break idempotence, and explicit security invalidation
  cannot replay a success that falsely represents revoked live authority.
- Stop: `v0.30.2 implementation stop reached. Run pentest for this exact commit.`

### v0.30.3 - Linear Ingress Work Permits

Goal: charge unauthenticated work through one cheap linear permit before the
first public UDP Binding listener parses attacker-controlled bytes.

Deliverables:

- a cheap admission transition using only listener identity, datagram length,
  trusted receive metadata, and injected monotonic time, before frame parsing;
- a single-use non-cloneable `IngressWorkPermit` carrying finite allowances for
  packet/parse bytes and operations, HMAC attempts, credential-lookup admission,
  error-response bytes, and preparation-workspace bytes/operations;
- fixed global, listener, and worker budgets for received packets/bytes, parse
  operations/bytes, integrity/HMAC attempts, credential-lookup admissions, and
  generated error-response packets/bytes;
- preparation consumes but cannot refill, transfer, split, merge, or reuse the
  permit; every work stage fails before exceeding its remaining allowance;
- permit acquisition reserves maximum stage allowances without consuming them;
  beginning parse, HMAC, lookup, response construction/send, or preparation
  atomically converts only that stage's reservation into an attempt charge;
- dropping/cancelling the permit releases only unused reservations, while any
  started stage remains non-refundable through every later failure path;
- charge points before each expensive stage, with malformed, unauthenticated,
  unknown-user, bad-integrity, stale-nonce, and successful paths accounted;
- bounded admission/update work, saturating arithmetic, deterministic
  exhaustion outcomes, and no parsing/retry/refund path before a permit exists;
- non-refundable attempt capacity replenished only by deterministic injected
  monotonic token-bucket refill with explicit rate/burst ceilings, never by
  malformed input, failed preparation, queue exhaustion, cancellation, or send failure;
- spoofable-source policy that does not depend solely on per-source identity,
  plus amplification ceilings for unauthenticated responses;
- integration with `v0.23.6` attempt/occupancy/completion accounting and
  `v0.30.0` transaction caching so retransmissions cannot bypass or double-charge;
- cached retransmissions still consume packet, parse/classification,
  transaction-cache lookup, and send attempts, while transaction identity
  prevents recreation of semantic side effects;
- immutable safe defaults required by production listener construction, with
  later hierarchical/fairness extensions reserved for `v0.58.0`/`v0.59.0`.

Verification:

- `cargo test -p gjallarbru-core ingress_work_permit`
- compile-time single-use/non-clone checks plus split/merge/transfer/reuse and
  preparation-without-permit rejection fixtures
- per-stage reserve/start/drop matrices proving unused HMAC/lookup/response
  reservations release while started stages never refund
- malformed/valid packet floods across global/listener/worker boundaries,
  HMAC/lookup exhaustion, cached retransmission, error amplification, and
  counter/token-bucket saturation/wrap/refill
- model tests proving bounded work per datagram, deterministic monotonic
  recovery, and no failure-refund/retry/double-charge/workspace bypass

Exit criteria:

- No attacker-controlled parse, crypto, lookup, preparation, or error-response
  work occurs without a finite linear allowance; unused reservations release,
  started work never refunds, and cached retries cannot recreate side effects.
- Stop: `v0.30.3 implementation stop reached. Run pentest for this exact commit.`

### v0.30.4 - Two-Stage Ingress Classification

Goal: decide a finite method/work class without prematurely reserving HMAC,
lookup, preparation, or response capacity that the packet may never consume.

Deliverables:

- `UnclassifiedIngressPermit` acquired from listener/path, packet/frame length,
  trusted receive metadata, and monotonic time, paying only packet admission and
  one bounded fixed STUN/ChannelData header classification;
- refinement of `v0.30.3` into unclassified/classified typestates without
  changing its token-bucket refill, non-refundable attempts, or total ceilings;
- classification reads no attributes, performs no HMAC/credential lookup, and
  has fixed operation/byte limits independent of declared method;
- one irreversible atomic conversion into a configured method/work-class
  permit reserving only that class's maximum parse, HMAC, lookup, preparation,
  response, and send allowances;
- failure to reserve the classified permit stops before attribute iteration,
  text preparation, integrity processing, credential lookup, or response planning;
- classification attempt and bytes remain non-refundable whether conversion
  succeeds, fails, is cancelled, or the packet is malformed;
- an unclassified permit cannot classify twice, convert to multiple classes,
  downgrade/upgrade after conversion, split, merge, transfer, or probe class
  capacity without a newly charged packet;
- a fixed bounded class registry controlled by immutable configuration:
  attacker-declared unknown methods map to one finite unknown/invalid class and
  cannot manufacture class identifiers, fairness queues, or new quota domains;
- ChannelData has its finite fixed-header class; STUN requests remain in their
  ordinary method class through the charged transaction-cache lookup, with no
  pre-lookup cached-retransmission class.

Verification:

- `cargo test -p gjallarbru-core ingress_classification`
- compile/API tests for unclassified/classified typestates, exact-once
  conversion, and forbidden repeat/split/merge/transfer/reclassification
- exhaustive fixed-header method/class combinations plus malformed, truncated,
  unknown-method, ChannelData, retransmission, and class-exhaustion tests
- adversarial mixed-listener floods proving Binding never reserves TURN HMAC/
  lookup capacity, declared methods cannot create classes, and failed conversion
  performs no attribute/HMAC/lookup/preparation work
- accounting/model tests proving classification is irreversible, charged once,
  and cannot become a refund or capacity-probing oracle

Exit criteria:

- Before the work class is known, only fixed-header classification capacity is
  reserved; expensive stage authority is acquired exactly once afterward and
  failure stops before any class-specific work.
- Stop: `v0.30.4 implementation stop reached. Run pentest for this exact commit.`

### v0.30.5 - Ingress Reservation Fairness

Goal: retain maximum-stage reservation guarantees without allowing queued,
batched, or cheap traffic to hoard scarce future-work capacity.

Deliverables:

- just-in-time unclassified permit acquisition immediately before fixed-header
  classification of one packet/frame, never while input waits in a queue;
- fixed maximum outstanding permit count, total reserved stage capacity, and
  reservation lifetime per listener and worker, with deterministic expiry;
- batched receive represented as independently admitted packets: batch size
  never grants batch-wide permits or reserves aggregate HMAC/lookup capacity;
- unused stage reservations released at packet completion/drop and before the
  next packet is prepared where the runtime can do so without violating ordering;
- deterministic weighted/fair admission between listeners and, after bounded
  `v0.30.4` classification, among the finite configured method/work classes;
- no fairness class can bypass its packet, parse, HMAC, lookup, preparation,
  response, byte, or attempt charges, and spoofable identity cannot create an
  unbounded class;
- queue, shutdown, cancellation, worker replacement, and permit-lifetime
  handling integrated with `v0.23.3`, `v0.23.6`, and `v0.30.3`.

Verification:

- `cargo test -p gjallarbru-core ingress_reservation_fairness`
- adversarial multi-listener mixes of malformed Binding, valid Binding,
  authentication failures, authenticated TURN, and retransmissions under every
  outstanding-permit/reservation/deadline limit
- scalar and batched receive tests proving one permit per packet/frame, no
  pre-acquisition for queued work, prompt unused-reservation release, bounded
  wait, and identical non-refundable attempt accounting
- model/property tests for starvation, spoofed-class explosion, cancellation,
  shutdown, stale permit, monotonic wrap, and worker/listener replacement

Exit criteria:

- Reservation strengthens admission without becoming a starvation mechanism:
  no queued/batched packet hoards future stage capacity and every admitted work
  class makes bounded progress under its declared fairness policy.
- Stop: `v0.30.5 implementation stop reached. Run pentest for this exact commit.`

### v0.30.6 - Authorized Client Delivery

Goal: make every client-bound packet use the same typed, expiring,
revocation-fenced authority discipline as peer-bound delivery.

Deliverables:

- non-forgeable `AuthorizedClientPath`/`ClientDeliveryCapability` binding the
  complete `v0.4.1` `ClientPath`, remote/local destination, transport, listener,
  socket/connection/session, worker, configuration, proxy, TLS/DTLS, interface,
  realm, and tenant generations;
- binding to exact command, accepted batch, buffer/lease, transaction and/or
  allocation identity, response/indication kind, packet/byte charge, maximum
  queue age, execution tick, and `v0.23.12` authority sequence;
- single-use runtime validation immediately before handoff, with raw addresses,
  connection handles, reconstructed paths, charge substitution, and cross-batch
  or cross-transaction reuse rejected;
- disconnect, listener retirement, proxy/session replacement, path invalidation,
  revocation, reload, worker restart, and identifier/buffer reuse advancing the
  authority fence before replacement becomes visible;
- required use for Binding/error responses, authenticated successes, Allocate/
  Refresh/Permission/Channel responses, Data indications, peer-to-client
  ChannelData, and later RFC 6062 client indications/data;
- an API extension rule requiring future relay peer sources to be canonicalized
  before permission/channel lookup or construction of client delivery authority;
- bounded already-in-flight behavior integrated with `v0.23.11`, with no claim
  that disconnect/cancellation recalled an OS send and no attempt refund.

Verification:

- compile/API tests proving no client send command accepts a raw address,
  socket/connection/session handle, or forgeable generation tuple
- stale path/listener/socket/proxy/TLS/DTLS/interface/realm/configuration/
  worker/transaction/allocation/buffer/fence adversary matrices
- disconnect/reconnect, five-tuple reuse, trusted-proxy replacement, session
  resumption, revocation, queue expiry, duplicate consumption, and in-flight tests
- Binding/error/authenticated-response tests proving one exact live client path
  is required without depending on future relay-peer implementation

Exit criteria:

- Every client-bound packet is authorized for one exact live client path,
  command, charge, deadline, and authority sequence, and stale paths cannot send.
- Stop: `v0.30.6 implementation stop reached. Run pentest for this exact commit.`

### v0.30.7 - Cached Retransmission Admission

Goal: recognize an exact cached retransmission only after charging the ordinary
method path and the bounded transaction-cache lookup needed to prove identity.

Deliverables:

- fixed-header classification always selects the normal finite STUN method/
  work class; no cache-hit, retransmission, or transaction-ID class exists
  before lookup;
- the classified method permit reserves and charges one bounded transaction-
  cache lookup with explicit operation, probe, byte-read, and collision ceilings;
- only a successful strong-identity lookup after its charge may enter a typed
  `CachedResponse` substate bound to the original transaction/configuration/
  authentication/path generations and cached response bytes;
- a cache hit may release still-unused HMAC, credential-lookup, preparation,
  and semantic-mutation reservations that will provably not start;
- packet/frame admission, fixed-header classification, request parsing/identity
  work, cache lookup, response construction/copy where applicable, and send
  attempts remain consumed and cannot be refunded by the hit;
- cache miss, digest/byte mismatch, deliberately colliding transaction IDs,
  evicted entries, invalidated entries, and stale generations continue/reject
  under the ordinary method budget without a cheaper repeatable lookup path;
- hit/miss/error response content, amplification, audit, and rate-limit behavior
  cannot create a cache-membership oracle beyond protocol semantics; timing
  follows the explicit `v0.30.8` threat model rather than claimed full-path equality;
- cached response delivery still requires `v0.30.6` live client-path authority
  and cannot recreate allocation or other semantic side effects.

Verification:

- `cargo test -p gjallarbru-core cached_retransmission_admission`
- charge-ledger tests for hit, miss, collision, digest match/byte mismatch,
  eviction, invalidation, expiry, stale path/configuration, and response exhaustion
- assertions that a hit releases only unstarted reservations while admission,
  classification, parsing/identity, lookup, response/copy, and send attempts
  remain charged
- adversarial repeated/colliding transaction-ID floods proving bounded probes,
  no cheap cache oracle, no fairness bypass, and no semantic side-effect replay
- ordinary-versus-cached path timing/amplification envelopes and exact response/
  transaction identity differential tests

Exit criteria:

- Cached retransmission is a post-lookup substate, never a pre-lookup fairness
  class, and cache hits cannot refund performed work or reproduce side effects.
- Stop: `v0.30.7 implementation stop reached. Run pentest for this exact commit.`

### v0.30.8 - Cache Timing Threat Model

Goal: prevent useful transaction-cache oracles without pretending that a cache
hit and an authenticated miss perform identical work or adding attacker-driven
expensive work solely for timing equalization.

Deliverables:

- an explicit deployment/profile decision on whether cache membership is
  public protocol-correlated state or classified sensitive state, including
  remote, co-resident, authenticated, and cross-tenant observer capabilities;
- identical protocol-semantic error class, response bytes, amplification cap,
  audit redaction, retry/rate-limit accounting, and delivery authorization for
  equivalent hit/miss/error outcomes where the RFC permits equivalence;
- bounded fixed-probe lookup and keyed identity comparison, with constant-time
  comparison for secret-bearing digests/tags and no early secret-byte oracle;
- measured, documented hit, miss, collision, invalidation, and error latency
  envelopes per runtime/profile; envelopes need not be identical when cache
  membership is not secret and natural bounded work differs;
- prohibition on dummy HMAC, credential lookup, policy execution, response
  construction, or semantic mutation performed only to make a cache hit as
  expensive as a miss;
- profiles that classify membership as sensitive use a fixed bounded response-
  release schedule with finite delay slots, jitter policy, overload behavior,
  and no repeated authentication/provider work;
- schedule saturation fails or degrades according to documented profile policy
  without creating an unbounded delay queue, amplification change, or priority bypass;
- timing reports and threat-model decisions are release evidence and rechecked
  when cache identity, crypto provider, runtime, hardware, or profile changes.

Verification:

- `cargo test -p gjallarbru-core cache_timing_policy`
- response/error/amplification/audit/charge differential tests across hit, miss,
  collision, digest mismatch, stale, invalidated, evicted, and exhausted entries
- constant-time secret-comparison tests and instrumentation proving no dummy
  HMAC, credential lookup, or policy work occurs on a cache hit
- statistically reviewed timing-envelope benchmarks on maintained reference
  systems, treated as regression evidence rather than a universal constant-time claim
- sensitive-profile release-schedule tests for boundaries, overload, fairness,
  cancellation, clock anomalies, and cross-tenant isolation

Exit criteria:

- Cache timing has an explicit observer/secrecy model and bounded measured
  behavior; no semantic oracle or artificial expensive equalization path exists.
- Stop: `v0.30.8 implementation stop reached. Run pentest for this exact commit.`

### v0.31.0 - Portable IPv4 UDP Binding Runtime

Goal: connect real UDP sockets to the same Binding core path used in tests.

Deliverables:

- safe single-worker portable UDP listener, fixed buffer pool, path conversion,
  full-batch operation-queue reservation/acceptance, command execution, exact
  completion accounting, and clean shutdown;
- mandatory `v0.30.3`-`v0.30.5` two-stage just-in-time ingress admission before
  class-specific parse, HMAC, lookup, preparation, and response work;
- `v0.30.7` charged cache lookup/substate behavior for exact retransmissions;
- `v0.30.8` cache timing/secrecy profile, measured envelopes, and prohibition
  on dummy expensive work used only to equalize hit and miss paths;
- `v0.30.6` authorized client delivery for every Binding/error response, with
  final path/deadline/fence validation immediately before socket handoff;
- implementation of the `v0.23.9` accepted-batch crash/reconciliation contract
  through the `v0.23.10` single-thread portable publication adapter;
- local execution-domain implementation of `v0.23.12` fence acknowledgement
  plus `v0.23.13` coalesced watermarks and disconnect/listener/buffer reuse barriers;
- local timer integration using `v0.23.14` nonterminal deadline observations
  rather than synthesizing failed/cancelled socket results;
- `v0.23.15` ledgers separating fence progress, socket-operation in-flight
  state, semantic generation retirement, and physical buffer/descriptor release;
- `v0.23.16` fixed unresolved-operation budgets and local execution-domain
  replacement when cancellation/reconciliation cannot establish terminal truth;
- `v0.23.17` portable socket-adapter quiescence evidence before quarantined
  descriptors/buffers are returned to reusable pools;
- loopback integration harness with no task/timer per request.

Verification:

- `cargo test -p gjallarbru-runtime udp_binding_ipv4`
- local black-box Binding request/response smoke plus queue-full, partial
  external failure, cancellation, and shutdown reconciliation tests
- ready-before-execute, partial-send, lost-completion, queue-loss, buffer/lease,
  restart, and old-worker-epoch crash matrix
- receive-queue and multi-listener tests proving permits are not pre-acquired,
  retained beyond their lifetime, or batch-reserved across packets
- stale/replaced client path, queue deadline, disconnect, fence acknowledgement,
  and duplicate client-delivery capability tests
- silent-socket/test-provider, unresolved-budget saturation, quarantined-buffer,
  descriptor-alias, and execution-domain replacement tests
- cache hit/miss/error semantic differential and timing-envelope smoke tests
- closed-descriptor versus outstanding-operation proof tests demonstrating that
  handle close alone cannot release a quarantined buffer

Exit criteria:

- Real socket behavior matches synthetic core vectors, remains bounded when the
  socket provider is silent, and never reuses externally reachable storage.
- Stop: `v0.31.0 implementation stop reached. Run pentest for this exact commit.`

### v0.31.1 - First Hot-Path Resource Baseline

Goal: instrument allocation, copying, tasks, descriptors, and retained bytes
from the first real packet path instead of retrofitting evidence after tuning.

Deliverables:

- fail-after-startup allocator mode and allocation/copy counters around receive,
  parse, core transition, encode, queue, send, error, and drop paths;
- proof that no task, future, timer object, external lookup, or growable stream/
  response buffer is created per packet;
- file-descriptor, buffer-lease, queue-item, transaction-response-byte, and
  shutdown reconciliation counters with stable metrics;
- baseline latency/throughput/copy reports retained for later scalar/batched/
  accelerated differential comparison and eventual `v0.80.1` named profile closure.

Verification:

- successful, malformed, output-capacity, queue-full, send-failure, and shutdown
  tests under fail-after-startup allocation
- copy/task/descriptor/byte-counter assertions plus sustained loopback churn

Exit criteria:

- The first production-shaped UDP path has executable resource evidence, and
  later acceleration cannot redefine the baseline semantics.
- Stop: `v0.31.1 implementation stop reached. Run pentest for this exact commit.`

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
- `v0.30.6` authorized client-path capability on original and cached responses,
  revalidated for path/fence/deadline without recreating semantic side effects;
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

### v0.36.1 - Timing-Wheel Debt and Jump Closure

Goal: bound stale-entry debt and expiration work so refresh churn and large time
jumps cannot exhaust the worker or extend authorization.

Deliverables:

- independent ceilings for live timer entries, stale/dead entry debt, and
  reschedule insertions per object/generation;
- an explicit replace-in-place, bounded-duplicate, or incremental-compaction
  strategy with deterministic capacity and failure behavior;
- maximum expiration-work budget per transition plus an overdue-work cursor/
  backlog that advances fairly across object classes and generations;
- large forward-jump and lag semantics where authorization expires at its
  original deadline even if cleanup work is processed later;
- refresh-before-expiry behavior that cannot accumulate unbounded stale wheel
  nodes, starve other timers, or reset fairness debt.

Verification:

- attacker refresh churn immediately before expiry, maximum stale debt,
  compaction interruption, wheel wrap, and capacity-exhaustion model tests
- large-jump/overdue traces proving authorization checks use logical deadline,
  per-step work stays bounded, and backlog fairness eventually cleans every entry

Exit criteria:

- Timer debt and per-transition work have hard ceilings, and delayed cleanup
  can never be interpreted as extended permission or allocation authority.
- Stop: `v0.36.1 implementation stop reached. Run pentest for this exact commit.`

### v0.37.0 - Randomized Relay-Port Allocator

Goal: reserve relay ports predictably in cost but unpredictably in selection.

Deliverables:

- per-IP/family/transport/shard port tables and explicitly supplied randomized
  bounded selection, with the exact entropy profile closed by v0.37.1;
- free/reserved/opening/allocated transitions and atomic adjacent-port reservation.

Verification:

- `cargo test -p gjallarbru-core relay_ports`
- collision, exhaustion, randomness-health, rollback, and concurrency model tests

Exit criteria:

- Hostile requests cannot cause sequential leakage or unbounded port search.
- Stop: `v0.37.0 implementation stop reached. Run pentest for this exact commit.`

### v0.37.1 - Relay-Port Entropy Profile

Goal: reconcile unpredictable port choice with explicit deterministic reducer
inputs and bounded search.

Deliverables:

- one selected profile: an explicitly supplied per-worker seed feeding a
  deterministic keyed permutation/PRF, or a purpose-bound entropy completion
  for each allocation search;
- rejection sampling or equivalent mapping with no modulo bias and no repeated
  candidate within one bounded search;
- independent process/worker seeds and explicit snapshot, fork, clone, crash,
  restart, and reseed behavior preventing silent stream reuse;
- deterministic candidate-budget exhaustion and stable rollback when every
  generated candidate is unavailable;
- seed/result secrecy, redaction, zeroization limits, health/failure behavior,
  and provider qualification linked to the v0.17.2 crypto split.

Verification:

- distribution/bias and without-replacement tests over representative port sets
- same-input replay, independent-worker/process, fork/snapshot/restart,
  entropy-unavailable, collision, exhaustion, even-port pair, and rollback tests

Exit criteria:

- Port search is unbiased, nonrepeating, bounded, explicitly seeded/supplied,
  and cannot silently reuse a randomness stream after process duplication.
- Stop: `v0.37.1 implementation stop reached. Run pentest for this exact commit.`

### v0.37.2 - Canonical Effective Destinations

Goal: reduce every received peer representation to one policy identity while
preserving effective destinations hidden by mapping, translation, or IPv6 scope.

Deliverables:

- canonical IPv4/IPv6 address domains with IPv4-mapped IPv6 normalized to IPv4
  before equality, indexing, permission, policy, quota, logging, or loop checks;
- configured NAT64 prefix de-embedding that retains both the received IPv6 and
  effective IPv4 destination and requires both to pass policy;
- translation-profile and public-address-map generations included in the
  canonical result and all equality/cache/permission/policy keys that consume it;
- rejection of unspecified, multicast, IPv4 broadcast, and inappropriate
  link-local/interface/scope combinations before relay command construction;
- interface/scope-aware IPv6 equality and canonical hashing where zone identity
  is semantically required;
- local listener, administration/control, and relay-pool comparison after
  bind/local/public address translation and one-to-one NAT mapping;
- one bounded canonicalization result consumed by permission, channel,
  destination policy, relay-loop, quota, and audit logic without re-decoding.

Verification:

- `cargo test -p gjallarbru-core canonical_destination`
- cross-representation properties for IPv4, IPv4-mapped IPv6, configured NAT64,
  scoped/link-local IPv6, translated bind/public addresses, multicast,
  broadcast, unspecified, metadata, loopback, listener, and relay-pool targets
- same-received-address tests across translation/public-map generations proving
  equality, caching, and authority never silently cross generations
- alias-bypass tests proving all encodings of an effective protected
  destination receive the same or stricter denial

Exit criteria:

- No alternate representation or stale translation/public-map generation can
  silently change or inherit the security identity of an effective destination.
- Stop: `v0.37.2 implementation stop reached. Run pentest for this exact commit.`

### v0.37.3 - Translation-Generation Lifecycle

Goal: make NAT64 and public-address translation unambiguous, bounded, and safe
across configuration changes affecting existing protocol authority.

Deliverables:

- RFC 6052 validation accepting only supported NAT64 prefix lengths and
  rejecting malformed host-bit/layout configurations;
- deterministic failure for overlapping, equally applicable, or otherwise
  ambiguous translation-prefix/public-address-map matches;
- maximum translation depth of one configured mapping step, with recursive,
  chained, or re-embedded translation rejected;
- an explicit per-object decision for permissions, channels, transactions,
  cached policy results, and relevant allocation indexes: pin the exact
  translation generation until normal expiry or invalidate/teardown on change;
- atomic mapping publication with old/new generation overlap ceilings and no
  request evaluated against a mixed mapping set;
- reload, rollback, removal, replacement, and worker-restart semantics for
  translation generations and their dependent cached/stateful objects.

Verification:

- `cargo test -p gjallarbru-core translation_generation`
- RFC 6052 prefix-length vectors plus overlapping/ambiguous/recursive/depth
  negative configurations
- same received IPv6 address mapping to different effective IPv4 destinations
  across generations, covering permission, channel, transaction, cache, reload,
  rollback, expiry, invalidation, teardown, and restart

Exit criteria:

- A mapping change never silently retargets existing authority, and every
  translation is one-step, unambiguous, RFC 6052-valid, and generation-bound.
- Stop: `v0.37.3 implementation stop reached. Run pentest for this exact commit.`

### v0.37.4 - Typed Authorized Endpoints

Goal: seal canonical destination and policy approval into a capability so the
runtime cannot reconstruct, reinterpret, or substitute a different endpoint.

Deliverables:

- an `AuthorizedPeer` capability binding received and effective peer addresses,
  family, transport, interface/scope, translation/public-map/policy generations,
  allocation/permission identity, expiry, direction, and exact runtime endpoint;
- corresponding typed `AuthorizedRelayEndpoint` and fast-path capabilities for
  relay bind/open and accelerated packet authority where a peer permission is
  not the applicable identity;
- non-forgeable constructors available only after canonicalization,
  translation-generation, permission/allocation, destination-policy, loop,
  expiry, and quota checks succeed;
- `SendPeer`, relay-open, relay-send, ChannelData, and fast-path commands accept
  typed capabilities rather than raw policy-sensitive addresses;
- the runtime executes the included effective endpoint exactly or rejects the
  command; address reconstruction, remapping, DNS lookup, family conversion,
  scope substitution, or endpoint widening is forbidden;
- capability generation/expiry invalidation across permission refresh/removal,
  allocation teardown, policy/translation reload, worker restart, and handle reuse.

Verification:

- compile/API tests proving raw addresses cannot construct policy-sensitive
  commands or authorized endpoint capabilities
- runtime adversary tests attempting address substitution, remapping, family/
  scope change, stale generation, expired permission, cross-allocation reuse,
  and fast-path widening
- safe-reference differential packet captures proving the runtime endpoint
  equals the capability endpoint byte-for-byte on every accepted command

Exit criteria:

- Policy approval and runtime use share one typed generation-bound endpoint,
  and conforming adapters cannot reinterpret or substitute it.
- Stop: `v0.37.4 implementation stop reached. Run pentest for this exact commit.`

### v0.37.5 - Execution-Time Endpoint Authority

Goal: ensure a capability valid during planning cannot become indefinite queued
authority after expiry, revocation, teardown, policy change, or identifier reuse.

Deliverables:

- every delivery capability carries a maximum execution `Tick` no later than
  allocation/permission/capability expiry plus an independently bounded maximum
  queue age measured from command publication;
- binding to exactly one semantic command ID, accepted batch ID, operation
  generation, direction, packet length, byte charge, and packet attempt charge;
- single-use consumption for delivery commands, with duplicate handoff,
  split/merge, charge substitution, and cross-batch reuse rejected;
- runtime pre-handoff validation of execution tick, queue age, allocation/
  permission/policy/translation/public-map/worker generations, command/batch
  identity, buffer generation, and exact endpoint;
- a non-droppable control-lane revocation fence that prevents older queued
  capabilities from reaching the OS before identifier, endpoint, permission,
  allocation slot, policy generation, or buffer generation reuse;
- concrete reuse of the `v0.23.12` monotonic authority sequence and per-lane
  acknowledgement protocol for queues, socket/provider submission, and later
  accelerated lanes, never FIFO ordering alone;
- `v0.23.13` fixed lane registry, coalesced required watermark, acknowledgement
  meaning, semantic-generation separation, and declared execution-domain scope;
- bounded in-flight semantics after OS handoff: recall/cancellation is never
  assumed, attempt/byte charges remain consumed, and each possible late result
  follows the `v0.23.11` terminal-mailbox contract;
- explicit behavior for send syscalls/provider operations that complete after
  authority deadline without treating delayed execution as lifetime extension.

Verification:

- compile/API tests for single-use command/batch/charge binding and rejection of
  cloning, replay, split, merge, packet/byte substitution, and cross-batch use
- deterministic queue-delay tests crossing permission/allocation expiry,
  revocation, policy/translation reload, teardown, worker restart, and every
  identifier/endpoint/buffer reuse boundary
- fence-order model tests proving no pre-fence capability is handed off after
  reuse becomes visible, even with full packet queues and racing completions
- missing/uncertain acknowledgement tests proving the old execution domain is
  quarantined and quiescence-proven under `v0.23.17`, or replaced by a disjoint
  non-aliasing generation without physical-storage reuse
- syscall/provider fault tests for already-in-flight success, failure,
  cancellation, and uncertain status with exact non-refundable accounting

Exit criteria:

- Endpoint authorization remains valid at the final runtime handoff, every
  delivery capability is consumed once for its exact command and charge, and
  revocation/reuse cannot leave older queued authority executable.
- Stop: `v0.37.5 implementation stop reached. Run pentest for this exact commit.`

### v0.37.6 - Minimum Relay Safety Baseline

Goal: make the first functional relay methods depend on canonical destination,
execution-bounded typed authorized endpoints, relay-loop, and fixed relay-
resource defenses rather than placeholder traits.

Deliverables:

- a mandatory immutable baseline operating on the `v0.37.2` canonical/effective
  identity under the `v0.37.3` translation lifecycle, producing only the
  `v0.37.4` typed capabilities with `v0.37.5` execution authority after denying
  metadata services, loopback, all Gjallarbru listeners, administration/control
  endpoints, configured relay pools, same-node/self destinations, and direct
  or recursive relay loops;
- fixed global, worker, allocation, relay-port, permission, channel, retained
  buffer, and queued-byte ceilings with atomic reserve/commit/release behavior;
- mandatory reuse of the `v0.30.3`-`v0.30.5` two-stage just-in-time ingress
  permit for every TURN request before relay-specific admission begins;
- deterministic silent-discard, authenticated error, retry-later, or admission
  refusal behavior for every exhausted or denied path without amplification;
- capability-shaped policy/quota gates required by Allocate, CreatePermission,
  Send, ChannelBind, and ChannelData constructors, with no allow-all/default
  implementation admitted in production profiles;
- an extension boundary allowing `v0.56.0`-`v0.59.0` to add configurable
  profiles, hierarchical accounting, and fairness without weakening this baseline.

Verification:

- `cargo test -p gjallarbru-core minimum_relay_safety`
- generated canonical/effective metadata, loopback, listener, admin, relay-pool,
  same-allocation, same-node, and two-relay loop fixtures
- model/property tests for every fixed relay ceiling, reserve/rollback path,
  inherited ingress-permit gate, and deterministic exhaustion result

Exit criteria:

- No later relay command can be constructed without the minimum safety gates,
  and address aliases/runtime substitution cannot bypass their decisions.
- Stop: `v0.37.6 implementation stop reached. Run pentest for this exact commit.`

### v0.38.0 - Allocate Semantic Validation

Goal: validate Allocate completely before any relay resource is opened.

Deliverables:

- requested transport/family/lifetime/even-port/reservation/fragment schemas;
- authentication, existing allocation, mandatory `v0.37.6` quota/policy baseline,
  and relay availability ordering.

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

### v0.39.1 - Early State-Model Assurance

Goal: move mechanical state assurance into the first external-resource
transition rather than waiting for the late whole-project assurance milestone.

Deliverables:

- a simple executable allocation reference model covering provisional,
  committed, failed, timed-out, disconnected, and released states;
- generated traces containing duplicate, reordered, delayed, stale-generation,
  capacity-failed, entropy-failed, and output-capacity-failed events;
- bounded Kani/model harnesses for small slabs, timers, reservations, operation
  generations, counters, and command atomicity;
- promoted counterexamples as ordinary regression tests and a reusable model
  harness required by later permission/channel/TCP state milestones.

Verification:

- model-versus-core differential sequences across every small-capacity state
- Kani/property checks for uniqueness, rollback completeness, counter bounds,
  stale-event inertness, and at-most-once external side effects

Exit criteria:

- Two-phase allocation invariants have executable model evidence before the
  portable relay runtime becomes the reference for later features.
- Stop: `v0.39.1 implementation stop reached. Run pentest for this exact commit.`

### v0.39.2 - External-Effect Lifecycle Specification

Goal: mechanically explore the full allocation/open/cancel/timeout/completion/
fence/quarantine/quiescence lifecycle before portable sockets make one event
ordering look authoritative.

Deliverables:

- a small reviewable TLA+/PlusCal, Quint, or equivalently exhaustive declarative
  model separate from production Rust and the executable reference model;
- states/transitions for prepared/committed allocation, external open handoff,
  success/failure, local deadline, cancellation request/result, late/conflicting
  completion, revocation fence/acknowledgement, semantic retirement, physical
  quarantine, recovery budget, domain replacement, and typed quiescence proof;
- explicit environment/fairness assumptions for provider silence, delayed/lost/
  duplicate observations, control-lane scheduling, crash/restart, and process death;
- checked invariants for at-most-once external effect/terminal result, unique
  relay ownership, no stale semantic authority, no physical storage alias while
  externally reachable, no invented cancellation/failure, bounded mailbox/
  quarantine capacity, and recovery only under valid evidence;
- checked progress properties under declared fair/healthy-provider assumptions,
  with silence leading to bounded uncertainty/containment rather than false success;
- trace translation between model states and Rust/reference-model events plus a
  stable counterexample format promoted into ordinary regression fixtures.

Verification:

- exhaustive bounded model runs across tiny capacities, two allocations,
  multiple generations, reordered/lost/duplicate events, and every fault state
- mutation checks showing removal of a fence, generation, ownership, recovery,
  or quiescence condition produces a model counterexample
- replay of model traces against the simple reference model and core implementation
- CI resource/time bounds, pinned model-tool versions, deterministic outputs,
  and reviewed assumptions/invariants documentation

Exit criteria:

- The first external allocation effect has independent checked lifecycle
  evidence covering authority, completion truth, quarantine, and physical reuse.
- Stop: `v0.39.2 implementation stop reached. Run pentest for this exact commit.`

### v0.40.0 - Portable Relay Socket Adapter

Goal: execute exact UDP relay open/close/send commands with safe portable sockets.

Deliverables:

- relay bind options, socket registry, peer events, buffer ownership, and error mapping;
- `AuthorizedRelayEndpoint`/`AuthorizedPeer` consumption with exact endpoint
  execution and rejection of raw, reconstructed, remapped, or substituted addresses;
- `v0.37.5` execution-tick, queue-age, command/batch/charge, single-use, and
  revocation-fence validation immediately before socket/provider handoff;
- `v0.23.12` socket-worker/queue acknowledgement before relay endpoint,
  operation, descriptor, or buffer identity reuse, with `v0.23.13` coalescing
  under repeated revocation;
- `v0.23.15` physical descriptor/buffer/provider ownership retained after fence
  acknowledgement until terminal reconciliation and `v0.23.16` bounded
  quarantine/escalation for a socket/provider operation that never completes;
- `v0.23.17` socket-adapter proof covering outstanding operations, descriptor
  close/drain, worker termination, and the exact quarantined resource inventory;
- fixed pool/prebind extension points without changing core commands.

Verification:

- `cargo test -p gjallarbru-runtime relay_socket`
- real bind conflict, exhaustion, close, stale event, loopback peer, capability
  substitution, and exact-endpoint packet-capture tests
- expired/over-age/revoked/reused capability and already-in-flight completion
  tests with exact attempt/byte accounting
- close-with-late-completion, partial inventory, stale proof, and clean socket-
  worker quiescence tests before descriptor/buffer reuse

Exit criteria:

- Runtime socket outcomes map one-to-one to explicit core completions and
  execute only the endpoint sealed into the authorized capability.
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
- response-capacity and send-failure policy;
- `v0.30.6` authorized client delivery for every success/error response, bound
  to the allocation transaction and live path at final runtime handoff.

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

### v0.43.1 - Relay Payload Ownership Baseline

Goal: make Send and Data relay payload ownership safe before any zero-copy lease
optimization exists.

Deliverables:

- a bounded runtime-owned output buffer/copy command for client-to-peer Send and
  peer-to-client Data paths introduced by v0.44.0 and v0.45.0;
- command acceptance transferring ownership of the copied payload until one
  terminal completion, cancellation, drop, or shutdown event;
- no ordinary borrowed packet slice permitted to escape a core transition or
  outlive the receive callback in v0.44.0 through v0.47.0;
- payload-size, copy-byte, output-buffer, queue, tenant, allocation, and worker
  ceilings with deterministic silent-discard/error behavior as required;
- an explicit migration boundary: v0.47.1 may replace eligible copies with
  generation-tagged leases without changing authorization semantics.

Verification:

- compile-fail lifetime fixtures plus receive-buffer-reuse, queue-full,
  cancellation, partial-send, disconnect, and shutdown ownership tests
- maximum payload/copy-budget/exhaustion accounting and copied-versus-later-
  scatter differential vectors

Exit criteria:

- Early relay paths are safely bounded even without zero-copy, and no borrowed
  payload can be observed after its receive storage is reusable.
- Stop: `v0.43.1 implementation stop reached. Run pentest for this exact commit.`

### v0.43.2 - Client-Bound Relay Media Authority

Goal: define before relay media activates that peer-to-client Data and
ChannelData require exact live peer/permission/channel authority at handoff.

Deliverables:

- an explicit live-authority policy: Data and peer-to-client ChannelData must
  present sealed applicable permission/channel authority immediately before
  final client runtime handoff rather than relying on an admission-time snapshot;
- extension of `AuthorizedClientPath` for relay media with canonical received
  and effective peer identities, family/transport/scope, translation/public-map
  generations, allocation identity/generation, permission identity/generation/
  expiry, and exact media direction;
- ChannelData additionally binds channel number, canonical peer transport
  address, channel identity/generation/expiry, and its coupled permission generation;
- separate permission/channel authorization-revocation generations from timer/
  lifetime-revision generations so a refresh can reschedule expiry without
  disguising revoke/rebind authority changes or reviving stale timer entries;
- ordinary same-identity permission/channel lifetime refresh does not rotate
  the revocation generation of an already-issued capability, but that
  capability retains its original embedded expiry and gains no extended life;
- revocation, removal, peer/channel rebind, policy/mapping change, or other
  authority-changing update rotates the applicable generation immediately;
- a stale queued-media capability is dropped by the base policy; no runtime
  adapter may inspect core snapshots, reconstruct authority fields, or mint a
  replacement, with the optional core-only path defined separately by `v0.43.3`;
- permission/channel expiry, revocation, removal, rebind, mapping/policy change,
  allocation teardown, client disconnect, or fence advance before handoff makes
  the queued media inert with no lifetime refresh or response oracle;
- after actual OS/provider handoff, only the bounded already-in-flight,
  ownership, timeout, and stream-tail rules apply; authority is not
  retrospectively extended and attempts are not refunded;
- Data indications require live permission but no channel; ChannelData requires
  both live permission and the exact live channel generation;
- typed construction/model contract first; `v0.45.0` and `v0.47.0` provide the
  respective functional Data and ChannelData implementations.

Verification:

- `cargo test -p gjallarbru-core client_bound_relay_media_authority`
- synthetic peer source canonicalization and alias/NAT64/mapping-generation
  tests crossing permission/channel refresh, expiry, revoke, delete, and rebind
- Data versus ChannelData construction matrices proving distinct authority needs
- ordinary-refresh tests proving old capabilities retain only their original
  expiry while timer revision changes remain distinct and revoke/rebind/policy
  authorization generations invalidate immediately
- queue-age, client disconnect/reconnect, allocation teardown, fence advance,
  duplicate use, buffer reuse, and already-in-flight model tests

Exit criteria:

- No client-bound relay media command can be constructed without the exact
  canonical peer and live permission/channel generations it will require at
  final handoff.
- Stop: `v0.43.2 implementation stop reached. Run pentest for this exact commit.`

### v0.43.3 - Core-Only Queued-Media Reauthorization

Goal: keep stale relay-media handling inside core, with mandatory stale-drop as
the base behavior and one optional bounded ownership-preserving replacement path.

Deliverables:

- mandatory base runtime behavior that drops stale queued Data/ChannelData
  before handoff and returns its payload buffer/lease, charge, and ownership
  through the ordinary terminal path without consulting a snapshot;
- optional typed `ReauthorizeQueuedMedia` event returning the exact still-owned
  packet/lease to core, bound to original command/operation, allocation,
  canonical peer, permission/channel identities, buffer generation, charge,
  enqueue tick, absolute queue-age deadline, authority fence, and worker epoch;
- only core can consume that event and emit either one replacement single-use
  client-delivery capability or an explicit drop; runtime/provider adapters
  cannot inspect state, broaden endpoints, substitute fields, or construct authority;
- at most one reauthorization attempt per original media item, backed by fixed
  event/control-lane capacity and a separate bounded control-work charge;
- replacement retains the original payload, ownership, semantic byte/attempt
  charge, enqueue time, queue-age deadline, and delivery identity; it cannot
  refund work, reset age, extend the original packet lifetime, or create a
  second deliverable command;
- core rechecks current allocation, client path, canonical peer, translation,
  permission, channel, policy, quota, buffer, configuration, and fence state
  atomically before replacement; any mismatch or capacity failure drops;
- no reauthorization after any byte/packet has crossed the OS/provider handoff
  boundary, during a partial-stream tail, or after ownership became uncertain;
- ordinary same-identity permission/channel refresh follows `v0.43.2`: an
  existing capability remains usable only through its embedded original expiry,
  so reauthorization is not required merely to observe an extended lifetime.

Verification:

- `cargo test -p gjallarbru-core queued_media_reauthorization`
- compile/API tests proving adapters cannot mint or modify relay-media authority
  and snapshots cannot satisfy the event or replacement constructors
- refresh, expiry, revoke, delete, rebind, mapping/policy/configuration change,
  disconnect, queue-age boundary, fence, quota, and buffer-generation matrices
- duplicate/stale/wrong-command/wrong-buffer event tests proving at most one
  replacement or drop and exactly one final ownership/charge outcome
- event/control-capacity exhaustion and partial-handoff tests proving fail-closed
  drop without age reset, refund, duplicated delivery, or leaked lease

Exit criteria:

- Stale queued relay media always drops unless core alone reauthorizes the exact
  still-owned item once within its original charge and queue-age envelope.
- Stop: `v0.43.3 implementation stop reached. Run pentest for this exact commit.`

### v0.44.0 - Client-to-Peer Send Indication

Goal: relay client datagrams only through live authorized permissions.

Deliverables:

- exact peer/data schema, family/policy/permission/quota checks, and a
  `SendPeer` command carrying `AuthorizedPeer` rather than a raw address;
- a `v0.37.5` single-use execution deadline, command/batch identity, exact
  packet/byte charge, queue-age limit, and revocation fence on every send;
- RFC-required silent discard with no permission refresh or response oracle.

Verification:

- `cargo test -p gjallarbru-core send_indication`
- missing/expired permission, forbidden destination, zero/maximum data,
  stale/over-age capability, cross-allocation, runtime-substitution, revocation-
  fence, duplicate consumption, and already-in-flight completion tests

Exit criteria:

- No SendPeer command exists without current allocation/permission authority or
  with a runtime endpoint different from its sealed `AuthorizedPeer`.
- Stop: `v0.44.0 implementation stop reached. Run pentest for this exact commit.`

### v0.45.0 - Peer-to-Client Data Indication

Goal: deliver permitted peer UDP datagrams through bounded STUN indications.

Deliverables:

- relay ownership lookup plus `v0.37.2`/`v0.37.3` canonicalization of the
  received peer source before permission lookup, quota, channel selection, or audit;
- peer-IP permission filter, inbound limits, Data encoder, and one `v0.30.6`
  `AuthorizedClientPath` bound to allocation, command/batch, payload buffer,
  exact charge, deadline, and acknowledged authority fence;
- `v0.43.2` live final-handoff binding to canonical peer plus exact permission
  identity/generation/expiry and `v0.43.3` core-only stale-media handling;
- unknown/stale relay, alias/mapping-generation mismatch, expired permission,
  stale/disconnected client path, buffer exhaustion, and send-failure tests.

Verification:

- `cargo test -p gjallarbru-core peer_data`
- real relay socket bidirectional integration plus stale client-path,
  disconnect/reconnect, permission refresh/expiry/revoke, fence, queue-expiry,
  and duplicate-capability tests

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

- client channel lookup plus peer exact-address channel selection producing the
  same `AuthorizedPeer` capability used by Send indications;
- the same `v0.37.5` single-use execution deadline, command/batch/charge
  binding, queue-age, runtime-generation checks, and revocation fence;
- peer-to-client lookup canonicalizes the received peer source under
  `v0.37.2`/`v0.37.3` and emits `v0.30.6` authorized client delivery rather
  than a raw client address/connection;
- `v0.43.2` live final-handoff binding to exact permission and channel
  identities/generations/expiries plus `v0.43.3` core-only stale-media handling;
- permission recheck, rate/byte limits, headroom/scatter plans, and stream padding.

Verification:

- `cargo test -p gjallarbru-core channel_data_relay`
- UDP/stream round trips, expiry-with-active-traffic, stale/over-age capability,
  endpoint/client-path substitution, alias/mapping-generation mismatch,
  permission/channel refresh/expiry/revoke/rebind, duplicate use, revocation
  fence, disconnect, and in-flight tests

Exit criteria:

- ChannelData never outlives either its channel binding or peer-IP permission.
- Stop: `v0.47.0 implementation stop reached. Run pentest for this exact commit.`

### v0.47.1 - Relay Buffer-Lease Ownership

Goal: make zero-copy relay output safe across asynchronous runtime completion
and receive-buffer reuse.

Deliverables:

- generation-tagged runtime-owned receive leases with explicit retain/release
  commands and no ordinary borrowed slice escaping a core transition;
- scatter/gather transmit plans combining generated headers/padding with
  immutable payload segments and exact completion ownership;
- operation, allocation, worker-epoch, and buffer-generation binding for every
  delayed send completion, cancellation, retry, drop, and shutdown path;
- `v0.23.15` separation of semantic fence progress from physical lease release,
  plus `v0.23.16` bounded quarantine if completion/reconciliation never arrives;
- `v0.23.17` typed quiescence proof before any quarantined receive lease or
  pointer-bearing scatter segment returns to its physical pool;
- bounded fallback-copy policy for platforms/providers that cannot retain a
  lease, with separate copy accounting and no semantic drift.

Verification:

- Miri and model tests for reuse, aliasing, double release, stale completion,
  partial send, cancellation, queue failure, disconnect, and shutdown
- scatter output differential tests against canonical contiguous encoding plus
  lease/copy/exhaustion counter assertions

Exit criteria:

- No relay command can observe reused receive storage, and a lease remains live
  exactly until its final runtime completion or explicit cancellation.
- Stop: `v0.47.1 implementation stop reached. Run pentest for this exact commit.`

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
- supported family/type/code policy and forged/unrelated error rejection;
- canonical correlated peer identity plus `v0.30.6` client delivery capability
  for every client-visible Data indication.

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

### v0.55.1 - `gjallarbru` Facade Crate

Goal: give library users one ergonomic `gjallarbru::` entry point without
merging the focused implementation or trust boundaries.

Deliverables:

- public `crates/gjallarbru` facade licensed `MIT OR Apache-2.0`, built as
  `no_std`, forbidding unsafe code, and containing only documentation,
  features, curated convenience exports, and namespaced `wire`, `crypto`, and
  `core` re-exports;
- default-empty feature policy with no dependency on the EUPL runtime, server,
  cluster, operating-system I/O, executor, TLS/DTLS, or network behavior;
- repository README used as the facade package README and crate-level
  documentation, with an automated byte-parity or single-source check that
  prevents the GitHub, crates.io, and docs.rs introductions from drifting;
- facade version tied to the Gjallarbru project milestone while support crates
  retain independent versions, plus release tooling that publishes in strict
  `wire -> crypto -> core -> gjallarbru` dependency order;
- documentation that directs most consumers to `gjallarbru`, while preserving
  direct support-crate dependencies for minimal, embedded, alternate-runtime,
  and independently versioned use cases.

Verification:

- `no_std` and Rust 1.90.0 through 1.97.0 builds for the facade and its default
  graph, with dependency-tree assertions excluding every private package
- compile tests for `gjallarbru::wire`, `gjallarbru::crypto`, and
  `gjallarbru::core`, public-API/SemVer evidence, doctests, and facade README
  parity failure fixtures
- package-content inspection, docs.rs metadata review, publish dry runs, and
  release-tool tests proving the facade cannot publish before or ahead of its
  support crates

Exit criteria:

- Consumers have a documented, stable, no_std `gjallarbru::` namespace without
  weakening crate isolation, licensing, dependency, or release guarantees.
- Stop: `v0.55.1 implementation stop reached. Run pentest for this exact commit.`

## Phase E: Security and Operations

### v0.56.0 - Destination Policy Profiles

Goal: make peer reachability explicit for public, enterprise, custom, and test deployments.

Deliverables:

- immutable numeric prefix/profile decisions over the `v0.37.2`
  canonical/effective destination, with deny reasons and rate classes;
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
  and configured-sensitive-prefix denial over canonical/effective destinations;
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

Goal: extend the exact `v0.30.3` monotonic token-bucket primitive from ingress
admission to hierarchical ongoing work and traffic.

Deliverables:

- reuse of the same saturating refill, reserve-to-attempt conversion, burst,
  wrap, and non-refundable charge semantics defined by `v0.30.3`;
- additional token-bucket scopes for auth, allocation, errors, packets, bytes,
  lookups, relay traffic, tenants, identities, peers, and admin work;
- burst/fairness classes, spoofable-source policy, saturation arithmetic, and clock-jump handling.

Verification:

- `cargo test -p gjallarbru-core rate_limit`
- ingress-versus-hierarchical primitive equivalence plus deterministic burst,
  fairness, wrap, clock-jump, and prolonged-overload simulations

Exit criteria:

- One token-bucket model governs ingress and later rate limits; time anomalies,
  failure refunds, or one quota dimension cannot bypass it.
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
- production implementation of the foundational `v0.23.9` accepted-batch,
  queue-survival/loss, runtime-resource inventory, fencing, cancellation, and
  cleanup matrix under supervisor-controlled worker/process restart;
- implementation of `v0.23.15` physical-ownership quarantine and `v0.23.16`
  bounded unresolved recovery, plus `v0.23.17` evidence that confirmed worker/
  provider process death, thread join, unregister, and inventory closure make
  old external references unreachable before quarantined storage is reclaimed;
- documented single-process development limitation and production minimum redundancy for
  native, container, cluster, and future Aesynx deployment profiles.

Verification:

- test-only dependency/provider and first-party panic injection in release-profile workers,
  proving process abort, supervisor detection, cleanup/fencing, and restart within the SLO
- repeated crash, simultaneous worker crash, crash loop, supervisor death, partial startup,
  secret/core-dump inspection, stale socket/completion, and healthy-worker continuity tests
- cross-checks proving every `v0.23.9` reconciliation outcome is implemented
  rather than replaced by supervisor restart assumptions
- never-responding provider and exhausted-recovery-budget tests proving domain
  destruction, generation replacement, non-aliasing quarantine, and bounded
  emergency capacity without silent unresolved-operation eviction
- false process-death, surviving provider thread, incomplete unregister,
  partial resource inventory, and stale quiescence-proof tests
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
- `v0.2.5` caller-owned semantic workspace/command arena with an Aesynx-owned
  capacity reservation/publication mechanism rather than a required queue model;
- `v0.6.1`/`v0.6.2` no-atomic local path, deterministic storage iteration,
  tombstone/probe debt, fixed stack/static/alignment, generation wrap, and Tick horizon;
- compile-only/mock Aesynx adapter with no `std`, OS socket, thread, or ambient allocator dependency.

Verification:

- `cargo test -p gjallarbru-core --no-default-features fixed_storage`
- Aesynx-shaped mock integration, distinct queue-free publication fixture,
  width/wrap/layout differential, symbol/import, and no_std target checks

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
- bounded framing-byte/partial-frame occupancy before semantic admission and
  one `v0.30.3`-`v0.30.5` two-stage just-in-time ingress permit for each
  complete frame;
- coalesced frames admitted and charged independently without connection-wide
  or read-batch permit reservation;
- no allocation migration between connections with reused endpoints.

Verification:

- `cargo test -p gjallarbru-runtime turn_tcp`
- fragmented/coalesced frames, per-frame permit/charge, reservation-lifetime,
  reconnect reuse, and real TCP interoperability tests

Exit criteria:

- A TCP connection can affect only allocations created on that exact generation.
- Stop: `v0.71.0 implementation stop reached. Run pentest for this exact commit.`

### v0.72.0 - Stream Backpressure

Goal: keep slow TCP/TLS clients from consuming unbounded memory or work.

Deliverables:

- queued frame/byte/age limits, partial-frame ceilings, read suspension, fair writes,
  hard-close thresholds, and peer-data drop policy;
- a write-ledger extension point requiring any later partially accepted frame
  to remain connection-head ordered and end in completion or connection close;
- occupancy/work accounting for stream framing bytes and retained partial
  frames before a complete frame can acquire semantic ingress authority;
- allocation/global accounting of queued bytes and leased buffers.

Verification:

- `cargo test -p gjallarbru-runtime stream_backpressure`
- slow-reader, no-reader, partial-frame, fairness, and sustained-peer-load tests

Exit criteria:

- Every stream retains bounded memory and terminates stalled work deterministically.
- Stop: `v0.72.0 implementation stop reached. Run pentest for this exact commit.`

### v0.72.1 - Secure-Transport Memory Contract

Goal: define the mandatory memory/allocation qualification that every TLS/DTLS
provider must pass before its adapter can activate a secure listener.

Deliverables:

- provider-neutral phase taxonomy for configuration/key load, listener startup,
  connection/session creation, handshake, resumption, established record/frame
  processing, key update, retransmission, shutdown, failure, and replacement;
- required declarations for allocator behavior and maximum provider-owned
  plaintext, ciphertext, handshake-flight, pending-record, retransmission,
  session/ticket, certificate-chain, write-tail, and total connection bytes;
- fixed global/listener/tenant/connection/provider object and byte ceilings,
  including provider buffers not visible to core/runtime-owned pools;
- deterministic exhaustion/backpressure outcomes: suspend, bounded retry,
  reject, or close without hidden growth, deadlock, amplification, or false
  application completion;
- accepted plaintext/ciphertext forbidden from causing undeclared growable
  buffering or bypassing retained-byte/record counters;
- qualification harness with allocator instrumentation, retained-byte probes,
  provider/test-double fault injection, and secret/plaintext cleanup scanning;
- bounded connection-lifecycle allocation permitted by declared profile;
  hardened/accelerated established hot paths require zero allocator calls per
  frame after configured preallocation/warmup;
- providers unable to meet the zero-allocation hot-path contract excluded from
  those profiles while any portable profile remains measured and strictly bounded;
- cleanup, ownership, and best-effort zeroization contract for provider-owned
  plaintext, ciphertext, sessions, record tails, retransmission flights, and
  key-adjacent storage on every terminal path;
- integration with `v0.23.15`-`v0.23.17`: fence acknowledgement does not release
  provider memory, a silent provider enters bounded quarantine, and only typed
  provider-thread/buffer quiescence evidence permits physical release.

Verification:

- contract/test-double suite covering allocation, hidden growth, exhaustion,
  backpressure, partial acceptance, silent provider, cleanup, and zeroization
- compile/API checks requiring a memory qualification descriptor and counters
  before a TLS/DTLS adapter can construct an activatable listener
- fail-after-warmup fixtures proving hardened/accelerated profiles reject any
  established-frame allocation or undeclared retained byte

Exit criteria:

- No secure-transport provider can activate without finite declared memory,
  executable exhaustion behavior, ownership/cleanup rules, and profile-specific
  allocation evidence.
- Stop: `v0.72.1 implementation stop reached. Run pentest for this exact commit.`

### v0.72.2 - Secure Control-Traffic Budgets

Goal: bound TLS/DTLS post-handshake control work that consumes cryptography,
timers, state, or output without ever becoming a STUN/TURN plaintext frame.

Deliverables:

- provider-neutral control-event taxonomy and accounting before common plaintext
  ingress: inbound/outbound records and bytes, cryptographic operations, timer/
  retransmission work, generated responses, retained state, and control age;
- fixed per-connection, listener, tenant, source/prefix where observable, and
  global count/byte/rate/concurrency budgets with monotonic non-refundable
  charging and fair control-work scheduling independent of application permits;
- TLS 1.2 renegotiation disabled; TLS 1.3 post-handshake client authentication
  disabled unless a separately versioned profile later defines need and authority;
- TLS 1.3 `KeyUpdate`, including peer-requested reciprocal update, limited by
  minimum interval, lifetime count, concurrent/global crypto work, output bytes,
  and anti-ping-pong policy without extending TURN/session authority;
- bounded session-ticket/control-record generation with ticket count, encoded
  bytes, key-generation, rate, lifetime, and retained-session ceilings;
- bounded DTLS acknowledgements, flights, retransmissions, key updates,
  connection-ID processing, path/migration attempts, and generated control
  output, integrated with anti-amplification and path-identity policy;
- adapters expose normalized events/counters before performing expensive or
  state-growing work, or enforce an equivalent reviewed provider-internal limit
  whose configuration and exhaustion evidence is part of qualification;
- deterministic over-budget action per event/version/provider—ignore where safe,
  suppress reciprocal output, reject migration, or close the secure session—
  without plaintext delivery, allocation refresh, retry refund, or unbounded alerts;
- redacted fixed-cardinality metrics distinguish control-budget exhaustion from
  malformed transport and application ingress without leaking keys/session IDs.

Verification:

- `cargo test -p gjallarbru-runtime secure_control_budget`
- TLS renegotiation/post-handshake-auth rejection and KeyUpdate request/reciprocal-
  update flood tests across boundary counts, rates, concurrency, and output bytes
- ticket/control-record generation tests covering churn, rotation, resumption,
  no-reader backpressure, and provider-generated bursts
- DTLS acknowledgement/retransmission/key-update/CID/migration/loss/reorder
  matrices with anti-amplification, timer, memory, and CPU accounting
- provider/test-double tests proving no control path reaches plaintext ingress or
  bypasses an exposed event/counter or equivalent reviewed internal ceiling

Exit criteria:

- Every secure-transport control path is disabled or consumes finite authority
  before work/output; control-only traffic cannot bypass application admission.
- Stop: `v0.72.2 implementation stop reached. Run pentest for this exact commit.`

### v0.73.0 - TLS Provider Adapter

Goal: integrate TLS without placing certificate or record logic in core.

Deliverables:

- reviewed provider dependency/feature/license/MSRV decision and plaintext connection adapter;
- provider-specific `v0.72.1` memory descriptor, ceilings, counters,
  instrumentation, backpressure, cleanup, and profile admission evidence;
- provider-specific `v0.72.2` normalized control events or reviewed equivalent
  internal limits, with renegotiation/post-handshake authentication disabled and
  KeyUpdate/ticket/control-record work charged before plaintext ingress;
- certificate/key loading, handshake/result normalization, session cleanup, and
  mandatory rejection of TLS/provider early application data before framing,
  authentication, or core processing;
- an exact provider plaintext-output acceptance result distinct from encrypted
  record buffering and eventual kernel write completion, consumed by `v0.79.3`;
- dedicated handshake budgets followed by one common `v0.30.3`-`v0.30.5`
  two-stage ingress permit for every handshake-confirmed plaintext frame;
- provider substitution tests proving the adapter cannot accidentally enable
  0-RTT through defaults, resumption, tickets, or termination metadata.

Verification:

- `cargo test -p gjallarbru-runtime tls_adapter`
- two-provider or provider/test-double differential framing and replayed
  early-data rejection tests where practical
- TLS lifecycle and steady-state allocation/retained-byte/exhaustion tests from
  the `v0.72.1` qualification harness
- TLS control-only flood and budget-exhaustion tests from the `v0.72.2` harness

Exit criteria:

- Core receives provider-validated decrypted transport data with no TLS implementation
  type; TURN authentication remains authoritative for client identity unless a separate,
  explicit mTLS profile is configured, and no early application byte reaches core.
- Stop: `v0.73.0 implementation stop reached. Run pentest for this exact commit.`

### v0.74.0 - Hardened TLS Deployment

Goal: apply current BCP 195 policy and bound all TLS work.

Deliverables:

- TLS version/cipher/certificate policy, handshake prefix/global quotas, timeout,
  chain/record limits, resumption/ticket rotation, key-log/dump policy, and reload;
- deployable `v0.72.2` control-budget defaults and immutable disabled-feature
  policy for renegotiation and post-handshake client authentication;
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
- trusted termination inputs normalized into the same per-frame ingress permit
  and charge path as direct TLS, without granting bypass authority to the proxy;
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
- provider-specific `v0.72.1` memory descriptor, flight/record/session ceilings,
  allocation instrumentation, backpressure, cleanup, and profile admission evidence;
- provider-specific `v0.72.2` acknowledgement/retransmission/key-update/CID/
  migration control events or reviewed equivalent internal limits;
- dedicated cookie/handshake/replay admission budgets followed by one common
  `v0.30.3`-`v0.30.5` two-stage permit per accepted plaintext datagram;
- migration/rebinding policy distinct from RFC 8016 mobility;
- mandatory rejection of DTLS/provider early application data before STUN/TURN
  framing or allocation/authentication state.

Verification:

- `cargo test -p gjallarbru-runtime dtls_adapter`
- RFC 7350 interoperability, loss/reorder/replay, session-reuse, and replayed
  early-data rejection tests
- DTLS lifecycle and steady-state allocation/retained-byte/exhaustion tests
  including retransmission-flight storage
- DTLS control-only flood and budget-exhaustion tests from the `v0.72.2` harness

Exit criteria:

- DTLS sessions cannot inherit stale allocations, bypass client-path identity,
  or deliver early application data to core.
- Stop: `v0.75.0 implementation stop reached. Run pentest for this exact commit.`

### v0.76.0 - DTLS Anti-Abuse

Goal: prevent spoofed handshakes and retransmissions from becoming amplification/CPU attacks.

Deliverables:

- cookie/anti-amplification policy, per-prefix/global handshake and byte ceilings,
  timeouts, flight/retransmit limits, buffer accounting, and provider failure isolation;
- post-handshake `v0.72.2` acknowledgement/retransmission/key-update/CID/
  migration budgets retained after cookie validation and handshake completion;
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

### v0.76.2 - Cross-Provider Early-Data Closure

Goal: prove that the early-data rejection already required by the initial TLS
and DTLS adapters is consistent across every production provider and topology.

Deliverables:

- TLS/DTLS 0-RTT and provider-specific early application data disabled by
  default for every listener, profile, resumption ticket, and termination topology;
- unconditional rejection before semantic processing for Allocate, Refresh,
  CreatePermission, ChannelBind, Send, mobility, token, credential, admin, and
  every other stateful or replay-sensitive operation;
- no blanket “idempotent STUN” exception: any future enablement requires a
  separately versioned method-level replay-safety proof, bounded replay cache,
  deployment threat model, provider evidence, and interoperability profile;
- early-data status carried through trusted termination metadata without
  allowing an untrusted proxy to claim handshake-confirmed traffic;
- ticket rotation, anti-replay provider behavior, fallback, and rejection
  metrics that reveal no credential or method-sensitive detail.

Verification:

- direct TLS/DTLS and trusted-termination tests replaying early data across
  tickets, nodes, regions, process restart, loss, and handshake fallback
- provider substitution proving early bytes never reach wire/auth/core method
  processing and confirmed post-handshake retransmission remains interoperable

Exit criteria:

- No STUN/TURN application request is authorized from early data, and any future
  exception requires its own reviewed release contract.
- Stop: `v0.76.2 implementation stop reached. Run pentest for this exact commit.`

### v0.76.3 - Cross-Provider Secure-Transport Memory Closure

Goal: close the `v0.72.1` memory contract across every selected TLS/DTLS
provider, version, platform, and production profile before shared-port and
performance work expands the secure-transport surface.

Deliverables:

- audited `v0.72.1` provider/version/platform memory declarations separating configuration/key
  load, listener startup, connection/session creation, handshake, resumption,
  established record processing, key update, shutdown, and failure paths;
- explicit allocation policy for every phase, with bounded connection-lifecycle
  allocation permitted only under fixed global/listener/tenant/connection byte
  and object ceilings;
- maximum provider-owned plaintext, ciphertext, handshake-flight, pending-
  record, retransmission, session/ticket, certificate-chain, and write-tail bytes;
- deterministic provider-storage exhaustion/backpressure behavior: read/write
  suspension, bounded retry, handshake rejection, frame rejection, or connection
  close without hidden growth, deadlock, amplification, or semantic partial success;
- accepted plaintext/ciphertext and coalesced frames forbidden from triggering
  undocumented growable buffers or escaping the declared byte/object counters;
- fail-after-handshake allocation instrumentation for established TLS and DTLS
  record/frame paths; hardened/accelerated profiles require zero allocator
  calls per steady-state frame after configured preallocation/warmup;
- a provider that cannot meet the allocation-free hot-path contract explicitly
  excluded from those profiles while any portable profile remains bounded,
  measured, documented, and unable to claim zero-allocation performance;
- exact cleanup ownership for provider plaintext/ciphertext buffers, session
  objects, record tails, retransmission flights, and keys on failure, timeout,
  cancellation, disconnect, reload, provider replacement, and process shutdown;
- best-effort zeroization requirements and documented library/OS limitations
  for provider-owned plaintext and key-adjacent memory;
- integration with `v0.23.15`-`v0.23.17`: fence acknowledgement never releases
  provider storage still externally reachable, silent providers escalate into
  bounded quarantine, and provider/domain destruction releases storage only
  with complete typed thread/buffer quiescence evidence.

Verification:

- `cargo test -p gjallarbru-runtime secure_transport_memory`
- allocation/retained-byte instrumentation across TLS 1.2/1.3 and declared DTLS
  1.2/1.3 providers, handshake/resumption/key-update/steady-state/shutdown phases
- maximum-size and fragmented/coalesced records, slow peer, no-reader, provider
  backpressure, record-buffer exhaustion, retransmission, and failure matrices
- fail-after-handshake allocator tests proving the qualified established hot
  paths allocate zero or the provider/profile is rejected as declared
- secret/plaintext scanning and cleanup/zeroization tests after failure,
  disconnect, timeout, replacement, crash containment, and repeated session churn
- two-provider/test-double differential accounting proving provider internals
  cannot alter core framing, authority, completion, or resource truth

Exit criteria:

- Every active TLS/DTLS provider has measured finite memory behavior, explicit
  phase-specific allocation policy, fail-closed backpressure, and complete
  cleanup evidence; no declared provider/platform/profile remains unqualified.
- Stop: `v0.76.3 implementation stop reached. Run pentest for this exact commit.`

### v0.76.4 - Cross-Provider Secure Control Closure

Goal: prove every selected TLS/DTLS provider, version, platform, and termination
topology enforces the `v0.72.2` post-handshake control policy equivalently before
shared-port and performance work enlarge the transport attack surface.

Deliverables:

- audited provider/version capability matrix for TLS renegotiation, post-
  handshake authentication, KeyUpdate/reciprocal update, tickets/control
  records, DTLS acknowledgements/retransmissions/key updates/CID/migration;
- proof each active path exposes normalized pre-work events/counters or has
  reviewed provider-internal limits no broader than the configured Gjallarbru
  connection/listener/tenant/global budgets;
- provider-independent charge/result normalization for accepted, ignored,
  suppressed, rejected, over-budget, unsupported, and session-closing outcomes;
- configuration validation refusing a provider/profile when a required feature
  cannot be disabled, bounded, observed, or safely isolated;
- trusted TLS termination contract carrying authenticated aggregate control-
  budget evidence where applicable without trusting client-supplied metadata or
  pretending upstream proxy work was locally charged;
- mixed-version/node configuration compatibility so load balancing cannot move
  clients onto a weaker control policy, with rollout gates and downgrade rejection;
- operational defaults, metrics, alert thresholds, and incident evidence for
  control-budget exhaustion without unbounded labels or sensitive session data.

Verification:

- `cargo test -p gjallarbru-runtime secure_control_provider_closure`
- cross-provider differential control traces for all declared TLS 1.2/1.3 and
  DTLS 1.2/1.3 profiles, including unsupported/opaque provider behavior
- renegotiation, post-handshake-auth, KeyUpdate ping-pong, ticket burst, DTLS
  loss/retransmit/ACK/CID/migration flood, and mixed-control attack suites
- direct, shared-port, trusted-termination, restart, reload, cluster mixed-
  version, and budget-saturation matrices with exact counters and output bounds
- negative provider-substitution tests proving activation fails when equivalent
  pre-work enforcement cannot be demonstrated

Exit criteria:

- No advertised secure provider or topology accepts unbounded post-handshake
  control work, and provider choice cannot weaken the normalized budget policy.
- Stop: `v0.76.4 implementation stop reached. Run pentest for this exact commit.`

### v0.77.0 - Standard Shared-Port Demultiplexing

Goal: implement standardized first-byte demux without inventing TURN-over-QUIC.

Deliverables:

- RFC 7983 and RFC 9443 range table, STUN/ChannelData/DTLS/QUIC classification,
  ambiguous/invalid handling, and configuration collision checks;
- bounded demultiplexing work followed by transport-specific admission that
  cannot skip the common plaintext ingress permit;
- docs explicitly separating shared port from transport encapsulation.

Verification:

- `cargo test -p gjallarbru-wire shared_port`
- exhaustive 256 first-byte classification plus integration fixtures

Exit criteria:

- Shared listeners route only standardized ranges and make no proprietary TURN claim.
- Stop: `v0.77.0 implementation stop reached. Run pentest for this exact commit.`

### v0.77.1 - Common Transport Ingress Accounting

Goal: prove every client transport reaches semantic STUN/TURN processing through
one normalized work-permit model with no alternate-transport budget bypass.

Deliverables:

- one normalized ingress descriptor for UDP datagrams, complete TCP/TLS frames,
  DTLS plaintext datagrams, trusted-termination frames, and shared-port dispatch;
- mandatory just-in-time `v0.30.3`-`v0.30.5` unclassified permit acquisition
  after required transport handshake/replay/framing admission, followed by
  fixed-header classification and class reservation before semantic parsing;
- separate bounded occupancy/work charges for TCP/TLS framing bytes and retained
  partial frames, with one semantic permit and charge lifecycle per complete frame;
- TLS/DTLS cookie, handshake, record, replay, and retransmission work kept under
  their dedicated budgets, including `v0.72.2` post-handshake control events;
  accepted plaintext then pays common packet/parse, HMAC, credential-lookup,
  preparation, response, and send charges;
- coalesced frames, batched datagrams, and shared-port classifications admitted
  independently, never through one aggregate permit or batch reservation;
- trusted termination metadata may establish reviewed path provenance but
  cannot waive, refill, refund, or alter semantic ingress accounting;
- transport-independent accounting/event snapshots and failure outcomes suitable
  for scalar/batched/provider differential comparison.

Verification:

- `cargo test -p gjallarbru-runtime common_transport_ingress`
- identical valid/malformed/authentication/retransmission corpora across UDP,
  TCP, TLS, DTLS, trusted termination, and shared-port configurations
- fragmented and coalesced stream frames, replayed DTLS datagrams, handshake
  failure/success, demux ambiguity, queue delay, permit expiry, and overload tests
- differential ledgers proving equal semantic work receives equal charges,
  each frame has one permit, dedicated handshake charges do not replace semantic
  charges, and no transport path refunds or bypasses started attempts

Exit criteria:

- Every admitted plaintext STUN/TURN frame uses the same bounded semantic-work
  authority, while transport framing and secure-handshake work remain separately
  bounded and cannot create accounting gaps.
- Stop: `v0.77.1 implementation stop reached. Run pentest for this exact commit.`

### v0.78.0 - Per-Core Ownership

Goal: remove global allocation locks while retaining one authoritative owner per flow.

Deliverables:

- worker-local stores/timers/buffers/relays, stable flow steering, bounded cross-worker control,
  immutable configuration epochs, and ownership migration prohibition;
- per-worker execution domains implementing `v0.23.12` authority sequences and
  `v0.23.13` coalesced lane watermarks across cross-worker queues before
  ownership/identifier reuse;
- `v0.23.15`-`v0.23.17` separation of semantic worker-epoch retirement from
  physical queue/buffer reuse, with typed quiescence required after worker loss;
- safe single-worker reference retained for differential tests;
- initial focused Loom models for bounded cross-worker queue publication,
  ownership epochs, immutable configuration publication, cancellation, and
  shutdown/fence acknowledgement ordering.

Verification:

- `cargo test -p gjallarbru-runtime worker_ownership`
- concurrency/model tests proving no normal global allocation mutex or
  cross-worker relay path, plus routine small Loom models for the first
  concurrent structures

Exit criteria:

- Every client path and relay completion reaches exactly one owning worker, and
  the first cross-worker/publication races have executable model evidence.
- Stop: `v0.78.0 implementation stop reached. Run pentest for this exact commit.`

### v0.78.1 - Expanded Concurrency-Model Closure

Goal: expand the initial v0.78.0 concurrency evidence across the full
cross-worker configuration and lifecycle surface before acceleration.

Deliverables:

- focused Loom models for bounded cross-worker enqueue/dequeue, wakeup/lost-
  wakeup handling, ownership epochs, authority-fence acknowledgement, and
  stale-message rejection;
- immutable configuration generation publication and reader lifetime model,
  including reload, rollback, retirement, and shutdown races;
- worker start/drain/abort/restart and command cancellation ordering with no
  double completion, leaked lease, reused authority, or stranded accepted effect;
- typed quiescence-proof publication/acceptance races, incomplete resource
  manifests, and stale worker/provider proof rejection under `v0.23.17`;
- model sizes and abstractions kept small enough for routine CI, with promoted
  counterexamples retained as deterministic regression tests;
- v0.93.0 remains the comprehensive Loom/Miri/sanitizer inventory rather than
  the first time these concurrent structures receive model evidence.

Verification:

- routine bounded Loom runs plus mutation/fault variants for queue ordering,
  publication, ownership transfer prohibition, cancellation, and shutdown
- worker-death versus late-access/quiescence-proof models proving physical
  storage cannot re-enter a pool before every external accessor is unreachable
- scalar/single-worker differential tests and repeated real-thread stress runs
  for every modeled outcome

Exit criteria:

- The initial models are expanded to cover every concurrent ownership and
  publication lifecycle needed before batching, `io_uring`, or kernel fast paths.
- Stop: `v0.78.1 implementation stop reached. Run pentest for this exact commit.`

### v0.79.0 - Batched I/O

Goal: improve throughput with bounded batching without changing protocol results.

Deliverables:

- portable batch abstraction plus Linux `recvmmsg`/`sendmmsg`, fairness budget,
  partial-send/error handling, and worker-local registries;
- per-packet just-in-time permit acquisition: receive batching never reserves
  permits or HMAC/lookup capacity for the batch as a whole;
- benchmarks against safe one-packet reference behavior.

Verification:

- differential packet/result/ingress-ledger suite and batch-size fairness/load benchmarks
- syscall/error fault injection

Exit criteria:

- Batching measurably improves target workloads and never changes authorization decisions.
- Stop: `v0.79.0 implementation stop reached. Run pentest for this exact commit.`

### v0.79.1 - Batch Completion Semantics

Goal: prove that syscall batching changes amortization only, including partial
success and stale-result behavior.

Deliverables:

- normalized receive events retaining remote address, local destination,
  transport, truncation state, buffer generation, operation ID, and worker epoch;
- scalar core invocation for every admitted packet with bounded per-batch
  fairness and no batch-wide authorization shortcut;
- send completion plans distinguishing sent, unsent, retryable, permanently
  failed, cancelled, and stale packets without reporting unsent work as success;
- deterministic queue/retry ordering and reconciliation counters across
  `recvmmsg`, `sendmmsg`, and portable fallback.

Verification:

- scalar-versus-batched differential traces for all batch sizes, partial-send
  positions, error mixes, truncation, stale buffers, and worker epochs
- syscall fault injection plus accounting proving each packet is completed,
  retried, or dropped exactly once

Exit criteria:

- Batch boundaries and partial syscalls cannot alter path identity, core
  decisions, lease ownership, counters, or completion truth.
- Stop: `v0.79.1 implementation stop reached. Run pentest for this exact commit.`

### v0.79.2 - Partial-Batch Capability Consumption

Goal: preserve single-use delivery authority and exclusive buffer ownership
when a batched send accepts only a prefix or reports per-entry partial results.

Deliverables:

- per-packet send states `Queued -> Validated -> HandedOff` or
  `Validated -> Unsent`, plus declared terminal transitions after handoff;
- validation of each entry's client/peer capability, deadline, queue age,
  generations, exact charge, buffer, and `v0.23.12` fence immediately before
  the batch syscall/provider submission, including `v0.43.2` canonical peer,
  permission generation, and ChannelData channel generation for relay media,
  using sealed capability checks rather than runtime inspection of core state;
- only the prefix/entries reported accepted by the OS/provider consume their
  single-use capabilities and enter bounded in-flight state;
- unsent entries retain exclusive capability and buffer/lease ownership, emit
  no send completion, and cannot be mistaken for failed or successful handoff;
- a stream/vector entry with a partially accepted byte range consumes its
  capability once and retains the unsent tail inside the same bounded in-flight
  operation, never as a fresh reusable capability or uncharged retry;
- retry requires fresh validation of deadline, queue age, client path/peer
  permission, allocation/transaction, worker/configuration, buffer generation,
  acknowledged authority sequence, and exact live permission/channel generations;
- a stale unsent relay-media entry drops by default; an enabled `v0.43.3`
  reauthorization returns the exact owned entry to core once and the batch/
  provider adapter cannot construct or modify its replacement capability;
- expiry, revocation, disconnect, policy/translation change, worker restart, or
  buffer-generation reuse between partial return and retry deterministically
  invalidates the unsent entry;
- retry consumes the `v0.23.6` declared new attempt charge unless a bounded
  idempotency budget explicitly authorizes reuse; a consumed capability is
  never reconstructed, refunded, or retried;
- scalar, `sendmmsg`, provider-vector, stream-vector, and future `io_uring`
  paths expose one equivalent per-entry result contract.

Verification:

- `cargo test -p gjallarbru-runtime partial_batch_capability`
- every accepted-prefix length and sparse provider-result pattern across mixed
  client/peer capabilities, errors, deadlines, charges, and buffer classes
- partial-byte acceptance inside first/middle/last stream-vector entries,
  including tail ownership, disconnect, cancellation, and timeout
- expiry, revocation, disconnect, mapping/policy reload, fence advance,
  permission/channel refresh or rebind, worker restart, and buffer reuse
  injected between partial return and retry
- enabled/disabled core-only reauthorization tests proving original enqueue age,
  charge, buffer ownership, and one-attempt limit survive partial batch return
- property/model tests proving accepted entries consume once, unsent entries
  retain one owner, retry charges correctly, and no entry receives false completion
- scalar/batched/provider differential traces including cancellation and
  `v0.23.11` late/conflicting terminal observations

Exit criteria:

- Partial batch acceptance consumes authority only for work actually handed to
  the OS/provider; every unsent entry remains exclusively owned and must still
  be live, acknowledged, and correctly charged before any retry.
- Stop: `v0.79.2 implementation stop reached. Run pentest for this exact commit.`

### v0.79.3 - Partial Stream-Frame Closure

Goal: preserve TCP/TLS framing and delivery truth when only part of one
client-bound frame has crossed the runtime/provider handoff boundary.

Deliverables:

- one ordered per-connection write ledger whose partially accepted frame
  remains at the head until its tail completes or the connection closes;
- later responses, indications, ChannelData frames, and relay bytes forbidden
  from overtaking or interleaving with the retained tail;
- the frame's single-use client-delivery capability consumed exactly once at
  first accepted byte, with the tail owned by that same bounded in-flight
  operation rather than reauthorized or charged as a new semantic delivery;
- exact retained-tail byte, age, retry/write-attempt, provider-buffer, and
  connection-wide ceilings with fair scheduling across other connections;
- operation-specific already-in-flight policy after authority expiry,
  revocation, cancellation, shutdown, or local timeout: the tail may finish
  only within a fixed byte/time window, otherwise the connection must close;
- dropping/truncating the tail while keeping the connection open forbidden,
  including best-effort indications, because stream framing would be corrupted;
- exact TCP syscall and TLS-provider acceptance boundaries: provider acceptance
  reports the plaintext prefix transferred into provider-owned output, while
  encryption, record coalescing, and eventual kernel writes remain separately
  tracked and cannot invent application-level completion;
- provider-owned output/tail state remains inside the qualified `v0.72.1` and
  `v0.76.3` byte/object ceilings, allocation profile, backpressure, ownership,
  cleanup, and zeroization contract throughout every partial-frame retry;
- disconnect/close releases the tail, provider buffers, leases, capability,
  charges, and terminal mailbox ownership exactly once without attempting to
  resume the frame on a replacement connection.

Verification:

- `cargo test -p gjallarbru-runtime partial_stream_frame`
- every partial byte offset for STUN responses, Data indications, ChannelData,
  and representative RFC 6062 control frames
- later-frame ordering/interleaving assertions plus tail expiry, revocation,
  cancellation, timeout, shutdown, provider failure, and connection-close tests
- two-provider/test-double acceptance-boundary differential tests distinguishing
  plaintext provider acceptance, encrypted-record buffering, and kernel writes
- secure-provider retained-byte exhaustion and fail-after-warmup tests proving
  a partial frame cannot escape provider ceilings or trigger hidden allocation
- bounded in-flight window exhaustion proving either complete frame bytes in
  order or connection close—never a truncated frame followed by later traffic

Exit criteria:

- A consumed partial stream frame either completes in order within its bounded
  in-flight window or closes the connection; its tail is never dropped,
  overtaken, reauthorized, or moved to another connection.
- Stop: `v0.79.3 implementation stop reached. Run pentest for this exact commit.`

### v0.79.4 - UDP GRO/GSO Segment Semantics

Goal: admit optional UDP receive coalescing and send segmentation only when
every original datagram/segment remains semantically equivalent to scalar I/O.

Deliverables:

- platform capability detection and disabled-by-default fallback for UDP GRO/
  GSO, with no requirement that a supported OS/provider expose either feature;
- GRO input split into exact original datagram views using validated segment
  metadata, each retaining remote/local destination, interface/scope, ECN/TOS,
  truncation, listener/worker/buffer generations, and independent admission;
- no aggregate parse, HMAC, credential, transaction, policy, quota, or command
  permit: every reconstructed datagram pays the same work and byte/packet charge
  and produces the same core event/result as scalar receive;
- malformed/inconsistent segment size, final short segment, ancillary metadata,
  overflow, or provider ambiguity rejects/punts without treating concatenated
  bytes as one STUN/ChannelData frame;
- GSO output accepts only equal compatible segment plans whose individual
  capabilities, buffers, charges, deadlines, destinations, and generations were
  validated; aggregation creates no broader destination or authority;
- exact per-segment handoff/completion/error contract, including provider
  behavior that reports only whole-superpacket status, with unsupported partial
  truth falling back to scalar sends rather than inventing completions;
- buffer/lease ownership and copy/allocation counters integrated with
  `v0.79.2`, `v0.80.0`, and `v0.80.1`, with scalar fallback always available.

Verification:

- `cargo test -p gjallarbru-runtime udp_gro_gso_semantics`
- every segment count/size/final-length, maximum buffer, mixed STUN/ChannelData,
  malformed metadata, ancillary mismatch, truncation, and exhaustion case
- scalar-versus-GRO event/result/charge traces and scalar-versus-GSO wire/
  completion traces under loss, error, cancellation, revocation, and stale epochs
- capability/destination/charge substitution and aggregate-permit adversary tests
- platform/provider matrix proving ambiguous completion semantics disable GSO
  and unsupported GRO/GSO changes performance only

Exit criteria:

- GRO/GSO changes syscall amortization only; each original datagram retains its
  exact scalar parsing, authorization, accounting, ownership, and completion truth.
- Stop: `v0.79.4 implementation stop reached. Run pentest for this exact commit.`

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

- Claimed packet paths allocate nothing after their `v0.80.1` named warm-up
  boundary and never reuse a live lease.
- Stop: `v0.80.0 implementation stop reached. Run pentest for this exact commit.`

### v0.80.1 - Measured Allocation and Copy Profiles

Goal: replace one global zero-copy/zero-allocation slogan with exact measurable
profiles for each transport phase and deliberately retained copy boundary.

Deliverables:

- separately versioned profiles for UDP/STUN steady state after worker startup,
  UDP/TURN relay after pool initialization, TCP after connection admission,
  TLS/DTLS handshake/session lifecycle, and established TLS/DTLS records/frames;
- each profile declares warm-up boundary, allowed allocator calls/bytes, pool/
  stack/static/provider-owned bytes, copies and copied bytes, retained bytes,
  tasks/timers, descriptors, scatter segments, and deterministic exhaustion;
- UDP/STUN and UDP/TURN steady state require zero allocator calls; TCP steady
  state requires zero calls after configured connection storage admission;
- secure handshake/lifecycle allocation may be finite and measured under
  `v0.72.1`; hardened established TLS/DTLS paths require zero calls after warm-up
  or explicitly reject that provider/platform/profile;
- deliberate bounded copies classified by reason—ownership transfer, secret
  isolation, provider boundary, platform limitation, or pre-lease relay safety—
  and kept distinct from avoidable copies and false universal zero-copy claims;
- worker-scoped fail-after-warm-up allocator plus isolated-process test mode so
  unrelated harness/global allocations cannot mask or falsely fail packet paths;
- allocation/copy/retention counters integrated from wire cursor/encoder,
  PRECIS, transaction evidence/cache, prepared transitions/queues, credentials,
  relay payloads/leases, logs/errors, and TLS/DTLS provider buffers;
- reference safe scalar profile retained for differential comparison with
  batching, `io_uring`, and later kernel acceleration; acceleration may reduce
  work but cannot weaken semantic or resource evidence.

Verification:

- `cargo test -p gjallarbru-runtime allocation_copy_profiles`
- isolated fail-allocator runs for valid, malformed, auth failure, cache hit/
  miss, allocation/relay, stream fragmentation, slow reader, provider failure,
  exhaustion, cancellation, disconnect, reload, and shutdown paths
- exact counter/copy-reason assertions at profile boundaries plus maximum-size,
  sustained churn, and retained-byte leak/plateau tests
- portable/batched/provider/platform differential reports and negative fixtures
  proving a single hidden allocation, unclassified copy, or undeclared retained
  byte rejects the claimed profile
- documentation tests preventing “zero-copy” or “allocation-free” claims without
  a named profile, warm-up boundary, provider/platform set, and evidence artifact

Exit criteria:

- Every performance/resource claim names an executable profile; Gjallarbru can
  prove zero unnecessary copies without denying intentional security copies.
- Stop: `v0.80.1 implementation stop reached. Run pentest for this exact commit.`

### v0.81.0 - `io_uring` Backend

Goal: add measured Linux `io_uring` acceleration behind the unchanged runtime contract.

Deliverables:

- fixed files/buffers, multishot capability detection, bounded in-flight operations,
  generation-tagged user data, cancellation, shutdown, and portable fallback;
- `v0.79.2` per-entry capability consumption and unsent/retry semantics for
  linked, multishot, or vector submissions with partial acceptance;
- `v0.79.3` ordered stream-tail ownership/close semantics where `io_uring`
  accepts only part of a stream frame;
- `v0.23.17` adapter proof covering ring disable/exit, completion drain,
  registered file/buffer unregister, worker/process death where used, and the
  exact quarantined fixed-resource inventory before physical reuse;
- isolated unsafe/syscall modules with safety evidence.

Verification:

- differential portable/batched/`io_uring` suite, Miri-safe helpers, sanitizers,
  stale completion, cancellation, unsupported-kernel, and overload tests
- failed unregister, late completion after close, live ring worker, partial
  inventory, stale proof, and clean quiescence/reuse tests

Exit criteria:

- Disabling `io_uring` changes performance only and unsafe invariants are reviewed.
- Stop: `v0.81.0 implementation stop reached. Run pentest for this exact commit.`

### v0.82.0 - Optional eBPF and AF_XDP Fast Path

Goal: accelerate only traffic already authorized by live core state.

Deliverables:

- ingress filtering/steering and optional rules containing allocation generation,
  the exact `v0.37.4` authorized endpoint fields, direction, channel, expiry,
  policy epoch, and byte/packet budgets, with client-bound relay rules also
  binding the `v0.43.2` permission generation and ChannelData channel generation;
- install commands derived from typed fast-path capabilities, with kernel/user
  adapters forbidden from reconstructing or widening raw endpoints;
- install/remove ordering, map-capacity, fail-closed miss, and reconciliation checks.

Verification:

- core-rule subset property, stale/expired/epoch mismatch, endpoint-substitution/
  widening tests, XDP-disabled differential suite, verifier/load/eviction tests,
  and performance report

Exit criteria:

- Kernel rules cannot create, refresh, broaden, or outlive core authorization.
- Stop: `v0.82.0 implementation stop reached. Run pentest for this exact commit.`

### v0.82.1 - Fast-Path Revocation Closure

Goal: make revocation, expiry, reuse, and reconciliation authoritative even
when packets bypass the ordinary userspace relay path.

Deliverables:

- remove-or-invalidate-before-reuse ordering for allocation/channel/policy
  generations and emergency revocation;
- `v0.23.12` authority sequences carried by every rule/install/remove command,
  with `v0.23.13` coalesced high-water acknowledgement from each kernel
  map/program/queue lane before reuse;
- kernel expiry that is never later than core expiry, with bounded clock/
  epoch translation and fail-closed uncertainty;
- map loss, eviction, reload, worker restart, reconciliation failure, and
  partial update behavior that drops or returns traffic to the slow path;
- missing/uncertain fence acknowledgement destroys or replaces the fast-path
  execution domain with a disjoint generation and never relies on map FIFO;
- fence acknowledgement never releases registered buffers, map values, UMEM
  frames, descriptors, or provider slots still reachable by accepted fast-path
  work; `v0.23.15` terminal reconciliation or `v0.23.17` typed map/queue/UMEM/
  DMA quiescence evidence is required;
- `v0.23.16` bounds unresolved remove/reconcile attempts, age, counts, and
  quarantined physical ownership, failing new acceleration admission rather
  than evicting another unresolved rule or aliasing its storage;
- rules binding generation, direction, endpoints, policy epoch, quotas, expiry,
  worker ownership, and applicable permission/channel generations, plus
  complete install/remove/reconcile audit evidence.

Verification:

- revoke/reuse races, expiry boundary, clock skew, map loss/eviction, partial
  update, restart, stale epoch, and reconciliation-failure model tests
- multi-map/program/queue fence acknowledgement, lost acknowledgement, domain
  destruction, typed unregister/drain/DMA-quiescence proof, and disjoint-
  generation replacement tests
- accepted-packet versus fence-acknowledgement ownership races, silent remove/
  reconcile providers, unresolved-budget exhaustion, and UMEM/map-storage
  non-aliasing tests
- fast-path-disabled/slow-path differential traffic and authorization suite
  with rule/core inventory reconciliation under load

Exit criteria:

- No kernel rule survives authority revocation or identifier reuse, and any
  uncertain fast-path state becomes inert before traffic is admitted.
- Stop: `v0.82.1 implementation stop reached. Run pentest for this exact commit.`

### v0.82.2 - Fast-Path Quota Leases

Goal: make accelerated packet/byte budgets finite leased authority rather than
an independently refillable kernel quota system.

Deliverables:

- core-issued packet/byte budget leases bound to allocation, direction,
  endpoints, policy/quota generation, worker epoch, and expiry;
- kernel code permitted only to decrement the finite lease and never refill,
  extend, transfer, or derive a new budget;
- consumption reconciled with core before renewal, with uncertainty, lost
  counters, map replacement, CPU migration, or partial reads preventing renewal;
- unused authority reclaimed or invalidated on expiry, revocation, rule removal,
  allocation teardown, worker restart, and generation reuse;
- bounded overshoot analysis for in-flight packets/counters plus fail-closed
  fallback or drop when strict accounting cannot be demonstrated.

Verification:

- exhaustion, renewal, concurrent consumption, lost accounting, map loss,
  reconciliation race, expiry, revoke, restart, and reuse model tests
- slow-path quota differential and load tests proving total kernel plus
  userspace consumption never exceeds the documented lease/overshoot bound

Exit criteria:

- Fast-path accounting remains a strict finite subset of core quota authority,
  and uncertain consumption can never be renewed.
- Stop: `v0.82.2 implementation stop reached. Run pentest for this exact commit.`

## Phase G: Extended TURN Profiles and Assurance Foundations

### v0.83.0 - RFC 6062 State Model

Goal: define TCP relay semantics as a deterministic sans-I/O state machine before
opening TCP relay sockets.

Deliverables:

- bounded TCP allocation, pending-connection, connection-identifier, binding,
  expiry, and generation state;
- abstract `CONNECT`, `CONNECTION-ATTEMPT`, and `CONNECTION-BIND` events and
  commands, including duplicate and timeout behavior;
- every client-bound indication/control output modeled with `v0.30.6`
  authorized client-path authority rather than a raw connection/path handle.

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
  generation, identifier, replay, timeout, and cleanup checks;
- `CONNECTION-ATTEMPT` sent only through a live single-use `v0.30.6`
  client-delivery capability with acknowledged disconnect/revocation fencing.

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
- client-bound relay/control writes retain `v0.30.6` connection/path/fence
  authority plus `v0.79.2` per-entry consumption and `v0.79.3` ordered
  partial-tail completion-or-close semantics;
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
