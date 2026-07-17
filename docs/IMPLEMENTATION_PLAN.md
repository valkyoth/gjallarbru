# Gjallarbru Serious Implementation Plan

Status: planning document

Project and binary name: `gjallarbru`

Primary `1.0.0` target: the first serious production-ready STUN/TURN server
application and its reusable protocol crates.

This plan is derived from the completed initial design discussion. The settled
design is a portable `no_std` protocol authority with replaceable
operating-system, storage, authentication, cryptographic, secure transport, and
acceleration adapters.

## 1. Objective

Gjallarbru will provide:

- A first-party STUN/TURN wire implementation.
- A thin `no_std` `gjallarbru` facade over the reusable protocol crates.
- Borrowed, allocation-free, panic-free decoding.
- Caller-buffer encoding with exact integrity byte ranges.
- A deterministic, bounded Sans-I/O server core.
- UDP, TCP, TLS-over-TCP, and DTLS-over-UDP client transports.
- UDP TURN relaying plus the RFC 6062 TCP-relay extension.
- IPv4, IPv6, and dual-family allocations.
- IPv6-only, NAT64/464XLAT, multi-homed, one-to-one NAT, and explicitly
  advertised public relay-address deployments.
- Modern SHA-256 authentication with explicit legacy interoperability.
- Short-lived, purpose-bound Pawalyze credentials with OpenBao-backed rotation.
- Node-local allocation authority with tested multi-node and regional recovery.
- A private, mutually authenticated cluster protocol for membership, health,
  capacity, drain, and version coordination across two or more nodes.
- A tested Fluxheim TCP/TLS load-balancer profile with an honest direct-UDP boundary.
- Qualified rootless Docker/Podman networking with Wolfi and Debian images.
- A mandatory minimum destination/loop policy, fixed resource ceilings, and
  pre-authentication work budgets before any relay traffic, followed by
  configurable policy, hierarchical quotas, rate limits, and bounded telemetry.
- Portable runtimes for Linux, Windows, BSD, macOS, Android, and iOS.
- Fixed-capacity interfaces suitable for an eventual Aesynx adapter.
- Optional Linux acceleration that cannot bypass core authorization.
- Requirement-by-requirement RFC, errata, test, and implementation evidence.

The project does not implement TLS, DTLS, digest primitives, CSPRNGs, Unicode,
or PRECIS from scratch. It does implement all STUN/TURN-specific parsing,
encoding, authentication ordering, validation, state, and relay authority.

## 2. Standards Baseline

| Profile | Standards | Purpose |
| --- | --- | --- |
| `stun-base` | RFC 8489, RFC 5769 | STUN messages, Binding, authentication, official vectors |
| `turn-udp-base` | RFC 8656 | UDP allocations, IPv4/IPv6, permissions, channels |
| `turn-stream` | RFC 8656 | TCP and TLS client transports and stream framing |
| `endpoint-uri` | RFC 7064, RFC 7065 | Standard STUN/STUNS and TURN/TURNS endpoint URIs |
| `turn-discovery` | RFC 5928, RFC 8155 | DNS resolution and auto-discovery deployment behavior |
| `ip-translation` | RFC 6052 | IPv4-embedded IPv6 formats and validated NAT64 prefix handling |
| `auth-text` | RFC 7376, RFC 8265 | Authentication threat analysis and current PRECIS profiles |
| `turn-tls` | RFC 7443, RFC 9325 | ALPN identity and current TLS deployment policy |
| `turn-dtls` | RFC 7350, RFC 9147, RFC 9325 | DTLS 1.2 transport, DTLS 1.3 disposition, and secure policy |
| `turn-tcp-relay` | RFC 6062 | TCP allocations and peer connections |
| `turn-third-party-auth` | RFC 7635 | Access-token authorization |
| `turn-mobility` | RFC 8016 | Allocation mobility tickets |
| `stun-behavior-discovery` | RFC 5780 | Isolated experimental diagnostic listener |
| `stun-ecn-check` | RFC 6679 | Explicit implemented or reviewed-excluded ECN check behavior |
| `stun-measurement` | RFC 7982 | Bounded loss and RTT measurement attributes |
| `shared-port` | RFC 7983, RFC 9443 | Standard packet demultiplexing only |

RFC 8656, not RFC 5766 plus RFC 6156, defines the base TURN model. A
de-facto time-limited shared-secret credential profile may be supported but is
never labeled an RFC feature. RFC 9443 does not make TURN-over-QUIC or
TURN-over-WebTransport standard; custom transports remain separate protocols
and are not substituted for standard TURN.

## 3. Non-Negotiable Engineering Rules

### 3.1 Rust and portability

- Rust edition 2024 and resolver 3.
- Stable Rust `1.97.0` for main development.
- Verified MSRV range `1.90.0` through `1.97.0`.
- No nightly requirement for normal builds or releases.
- `gjallarbru`, `gjallarbru-wire`, `gjallarbru-crypto`, and
  `gjallarbru-core` are `no_std`.
- `alloc` is not used by the core packet path; any optional allocation feature
  must remain explicit and must not define the public protocol model.
- OS socket types never enter wire or core APIs.

### 3.2 Modularity

- `lib.rs` and `main.rs` are wiring and orchestration only.
- Parsing, validation, authentication, state, policy, storage, I/O, and tests
  live in focused modules.
- Non-generated Rust files remain below 500 lines and are reviewed for a split
  around 300 lines.
- A new crate is created only for a real trust, dependency, publication, or
  platform boundary; ordinary organization uses modules.
- Core crates never depend outward on runtime or deployment crates.

### 3.3 Security and resources

- Untrusted inputs cannot cause an unbounded loop, allocation, queue, lookup,
  cryptographic operation, log stream, or metric label set.
- No relay resource is opened before authentication, policy, and quota gates.
- Arithmetic involving offsets, lengths, counters, time, or capacity is
  checked or proven bounded.
- The protocol parser forbids unsafe code and direct unchecked indexing.
- Runtime unsafe code, when later necessary for syscalls or buffer ownership,
  is isolated, documented, and differentially tested against a safe backend.
- Capacity exhaustion has a deterministic, tested result.
- Protocol acceleration always fails closed.

## 4. Workspace and Trust Boundaries

### `gjallarbru`

Public `no_std`, unsafe-free, `MIT OR Apache-2.0` facade introduced by
`v0.55.1`. It owns no protocol implementation. It exposes the focused public
crates as stable `wire`, `crypto`, and `core` namespaces, uses the repository
README as its crates.io/docs.rs introduction with automated drift prevention,
and never depends on the EUPL runtime, cluster, or server packages.

### `gjallarbru-wire`

`no_std`, no allocation, no unsafe, preferably dependency-free.

Owns frame classification, STUN headers, methods/classes, borrowed attribute
iteration, typed attribute views, ChannelData, stream framing, caller-buffer
encoding, integrity ranges, and fingerprint framing. It owns no state, clock,
socket, credential database, or policy.

### `gjallarbru-crypto`

`no_std`, no unsafe in first-party STUN-specific code.

Owns provider traits and protocol composition for HMAC-SHA-1,
HMAC-SHA-256, MD5/SHA-256 long-term key derivation, constant-time comparison,
authenticated nonces, reservation tokens, mobility tickets, access tokens,
secret wrappers, and key generations. Reviewed primitive crates remain behind
local provider interfaces.

### `gjallarbru-core`

`no_std`, no packet-path allocation, no unsafe.

Owns Binding, authentication ordering, transactions, allocations,
permissions, channels, timers, quotas, destination policy, relay-port state,
and abstract runtime commands. It never reads system time or performs I/O.

### `gjallarbru-runtime`

Internal EUPL-1.2 `std` crate.

Owns portable sockets, worker loops, buffer pools, credential adapters,
TLS/DTLS adapters, logging, metrics, administrative transport, Linux batching,
`io_uring`, and optional eBPF/AF_XDP. Unsafe is allowed only in named modules
with safety documentation and safe reference tests.

### `gjallarbru-cluster`

Internal EUPL-1.2 `std` crate, introduced by `v0.96.1` and never published.

Owns the first-party bounded node-control codec, provider-neutral mTLS session
boundary, cluster/node identity, capability negotiation, membership views,
health/load summaries, convergence, drain coordination, and relay-pool lease
generations. It owns no STUN/TURN parsing, allocation/permission/channel state,
relay payload, browser credential, raw private key, socket fast path, or direct
worker mutation.

### `gjallarbru-server`

Internal EUPL-1.2 binary crate.

Owns configuration, listener and relay setup, privilege reduction, sandboxing,
key loading/rotation, health, administration, drain, shutdown, packaging, and
operator-facing errors.

The enforced dependency direction is:

```text
gjallarbru facade -> {wire, crypto, core}
server -> runtime -> {core, wire}
core -> {wire, crypto}
```

Runtime's direct wire access is restricted to classification, transport
framing, exact frame consumption, and raw untrusted views. Only core promotes
those views into authenticated, method-valid, stateful, policy-authorized, or
capability-bearing values. Core also orchestrates wire range/segment evidence
into crypto provider calls, keeping wire and crypto independent. Module/API and
dependency tests enforce this boundary. Typed capabilities and quiescence
evidence constrain reviewed conforming adapters; they are not cryptographic
proof against a malicious runtime that already possesses syscall authority.

## 5. Core Data Model

Core address and transport types use byte arrays and integers rather than
`std::net` types. Client paths include remote/local addresses, transport kind,
stable listener and local-endpoint identities, listener/configuration
generations, authenticated ingress provenance, platform interface/scope where
needed, connection/session generation, and worker ownership epoch. Reused
sockets, listeners, proxy trust, TLS/DTLS sessions, configurations, interfaces,
or workers therefore cannot inherit stale or cross-realm authority.

Every reusable object uses an index plus generation:

```rust
pub struct AllocationId {
    index: u32,
    generation: u32,
}
```

The same pattern applies to relay, permission, channel, timer, operation,
credential, buffer, and fast-path handles. Delayed completions and stale
timers become harmless generation mismatches.

Monotonic `Tick` and `AbsoluteTime` are distinct primitive-domain types. The
runtime injects both; the core never reads a clock. `AbsoluteTime` carries the
observation, explicit `Trusted`, `Uncertain`, or `Unavailable` status, source
identity, and source generation from the first public primitive API. Untrusted
wall time cannot mint new credential authority, while later clock-health,
rollback, forward-correction, source-replacement, and recovery transitions
never alter monotonic allocation lifetimes without a separate revocation event.

## 6. Wire Processing

### 6.1 Checked cursor

A small internal cursor owns all length and offset arithmetic. It uses checked
addition, bounds-checked slice methods, exact structural 4-byte padding rules,
and stable parse errors. Receivers validate that calculated padding is present
but ignore its octet values; encoders always write zero padding. No generic
parser or serialization framework is used.

### 6.2 Borrowed views

The top-level classifier yields a borrowed STUN or ChannelData view. The STUN
view retains the original encoded bytes and exact attribute offsets because
integrity verification changes the logical header length at a precise
boundary. Unknown and duplicate attributes remain visible to later semantic
validation. Unknown comprehension-optional attributes preserve their raw bytes;
unknown methods and negotiation bits remain bounded and inert until an extension
profile explicitly assigns semantics. ALTERNATE-SERVER, ALTERNATE-DOMAIN, 300
Try Alternate, and security-feature negotiation have explicit loop, trust,
realm, and downgrade policy.

The raw view can retain attributes after MESSAGE-INTEGRITY for diagnostics, but
the authenticated semantic view ignores them except for integrity/fingerprint
attributes explicitly permitted there by RFC 8489. Attribute iteration is
fused, always advances on success, terminates on failure, and feeds one bounded
inventory so later validation cannot repeatedly rescan attacker-controlled input.
That inventory uses fixed bitsets/counters for known attributes, selected exact
offsets for integrity/fingerprint and other revisited fields, and caller-bounded
storage only for unknown comprehension-required types. It does not retain one
descriptor per attribute. Inventory exhaustion is a resource/profile outcome,
not malformed syntax, and raw iteration remains byte-preserving.

### 6.3 Validation stages

Processing is separated into:

1. framing and memory safety;
2. basic STUN validity;
3. authentication requirements and integrity;
4. unknown comprehension-required attributes;
5. known-but-unexpected and duplicate attributes;
6. method-specific combinations;
7. allocation and transaction state;
8. destination, quota, and capacity policy.

This ordering is tested directly and prevents state or policy oracles from
leaking through unauthenticated error paths.

### 6.4 Encoder and stream framer

The transactional encoder exposes an explicit typestate sequence:
`EncodeDraft -> ValidatedPlan -> FinalizedEncodePlan -> committed output`.
Draft construction may still fail and validation resolves canonical ordering,
exact lengths, padding, capacity, borrowed segments, and typed finalizer slots.
CRC and HMAC finalizers then populate those slots without mutating caller
output; only `FinalizedEncodePlan` can write caller-visible bytes. Generic
structural typestates land before protocol-specific FINGERPRINT and integrity
finalizers, so the API does not claim immutability while tags are still being
computed.

Every finalizer slot is bound to one plan identity, exact expected output
length, algorithm/purpose, input range, and dependency node. It is filled
exactly once and cannot be copied, transferred, substituted, or reused by
another plan. The dependency graph requires all integrity fields in wire order
before FINGERPRINT, detects missing/duplicate/cyclic finalization, and admits
`FinalizedEncodePlan` only when every required node is complete.

Segments, dependency nodes, finalizer slots, prepared outputs, and scatter
entries use fixed arrays or caller-provided workspace with exact alignment and
capacity. Per-message vectors, boxes, captured closures, heap-created trait
objects, recursive nodes, and dynamically grown scatter lists are prohibited.
Workspace exhaustion is `PlanCapacity`, not malformed input, and leaves caller
output unchanged. Allocation/copy/edge/finalizer counters begin with the first
encoder implementation.

Sizing, prescribed HMAC/CRC range views, prepared fixed-size tags, and final
writing derive from the same validated segment plan. Provider finalization
completes before direct caller output changes, writing occurs once, and the
committed length is the final infallible publication. A failed transactional
encode leaves the caller's declared output bytes unchanged. Profiles unable to
seal final outputs use an explicit fixed caller staging region whose expected
copy is separately accounted; destructive in-place APIs are separately named
and typed.

The stream framer accepts arbitrary partial reads and coalesced frames, caps
retained bytes and frame counts, and applies ChannelData stream padding without
including it in the ChannelData length. An invalid/impossible/oversized prefix,
invalid stream padding, impossible declared length, or EOF with a partial frame
is terminal for the connection. The framer never scans forward for a plausible
cookie or ChannelData boundary after failure; arbitrary fragmentation and
malformed input retain linear work with no resynchronization attempt.

UDP ChannelData accepts either the exact declared datagram length or its legal
four-byte-aligned padded form. Every other trailing length is rejected. Received
padding values are ignored and generated padding is zero.

## 7. Authentication and Cryptography

The modern profile prefers SHA-256 password derivation and
MESSAGE-INTEGRITY-SHA256. Legacy MD5 derivation and HMAC-SHA-1 remain an
explicit interoperability profile, not the internal design center.

Authentication is one auditable state pipeline covering absent credentials,
401 challenges, realm and nonce validation, USERNAME/USERHASH, password
algorithm negotiation, credential lookup, integrity verification, stale nonce
438 responses, and response integrity selection.

Nonces are versioned, source-path-bound, realm-bound, time-limited,
authenticated values with a key identifier and rotation overlap. Raw keys,
credentials, nonces, tokens, usernames, and full endpoint identities never
enter ordinary logs or metrics.

These stateless nonces are context-bound and replay-window-limited, not single-
use or replay-detecting. A captured nonce can validate again inside the same
accepted path/realm/time/key context; short lifetime, authentication,
transaction idempotence, quotas, and allocation semantics contain that reuse.
“Replay detected” is reserved for mechanisms that retain replay state.

Credentials are returned as bounded derived-key records. Slow providers are
represented by pending operations and bounded caches; the core never performs
an external lookup while holding an incomplete mutation.

Packet-path hash, HMAC, and derivation providers are synchronous, deterministic,
bounded, nonblocking, allocation-qualified, and free of ambient entropy.
Opaque handles cannot conceal I/O under that interface. HSM, KMS, network, or
other external cryptographic work uses generation-tagged asynchronous
command/completion operations, so provider state and nondeterministic results
become explicit reducer inputs.

Provider key types are opaque and purpose-specific for message integrity,
nonces, transactions, reservations, mobility, tokens, and other domains; they
do not expose `AsRef<[u8]>`, ordinary `Debug`, `Clone`, or equality. Fixed
public validated tag-length types and fixed outputs prevent caller-selected
shape drift. A provider may expose a combined derivation-and-MAC suite so an
externally held key never needs export between provider objects. `Unsupported`,
`InvalidKey`, `Unavailable`, `StaleGeneration`, and `InternalFailure` remain
distinct internally but all fail closed without algorithm fallback or
unauthenticated success.

Concurrent or prepared key use is represented by one bounded non-cloneable key
lease bound to purpose, provider, core key reference, generation, consumer, and
expiry. A prepared synchronous operation borrows for its call or owns one
accounted lease. Revocation prevents new use; already-started work follows its
declared completion/cancellation/quarantine lifecycle. Leases never export key
bytes or backend handles, compare backend representation, extend themselves on
use, or hide unbounded reference-counted cache retention.

For valid public tag lengths, verification computes the complete required MAC
and compares every offered tag byte without secret-dependent early exit.
Structurally invalid public lengths may fail before secret work. Statistical
leakage tests are regression evidence for qualified provider boundaries, not a
mathematical or end-to-end constant-time claim.

Base-profile packet HMAC remains synchronous; asynchronous external services
normally provision/manage keys rather than retain packet input. Any separately
admitted asynchronous packet-crypto profile owns the exact immutable segment
sequence through a generation-tagged bounded message lease or copy with byte,
operation, timeout, cancellation, and shutdown ceilings.

Pawalyze never embeds a permanent TURN password in browser configuration.
Its authenticated issuer returns short-lived credentials bound to user,
tenant, realm, purpose, audience, expiry, and quota. OpenBao holds rotating
shared-secret generations with bounded overlap and emergency revocation.

## 8. Sans-I/O State Engine

Events include client frames, peer datagrams, ICMP results, relay open/close
completions, credential completions, ticks, disconnects, revocations, and
policy generation changes.

Commands include client/peer sends, relay open/close requests, credential
lookups, audit/metric events, and fast-path install/remove requests. A
caller-provided command sink allows one event to emit several bounded actions.
Borrowed packet data must be consumed before event handling returns or replaced
by an explicit runtime-owned buffer lease.

The core is a pure reducer: identical initial semantic state, immutable configuration,
ordered event/path identities and generations, supplied monotonic/absolute
times, entropy bytes, provider completions, storage seed/layout inputs, and
output/workspace capacities produce byte-identical wire/command output and the
same complete versioned, domain-separated `CanonicalStateWitness`. The witness
is an internal/test-only canonical structured stream or lockstep iterator using
fixed scratch space and contains every field capable of changing future reducer
behavior, including sensitive retained evidence and resource debt. Full stream
comparison is decisive; its digest is diagnostic only. Witnesses never format,
serialize, log, export, administer, persist, restart, or deserialize authority.
Provider secret bytes remain outside core when stable purpose-bound
`{domain, id, generation}` references are the semantic state.

`RedactedObservationSnapshot` is a separate bounded production diagnostic with
identities, credentials, nonces, packet/authentication evidence, and reusable
handles removed. It is never equality evidence. Equality also never compares
raw Rust memory, padding, pointers, or backend handle representation. Every
future-behavior state field has a mutation test proving it changes the complete
witness, while intentionally nonsemantic fields require reviewed exclusions.

Open-addressed hash seed, layout, probe/load limits, tombstone debt, and
saturation are explicit reducer resource inputs. Identical inputs replay exactly;
cross-layout runs compare safety, lookup soundness, atomicity, and authorization
invariants while permitting only typed bounded resource outcomes to differ.
No hidden platform hash state, reseed, full-table scan, pointer layout, `usize`
width, endianness, allocator placement, or runtime correlation ID may affect
semantic authority or operation identity.
It first performs one bounded preparation pass into caller-provided fixed
workspace. The resulting non-cloneable `PreparedTransition` contains immutable
planned state changes, commands, and exact `TransitionRequirements`; it binds
the event, state revision, configuration generation, and worker epoch.
Requirements describe only semantic command kinds/counts, bytes, retained
ownership, terminal/control obligations, and alignment. They contain no queue
topology, wakeup, atomics, executor tasks, provider lanes, or OS submissions.
Preparation performs parsing, authentication, policy scans, encoding planning,
and other attacker-controlled work at most once. Client-ingress preparation
requires irreversible conversion from the finite unclassified fixed-header
permit into the matching method/work-class permit defined before the public UDP
runtime; authoritative control events instead consume their reserved control lane.

`PreparedTransition` is single-consume, worker-local, and normally `!Send` and
`!Sync`. It cannot survive an await, callback return, receive-buffer reuse, or
the synchronous prepare/acquire/commit scope unless an explicit bounded,
generation-tagged lease owns every referenced input and output. Its identity
includes input-buffer, derived-key, output-plan, configuration, and worker
generations. Discard scrubs derived keys, integrity tags, nonces, and
credential-derived response material in the workspace. Stack/static footprint
and alignment have explicit ceilings, and no implicit copy of the workspace is
allowed. The no-escaping-borrow rule applies to this intermediate object.

The adapter acquires one exact single-use capacity reservation and supplies a
bounded command arena from those requirements. Reservation has bounded declared
work, limits outstanding reservations and bytes/slots in the adapter, and
cannot retry preparation, incrementally hoard capacity, or expose queue layout
to the reducer. Core observes only opaque reservation/arena identity, exact
sufficiency, and single-consume validity. A stale prepared transition or
insufficient capacity is discarded without mutation. Only droppable client
ingress may be retried as a new external event under a new ingress-work permit.
State, input, mutable workspace, command output, and retained regions are
disjoint unless an API explicitly permits read-only overlap. Reservations bind
the exact arena identity, checked base/length, alignment, capacity, and
generation. Safe borrows make aliasing unrepresentable; raw-memory adapters
validate overlap, arithmetic, lifetime, substitution, alignment, and generation
at their reviewed unsafe construction boundary before mutation.

Queue/listener/worker generations, topology, publication state, wakeups, and
correlation IDs stay in the adapter envelope. Failed commit, cancellation,
dropped reservation, shutdown, resize/restart, and worker replacement release
unused capacity and make stale reservations inert. Semantic operation IDs are
created only by core from an explicit engine/worker epoch and bounded
generational counter. Exhaustion or wrap fails closed; adapter correlation
metadata cannot affect reducer behavior.

Mutable core state is exclusively worker-owned. Commit writes commands into the
adapter-reserved caller arena without knowing its eventual queue. Every provider
call, bounds/capacity check, encoding step, and fallible arena write finishes
before semantic mutation. Once mutation begins, it and ready-arena return are
infallible and non-panicking; preflight/shadow records or a bounded undo journal
prove failure atomicity rather than assuming arbitrary in-place rollback. The
adapter then performs
its reserved infallible publication. Threaded consumers use release/acquire;
local and custom adapters use equivalent mechanics without atomics. State
inspection occurs through owner-generated immutable snapshots, never concurrent
direct reads. If execution stops after mutation begins but before publication,
the base design destroys the complete worker engine epoch and its authoritative
state together with the arena; invalidating only the unpublished arena is
forbidden and this is epoch loss, not rollback. Partial arena acceptance is
prohibited, while later OS execution remains explicitly non-atomic and
completion-driven.

Public engine entry follows `Idle -> InCall -> Idle | Poisoned`. Exactly one
outer no_std guard owns a public call; internal storage/crypto/provider work
cannot disarm it, while independently scheduled domains own separate guards.
Every ordinary `Result`, including expected failure, disarms only after failure
atomicity and ownership validate. Guard drop without validated return poisons
the epoch. Reentrant public entry observes only `InCall`, returns
`ReentrantCall`, and cannot inspect input/state, invoke providers, or mutate.
If an unwind-enabled host catches a panic, all later work returns
`EnginePoisoned`; only bounded quarantine, redacted evidence, destruction, and
supervised disjoint-epoch replacement remain. Poison never proves quiescence or
releases external ownership. Production aborts and never treats `catch_unwind`
as fault isolation; destructor panic during unwinding remains process-fatal.

Capacity reservation and publication are runtime-adapter responsibilities, not
part of the portable core data model. `gjallarbru-core` transitions, requirements,
state, events, commands, and capabilities contain no atomics, queue topology,
wakeups, tasks, or OS handles and do not require `Send` or `Sync`. A
single-thread adapter commits and consumes locally without atomics. Threaded
adapters select `target_has_atomic`-appropriate release/acquire machinery and
must remain differentially equivalent; targets without pointer-width atomics
compile and use the local adapter.

After ready publication, every batch is tracked until execution/reconciliation
or deterministic cancellation. The recovery matrix distinguishes: published
but unexecuted batches; partial execution; an OS resource opened before core
received completion; surviving versus lost queues; retained buffers/leases;
and stale batches/completions from the prior worker epoch. Runtime resources
are generation-fenced and inventoried on restart. Surviving accepted work is
replayed/reconciled only when its idempotency contract permits it; otherwise
core receives bounded cancellation/uncertain-result events and cleanup owns
every buffer, lease, socket, and operation exactly once.

That reconciliation authority exists only while the authoritative core state
survives a thread or worker-runtime restart. Whole-process loss destroys the
base profile's allocation and relay authority: a replacement process never
adopts old allocations, sockets, leases, or provider operations. Survivors are
fenced, quarantined, and closed; non-idempotent datagram delivery with unknown
execution status is never replayed; attempt charges remain consumed; and no
delivery success is inferred. A future persistent accepted-batch journal would
be runtime infrastructure behind a separately reviewed durable-authority
profile, not part of the base no_std engine.

Events are classified as droppable ingress or authoritative control events.
When a command creates authoritative external work, admission reserves a
separate control lane for its worst-case terminal completion, compensation,
cancellation, shutdown reconciliation, and any ownership release. Expiry and
revocation progress have their own finite reserve. Packet delivery, metrics,
and new ingress cannot consume these slots. The reserve is bounded globally
and per worker/operation, and its use/refill is deterministic, so a full packet
queue cannot block the completion needed to release resources.

The reservation covers the complete transitive bounded control-effect closure:
completion-generated commands, compensation of compensation, completion versus
cancellation races, ownership release, security-audit consequences, and any
required terminal error response. The effect graph is acyclic with an explicit
maximum depth and node/byte count. Each operation owns one bounded terminal
mailbox that coalesces duplicate/stale completion observations without
allocating new control slots indefinitely.

The terminal mailbox follows an explicit state machine:
`Pending -> DeadlineExceeded -> CancelRequested -> Succeeded | Failed |
Cancelled | Uncertain`, with direct transitions to valid terminal states where
applicable. `DeadlineExceeded` is a nonterminal local observation, not evidence
that external work failed or stopped. It initiates the operation-specific
cancellation/reconciliation path and still permits a generation-valid late
success where that operation's policy allows it.
A cancellation request records intent and blocks forbidden new work but never
proves that an OS operation was cancelled. Operation-specific contracts decide
whether a generation-valid success observed after cancellation request wins.
Identical terminal observations coalesce; conflicting valid observations enter
the deterministic `Uncertain` reconciliation path. Terminal ownership,
attempt/completion accounting, cleanup, audit, and late-event behavior are
defined for every transition.

Each runtime execution domain has a monotonic `FenceId`/authority sequence.
Every delivery command carries the sequence current when it was authorized.
Revocation advances the sequence and requires bounded acknowledgement from
every applicable queue, submission ring, provider lane, and kernel fast path
before an identifier, endpoint, permission/allocation slot, connection, or
buffer generation can be reused. FIFO ordering alone is insufficient. Missing
or uncertain acknowledgement destroys the old execution domain or advances to
a disjoint generation whose identifiers cannot alias the unacknowledged one.
The portable core represents fence commands, acknowledgements, and generations
as ordinary no-atomic values; runtime adapters implement the synchronization.

Fence state is fixed-capacity. Each registered execution lane owns one pending
high-water mark; repeated revocations coalesce monotonically into the newest
required `FenceId` rather than allocating another control operation. An
acknowledgement of `F` means every command through `F` is handed off and tracked,
rejected, or terminally reconciled, never merely dequeued. Lane membership has
a generation: a lane added during a pending fence begins beyond the captured
watermark and cannot receive older commands; removal must acknowledge, drain,
or destroy its domain. Ordering `FenceId`s are distinct from semantic object
generations, so a narrowly scoped permission revocation does not invalidate
unrelated commands unless the configured execution domain deliberately uses a
coarser documented blast radius.

Fence acknowledgement is only an ordering fact: no command at or below the
acknowledged watermark remains capable of a new handoff in that lane. An
already-handed-off command may still be externally in flight. Its buffer,
descriptor, lease, provider storage, operation slot, and other physically
reachable ownership remain pinned until a generation-valid terminal result or
deterministic reconciliation proves release. For domain destruction, an adapter
submits a structured `QuiescenceReport` bound to a single-use core challenge,
domain/adapter/worker/provider generations, shutdown attempt, fences, and the
exact resource manifest. Core validates it against live state and alone creates
and consumes private `ValidatedQuiescence`. Types establish report shape,
freshness, inventory completeness, and exact-once acceptance; truthful
observation that every kernel operation, registered buffer, DMA/UMEM reference,
provider thread, and provider-owned buffer stopped remains a reviewed conforming-
adapter trust obligation. A closed descriptor, dropped handle, timeout, Boolean,
or free-form snapshot is insufficient. An adapter unable to report in-process
quiescence retains storage until confirmed process death or uses supervised
process isolation. Semantic identifiers may
advance to a disjoint generation after the fence, but their backing storage
cannot be reused or aliased while the old external operation could still access it.

Unresolved recovery is also bounded. Each operation type declares maximum
cancellation attempts, reconciliation rounds, unresolved age, and fixed
global/worker/provider counts. Exhaustion transitions the mailbox to
`Uncertain`, quarantines or destroys the affected provider/execution domain,
and keeps externally reachable storage non-aliasing until inventory or a core-
validated quiescence report establishes it unreachable. Logical admission capacity may be
replaced only from a separate bounded reserve/disjoint generation; another
unresolved operation is never silently evicted. Recovery from saturation is
explicit and cannot depend on a provider eventually responding.

Owner-generated `RedactedObservationSnapshot`s are fixed-size, redacted,
versioned observations and are distinct from complete internal state witnesses.
They contain no keys, credentials, packet bodies, raw tenant identities, or
capability-bearing handles; are bound to worker epoch and configuration
generation; and cannot authorize, validate a completion, or drive recovery.
Publication frequency, retained generations, reader leases, and reclamation
work are bounded. Slow readers receive an explicit stale/overrun result after
reload, restart, ownership replacement, or retention expiry rather than
pinning unbounded historical state.

Runtime effects use a composite envelope rather than mutually exclusive
classes. Orthogonal properties describe semantic authority, retained-resource
ownership, delivery guarantee, and durability/audit policy. A best-effort UDP
send can therefore own a buffer, consume quota, and require bounded audit
accounting without inventing a semantic delivery completion. Delivery failure,
cancellation, and shutdown release every retained resource exactly once.

Chargeable work has four distinct accounting modes. Occupancy reservations are
released exactly once when their slot, buffer, or lease ends. Attempt charges
are consumed at accepted work admission and are never refunded because delivery
later fails. Completion usage is recorded only from a valid generation-bound
completion. A retry consumes a new attempt charge unless a bounded idempotency
budget explicitly binds it to the original operation. No failure path can
refund attacker-driven work, double-charge completion, or bypass quota through
retry classification.

Partial execution after full-batch acceptance and compensation are
deterministic ordinary events. State never assumes an authoritative external
effect succeeded before its matching completion.

Capability-shaped commands constrain what a conforming adapter can execute and
are differentially verified against the safe reference runtime. They do not
claim to prevent a malicious runtime from performing unrelated operating-system
operations outside the command contract.

Entropy is explicit asynchronous authority, not a hidden synchronous callback.
The core emits purpose/length-bound entropy requests and consumes
generation-tagged completion events. Equal, duplicate, decreasing, delayed, and
wrapping monotonic observations have specified ordering behavior; wall-clock
rollback can affect credential validity only through its separate absolute-time
policy and never extends monotonic allocation lifetimes.

Required invariants include:

- one live owner per relay address;
- one allocation per applicable client path;
- no peer-bound packet without a live permission;
- no ChannelData without a live channel and permission;
- no relay state after authentication failure;
- no duplicate side effects on transaction retransmission;
- no reservation-token reuse;
- no stale timer/completion affecting a reused slot;
- no fast path broader or longer-lived than core authority;
- live counters never exceeding configured capacity.

## 9. Storage, Timers, and Transactions

The core accepts storage traits with two first-party implementations:

- fixed arrays for tests, appliances, embedded use, and future Aesynx;
- startup-preallocated slabs for production runtimes.

Bounded open-addressed indexes use per-process keyed hashing, a load ceiling,
maximum probe count, tombstone/stale-debt ceiling, and bounded cleanup work.
Iteration/bucket/insertion order never controls protocol output, operation
identity, authorization, or eviction; required enumeration has a stable bounded
order. Width-independent hashing/serialization and explicit generation/Tick
wrap horizons keep results equivalent across qualified targets. Direct relay-
port indexes avoid attacker-keyed hash lookups on the hottest peer path.

One hierarchical timing wheel per worker manages allocations, permissions,
channels, reuse blocks, transactions, reservations, nonces, credentials,
pending operations, TCP connections, mobility overlap, and fast-path rules.
Stale timer entries are ignored by generation rather than acquiring authority,
but live entries and stale-entry debt both have ceilings. Rescheduling and
compaction are bounded, each transition has an expiration-work budget, and an
overdue cursor processes backlog fairly. Large time jumps expire authority at
its original deadline even when physical cleanup is delayed.

The transaction cache records a per-process keyed cryptographic-strength request
identity and pending/completed outcome. An exact retransmission repeats no side
effect and reuses the prior response; the same transaction key with different
bytes is treated as suspicious. Collision resolution retains enough original
byte/semantic evidence to avoid trusting the digest alone, while request and
cached-response bytes have ceilings independent of record count. Transaction
tables inherit fixed load/probe/tombstone bounds and cannot order responses or
semantic choices by bucket layout. Constant-time comparison applies to secret-
bearing keyed evidence, not ordinary public transaction IDs.

Cache timing follows an explicit observer and secrecy threat model rather than
claiming identical full-path runtime. Lookup and secret-bearing identity
comparison stay bounded and constant-time where secrets are involved; hit,
miss, collision, invalidation, and error latency stay within measured profile
envelopes. Response content, amplification, accounting, and audit behavior do
not create a new membership oracle beyond protocol semantics. Gjallarbru never
performs dummy HMAC, credential lookup, policy, or mutation work merely to
equalize a hit. A profile that classifies membership as sensitive uses a fixed,
bounded response-release schedule with explicit overload behavior.

Ordinary configuration reload pins a live transaction to its original decision
generation until expiry. Security revocation is a separate invalidation event;
each invalidation class defines whether retransmission replays, returns an
error, discards, tears down state, or terminates the path. A cached success never
claims an allocation remains live after explicit revocation.

## 10. TURN Processing

Allocate uses a two-phase commit:

1. validate, authenticate, authorize, and reserve bounded core state;
2. emit an exact relay-open request;
3. validate the generation of the runtime completion;
4. atomically commit allocation/index/timer state and response, or release all
   reservations on failure.

Permissions are keyed by peer IP, while channels map channel numbers one-to-one
with peer transport addresses inside an allocation. Send indications silently
discard unauthorized data. Peer datagrams require a permission before Data or
ChannelData output. No data operation refreshes allocation, permission, or
channel lifetime unless the RFC explicitly says so.

Before generation-tagged zero-copy leases are admitted, Send and Data paths copy
payloads into bounded runtime-owned output storage. No borrowed receive payload
escapes a core transition. Later scatter/gather leases replace eligible copies
without changing authorization or completion semantics.

The relay-port allocator maintains state per relay IP, family, transport, and
shard. It uses an explicitly supplied independent worker seed with a
deterministic keyed permutation/PRF, or explicit per-search entropy completion.
Candidate mapping has no modulo bias, never repeats within a search, handles
fork/snapshot/restart seed reuse, and exhausts deterministically at its budget.
It supports atomic even-port reservation, consumes authenticated reservation
tokens once, and releases all state on failed opens.

## 11. Runtime and Platforms

The safe portable backend is the behavior reference on every supported OS. It
uses bounded buffers and no task or timer per allocation.

Every scalar UDP receive first normalizes platform completeness metadata.
`MSG_TRUNC`, `WSAEMSGSIZE`, equivalent indicators, or uncertainty that a buffer
contains the complete datagram silently discard that indivisible datagram before
classification, parsing, authentication, lookup, state, or response. A retained
prefix is never an input frame even when it is a complete valid authenticated
STUN message. Batched and accelerated receives refine this scalar rule.

All receive paths promote `RawIngress -> ValidatedProvenance ->
CompleteIngressEnvelope`. A common bounded header is paired with one sealed
variant: datagram, stream, secure datagram, or trusted termination. Internal
AF_XDP, simulation, and Aesynx sources validate into the applicable semantic
variant. A per-variant presence matrix distinguishes present, legitimately
absent, and unsupported; malformed, conflicting, truncated, untrusted, and
required-but-missing values cannot become `None` or defaults. Only complete
ingress can reach classification. Streams inherit identity from their generation-
bound accepted connection instead of fabricating per-frame ancillary metadata.
`MSG_CTRUNC` and malformed/conflicting packet information fail before promotion.
Wildcard/multihomed responses bind the authorized local address/interface to a
bound socket or validated per-send packet information; ambient OS source
selection is forbidden.

Linux adds worker-local `SO_REUSEPORT` steering, batched receive/send,
scatter-gather buffers, then `io_uring` only after measurement. Optional eBPF
and AF_XDP can filter or accelerate already-authorized plaintext UDP paths but
cannot authenticate, create state, refresh lifetimes, or independently decide
policy.

The `io_uring` `user_data` is one opaque nonzero 64-bit operation token—never a
pointer or lossy packed identifier. A bounded token table resolves it to checked
slab index/generation, domain/ring generation, kind, ownership, and completion
mode. Reserved/unknown/stale tokens fail closed; tokens never repeat in a live
domain, and exhaustion requires drain plus validated quiescence before a
disjoint domain resets the space. The adapter models multishot `F_MORE`
and terminal CQEs, cancellation with late completions, provided-buffer depletion
and exactly-once return, CQ overflow/ring disable, failed unregister/fixed-file
updates, and partial linked submission. `SEND_ZC` is excluded unless its separate
notification CQE retains buffer ownership correctly. Each unavailable feature
has a tested scalar fallback.

The first eBPF/AF_XDP profile prefers tuple steering/filtering and does not
duplicate the semantic STUN parser. VLAN/QinQ, IP options/fragments, IPv6
extension headers/fragments, checksum/offload ambiguity, and GRO metadata have
explicit punt/drop eligibility. Related maps are filled under one inactive
generation and exposed by a single atomic epoch switch, preferably map-in-map.
Each packet captures the active epoch once and uses it for every related lookup;
active entries are immutable. A fence first prevents new old-epoch entry, then
a generation-bound kernel/RCU grace-completion observation proves pre-fence
readers for that map/program class exited. Elapsed time never authorizes map
reclamation; missing/stale/timeout evidence quarantines old maps and disables
acceleration. UMEM/DMA/XSK ownership still requires its separate terminal or
core-validated quiescence evidence. Epochs cannot wrap or be reused while
reachable. UMEM frames carry a generation and one XSK queue owner with fixed
headroom/alignment and exactly-once fill/completion return.

Batched receives preserve the complete `CompleteIngressEnvelope` for every
scalar core transition without maintaining a second field list. Partial sends
report unsent packets truthfully. Fast-path rules are
removed or invalidated before authority reuse, never expire later than core
authority, and drop or return to the slow path on map loss or reconciliation
uncertainty.

Send batches track each packet independently:
`Queued -> Validated -> HandedOff` or `Validated -> Unsent`. Only the prefix
accepted by the OS/provider consumes its single-use delivery capability and
becomes in flight. Unsent entries retain exclusive buffer/capability ownership,
do not receive a completion, and must revalidate deadline, queue age,
adapter-local buffer/command/batch identity, exact endpoint, and acknowledged
fence before retry. Semantic freshness belongs to the core-issued capability.
Any runtime semantic-generation mirror is versioned and fence-driven, may reject
but never authorize, and fails closed when stale or uncertain; observation
snapshots are never send authority.
For a stream/vector call that accepts only part of one entry, that entry's
capability is consumed once and its remaining tail stays owned by the same
bounded in-flight operation; it is never reclassified as a fresh unsent packet.
The partially written frame stays at the head of its connection write ledger;
later frames cannot overtake or interleave with its tail. The tail is neither
reauthorized nor charged as a new semantic delivery. If authority expires,
revocation/cancellation arrives, or the connection enters shutdown, the tail
may finish only within its declared already-in-flight byte/time window;
otherwise the connection closes. Dropping a tail while retaining the stream is
forbidden because it would corrupt framing. TLS/provider adapters define an
exact prefix-acceptance boundary into provider-owned output independently from
eventual encrypted-record or kernel-write completion.
Retry attempt charging follows the declared idempotency policy and never
recreates a consumed capability. Expiry, revocation, disconnect, or buffer
reuse between a partial result and retry makes the unsent entry inert.

Optional UDP GRO is split into original datagrams before scalar admission;
each segment retains complete path/ancillary/generation metadata and pays its
own parse, crypto, policy, quota, and command charges. Optional GSO combines
only independently authorized compatible segment plans and requires truthful
per-segment completion semantics; ambiguous whole-superpacket providers fall
back to scalar sends. Coalescing/segmentation changes amortization only.

The first cross-worker queues, configuration publication, cancellation, and
shutdown ordering receive focused Loom models before batching or Linux
acceleration is admitted. Comprehensive concurrency and sanitizer closure still
occurs at the final assurance milestones.

Fast-path packet and byte authority is a finite generation-bound lease issued by
core. Kernel code may decrement but never refill it. Consumption must reconcile
before renewal; lost or uncertain accounting prevents renewal, and unused budget
is invalidated on expiry, revocation, teardown, restart, or generation reuse.

TLS and DTLS early application data is disabled for STUN/TURN. Resumption begins
application processing only after handshake confirmation; any future method-level
exception requires a separate replay-safety contract and release.

Secure-transport providers are memory-qualified before production activation.
Each adapter declares lifecycle versus established-session allocation behavior,
maximum provider-owned plaintext/ciphertext/pending-record/session bytes, and
deterministic backpressure on exhaustion. Bounded connection/handshake
allocation is permitted by profile; established record/frame hot paths must be
instrumented and allocation-free for hardened/accelerated profiles, or the
provider is explicitly excluded from those profiles. Accepted plaintext cannot
trigger hidden growable buffering. Failure, disconnect, timeout, and provider
replacement release and best-effort zeroize provider-owned plaintext and key-
adjacent storage within documented limits.

Secure-transport control traffic is charged before common plaintext ingress.
TLS 1.2 renegotiation and TLS 1.3 post-handshake client authentication are
disabled. KeyUpdate and reciprocal updates, ticket/control-record generation,
and DTLS acknowledgements, retransmissions, key updates, connection-ID work,
and migration attempts consume fixed per-connection and global operation/byte/
rate budgets. Providers expose normalized pre-work events/counters or enforce
reviewed equivalent internal limits; an opaque provider that cannot demonstrate
the bound is unavailable for that profile. Exhaustion suppresses, rejects, or
closes according to the transport contract without reaching STUN processing,
refreshing authority, or generating unbounded control output.

Allocation and copy claims are profile-specific. UDP/STUN steady state after
worker startup, UDP/TURN after pool initialization, and TCP after connection
admission require zero allocator calls. TLS/DTLS lifecycle allocation may be
bounded and measured; established hardened provider paths are allocation-free
after warm-up or excluded. Every profile declares allocation, copy, retained-
byte, task/timer, descriptor, and provider ownership counters plus deterministic
exhaustion. Deliberate security/ownership/platform copies remain classified and
measured; the claim is zero unnecessary copies, never universal zero-copy.

Every client transport converges on the same normalized ingress-work contract.
UDP datagrams, complete TCP/TLS frames, DTLS plaintext datagrams after
handshake/replay admission, trusted-termination frames, and shared-port demux
results each acquire one just-in-time permit before semantic parsing. Stream
framing bytes and retained partial frames have bounded occupancy/work charges;
coalesced frames pay semantic charges separately. TLS/DTLS handshake work uses
its dedicated handshake budgets first, then each admitted plaintext STUN/TURN
frame pays the common parse, HMAC, lookup, preparation, and response charges.
Demultiplexing and batching cannot create a transport-specific accounting bypass.

Windows, BSD, and macOS use platform event and batching facilities behind the
same runtime command contract. Android and iOS embed the portable runtime
without assuming service-manager, filesystem, or privileged-socket behavior.
Aesynx readiness means fixed storage, explicit time/random/network traits, no
OS types in core, and no implicit allocator or thread dependency.

Bind/local destination and advertised/public relay addresses are different
types. One-to-one NAT, multi-homing, multiple public relay pools, port ownership,
PMTU, ICMPv6 Packet Too Big, IPv6-only, NAT64, and 464XLAT behavior are validated
instead of inferred from operating-system defaults.

## 12. Security Policy

Before the first public UDP listener becomes functional, a cheap admission
transition uses only listener identity, datagram length, trusted receive
metadata, and injected monotonic time to acquire one linear
`UnclassifiedIngressPermit`. It carries finite global/listener/worker
allowances only for packet/frame admission and bounded fixed-header
classification. Irreversible classification converts it into one finite
configured method/work-class permit carrying the applicable parse, HMAC,
credential-lookup, error-response, send, and preparation allowances.
Preparation consumes but cannot refill or transfer those allowances; failure
to convert occurs before attribute scanning or authentication work.

Ingress authority has two irreversible levels. An `UnclassifiedIngressPermit`
pays only for packet/frame admission and bounded fixed-header classification.
After the fixed STUN/ChannelData header identifies a finite configured method/
work class, atomic conversion consumes that classification authority and either
acquires a class permit reserving the applicable HMAC, lookup, preparation, and
response capacity or stops before attribute scanning, HMAC, or lookup.
Attacker-declared methods cannot create new classes, repeat conversion, probe
capacity without charge, or refund classification work. Fixed-header
classification always selects the ordinary finite method class; it cannot know
that a request is an exact cached retransmission.

Within the classified permit, starting HMAC, lookup, response construction/send,
or preparation converts only that stage's reservation into a non-refundable
attempt charge. Dropping the permit releases unused reservations; started work
is never refunded. Cached retransmissions still pay packet, classification,
parse, and send charges but do not recreate semantic side effects. Capacity
recovers only through
deterministic saturating monotonic token-bucket refill with explicit burst and
rate ceilings. This includes spoofed-source and amplification-safe policy, so
Binding never ships as an unbudgeted internet-facing CPU or response path.

Permits are acquired just in time immediately before classification/preparation
and are never retained while a packet waits in an input queue. Outstanding
permit count, reserved stage capacity, and reservation lifetime are bounded per
listener and worker. Receive batching does not grant batch-wide reservation:
each packet is admitted independently, and unused stage reservations are
released before the next packet where practical. Deterministic fairness
prevents one listener or classified work class from starving another; cheap
Binding classification cannot reserve authenticated TURN HMAC/lookup capacity,
and expensive traffic cannot evade its own charges.

The ordinary method class includes one bounded charged transaction-cache lookup.
Only after that lookup may processing enter a `CachedResponse` substate. A hit
may release still-unused HMAC, credential, and semantic-mutation reservations,
but never refunds admission, fixed-header classification, request parsing,
cache lookup, or response/send attempts. A miss continues through the ordinary
method path. Deliberately colliding transaction IDs, near matches, and repeated
misses consume the same bounded lookup/classification authority and cannot form
a cheap cache-existence or capacity oracle.

Before Allocate, CreatePermission, Send, ChannelBind, or ChannelData can become
functional, every received destination becomes one canonical and effective
destination identity. IPv4-mapped IPv6 normalizes to IPv4; configured NAT64
prefixes are de-embedded and checked as both IPv6 and effective IPv4;
unspecified, multicast, broadcast, and inappropriate link-local/scope forms are
rejected; IPv6 equality includes interface/scope where required; and local
listener/control comparisons occur after bind/public-address translation.

The canonical result includes translation-profile and public-address-map
generations. NAT64 prefixes accept only RFC 6052-supported lengths, overlapping
or ambiguous matches fail closed, and at most one configured translation step
is applied. Permission, channel, transaction, and cached policy decisions
either pin the exact mapping generation for their lifetime or follow an
explicit invalidation/teardown rule when mappings change; they can never be
silently reinterpreted under a replacement mapping.

Successful destination/policy evaluation produces a sealed typed capability,
not a raw address for later reconstruction. `AuthorizedPeer` binds received and
effective peer addresses, address family, transport, interface/scope,
translation/public-map/policy generations, allocation and permission identity,
expiry, direction, and the exact runtime endpoint. Relay-open and fast-path
authority use corresponding typed endpoint capabilities. Commands accept these
capabilities rather than raw policy-sensitive addresses; the runtime executes
the included endpoint exactly or rejects the command, and cannot reinterpret
or substitute an address after authorization.

Delivery capabilities also carry a maximum execution tick no later than their
allocation/permission expiry, maximum queue age, one command/batch identity,
and the exact packet/byte attempt charge. They are single-use for delivery.
Before OS handoff, runtime verifies the deadline and every bound generation.
Revocation publishes a control-lane fence that invalidates older queued
capabilities before an identifier, endpoint, permission, allocation slot, or
buffer can be reused. Commands already handed to the OS have explicit bounded
in-flight semantics: recall is never assumed, their attempt charge stays
consumed, and late completion enters the terminal-mailbox contract rather than
silently extending authority.

Client-bound delivery is symmetric. `AuthorizedClientPath` binds the complete
`ClientPath` identity plus listener, socket/connection/session, worker,
configuration, proxy, TLS/DTLS, interface, realm, allocation/transaction,
command, batch, buffer, charge, and authority-sequence generations. It carries
maximum queue age/execution tick and is single-use at final handoff. Binding and
error responses, authenticated successes, Data indications, peer-to-client
ChannelData, and later RFC 6062 indications cannot be sent from a raw address or
connection handle. Disconnect, revocation, path replacement, or fence advance
invalidates queued client delivery before reuse. Incoming peer sources are
canonicalized with the same address/mapping-generation rules used for outbound
peers before permission or channel lookup.

Peer-to-client relay media uses live authority at final client handoff, not a
permission snapshot. Its client-delivery capability additionally binds the
canonical received/effective peer, translation/public-map generations,
permission identity/generation/expiry, and, for ChannelData, channel identity/
generation/expiry. Authorization-revocation generation is distinct from the
timer/lifetime revision used to reject stale expiry work. An ordinary same-
identity refresh can advance only the lifetime revision and does not rotate the
revocation generation, but an existing capability keeps its original expiry
and gains no extended lifetime. Revocation, rebinding, mapping/policy change,
or allocation teardown rotates authority and makes queued media inert. Stale
media drops by default. A runtime never inspects snapshots or reconstructs
authority; an optional single bounded reauthorization returns the exact owned
packet/lease to core with its original command, buffer, charge, enqueue time,
and queue-age deadline, and only core may issue one replacement capability.
Once bytes are handed off, reauthorization is forbidden and only the declared
bounded in-flight rules apply.

A non-optional minimum relay safety profile applies to that canonical identity
and denies metadata services, loopback, listeners, administration endpoints,
relay pools, and relay loops. It enforces fixed global/worker/allocation/
relay-port/permission/channel/buffer ceilings with deterministic exhaustion.
No placeholder or allow-all policy implementation can satisfy relay command
constructors, and alternate encodings cannot bypass a protected destination.

Later resource accounting is hierarchical: global, listener, relay IP, worker,
source address/prefix, realm, tenant, identity, allocation, and peer.
Authentication attempts, allocations, relay ports, permissions, channels, TCP
connections, credential lookups, transactions, packets, bytes, handshakes,
buffers, errors, audits, and admin calls all have limits.
Later hierarchical rate limiting extends the exact ingress token-bucket
primitive: the same monotonic refill, saturation, reserve-to-attempt
conversion, non-refundable work, and wrap behavior applies at every added scope.

Configurable public-server destination policy extends the mandatory baseline
with reviewed public, enterprise, test, or custom profiles. Private unicast is
therefore neither universally rejected nor accidentally enabled, and later
configuration can narrow but never remove the protected infrastructure and
relay-loop baseline.

The server starts with least privilege, separates public data and private
administration paths, drops unnecessary capabilities, restricts syscalls and
filesystem access where supported, disables secret-bearing core dumps, and
uses immutable configuration generations.

Listener, destination address, authenticated SNI, and configured default select
the realm before untrusted REALM input can acquire authority. Credential, nonce,
REST, mobility, reservation, certificate, policy, allocation, telemetry, usage,
and lifecycle domains are isolated per tenant and realm.

## 13. Production Service Model

Allocations, relay sockets, permissions, channels, transactions, and timers are
node-local. Node loss ends those allocations; Gjallarbru does not claim seamless
live allocation transfer. DNS/L4 routing sends new work to healthy nodes while
relay-IP and port-pool leases prevent dual ownership. Pawalyze performs an ICE
restart against another healthy node within a measured recovery SLO.

Nodes communicate over a separate private mTLS listener using a first-party,
versioned, bounded protocol. It carries authenticated membership observations,
health, capacity, drain state, configuration digests, lease generations, and
key-generation identifiers. It never carries relay payload, live allocation
state, browser credentials, or private key bytes, and it cannot authorize a
client operation. Static bootstrap and authenticated administrator approval are
the initial trust model; there is no public auto-join or trust-on-first-use.

Rolling upgrades support only tested adjacent-version pairs. Capability,
configuration, key, certificate, nonce, REST, reservation, and mobility
generations use staged activation, bounded overlap, drain, fencing, and rollback.
Region loss, split brain, stale nodes, and failback have explicit tests and
runbooks.

Fluxheim compatibility is capability-based. Its raw TCP stream proxy may balance
TURN/TCP and pass TURN/TLS through on port 443 with upstream PROXY v2 accepted
only from trusted Fluxheim peers. Gjallarbru UDP listeners and relay ranges are
reached directly because Fluxheim's current UDP beta is DNS/syslog-oriented, not
a generic production TURN proxy. Full UDP-through-Fluxheim becomes supported
only after a pinned Fluxheim release proves source-preserving five-tuple affinity,
relay-range behavior, overload safety, and cross-project interoperability.

Rootless deployment is a qualified profile rather than a universal one-command
claim. Supported Docker/RootlessKit/Podman/pasta modes must preserve the real
source five-tuple, publish the complete UDP/TCP relay range, validate bind versus
advertised addresses, and meet a native-runtime throughput floor. Port 443 uses
only documented host configuration, source-preserving forwarding, high-port, or
authenticated trusted-termination choices. Unsafe topology is rejected at
startup. The Wolfi image remains minimal, non-root, read-only, capability-free,
signed, and multi-architecture. A separately signed Debian stable-slim image
uses the same binary and qualified networking, remains non-root by default, and
retains a documented package/customization path for operators who prefer a more
familiar and controllable base. Image differences never change TURN behavior.

Capacity planning covers relay ports, packet rate, bandwidth, upstream link,
egress cost, regional headroom, SLOs, and autoscaling. Bounded application state
does not replace upstream DDoS scrubbing. Client and peer metadata has explicit
retention, residency, deletion, redaction, and durable usage-accounting policy.

Pawalyze one-to-one calls are the application integration target. TURN provides
connectivity relay; it does not replace signaling or WebRTC encryption. TURN is
not an SFU, and future group calls require a separate media architecture review.

## 14. RFC Evidence

The repository keeps untouched RFC Editor text under `rfc/`, locked by
SHA-256. A machine-readable requirement ledger will map each normative rule to
RFC/section, level, profile, component, symbol, test, status, and security
notes. Verified errata are applied; every other relevant erratum gets an
explicit decision.

The base RFC 8489/8656 ledger is followed before protocol implementation by
complete semantic ledgers for every locked advertised core, deployment,
extension, and transport RFC. RFC 5769 remains vector provenance rather than a
separate conformance profile, while RFC 2119/8174 define keyword interpretation.
Downloaded text alone grants no implementation status. Each extension remains
planned until semantic children resolve real symbols and CI observes their
positive/negative tests in the applicable profile.

IANA registries are updated only by a manually invoked tool. Normal builds are
offline and consume reviewed, dated snapshots. Numeric protocol assignments
are generated from that snapshot rather than scattered through source. Current
standardized, reserved, unassigned, and vendor-specific values are preserved;
unknown values remain byte-visible but inert until the extension-admission gate
assigns specification, threat model, key domain, requirements, and authority.

Scheduled post-1.0 controls review RFCs, errata, IANA, browsers, TLS/DTLS,
providers, dependencies, Rust, and platform behavior. New extensions require a
status, security, resource, portability, downgrade, conformance, interop, and
audit decision. Unsupported drafts remain outside production profiles.

## 15. Verification Strategy

Every release includes positive, negative, malformed, boundary, capacity, and
regression tests. Required layers are:

- unit tests for every decoder, encoder, state transition, and policy branch;
- RFC 5769 and project-owned vectors;
- encode/decode and production/reference-model properties;
- separate fuzz targets for cursors, attributes, frames, stream chunks,
  integrity ranges, nonces, transactions, timers, and event sequences;
- Kani for cursor/slab/state invariants where tractable;
- a small declarative lifecycle model for allocation/open/cancel/timeout/
  completion/fence/quarantine/quiescence, with traces replayed against Rust;
- Miri for ownership-sensitive runtime helpers;
- Loom for bounded concurrency primitives;
- sanitizers for syscall and buffer code;
- differential tests between safe and accelerated runtime paths;
- black-box interoperability with browsers, native ICE clients, and coturn;
- IPv4-only, IPv6-only, dual-stack, loss, duplication, reordering, NAT,
  overload, slow-client, restart, drain, and rollback scenarios.
- Chromium, Firefox, and Safari Pawalyze calls across UDP, TCP, TLS/443,
  NAT64, symmetric NAT, UDP-blocked, forced-relay, network-change, node-loss,
  and region-loss scenarios;
- native/container source-identity, relay-range, throughput, HA, mixed-version,
  privacy-retention, capacity/cost, and DDoS drills.

No release closes with an unexplained normative requirement, unresolved
security finding, unbounded resource, missing failure test, or source file over
the modularity limit.

## 16. Definition of 1.0.0

`1.0.0` requires all planned profiles to have published scope and evidence;
wire/core/crypto remain `no_std`; each packet/transport profile meets its
declared post-warm-up allocation, copy, and retention contract; all supported
transports and address-family combinations
interoperate; every external resource is bounded; acceleration is optional;
platform behavior is tested; tenant boundaries and Pawalyze ephemeral credentials
are verified; secure multi-node communication, node-local HA, ICE-restart recovery,
rolling upgrades, regional failover, the Fluxheim hybrid profile, rootless network
qualifications, capacity/cost, DDoS, and privacy controls are complete; deployment
and incident procedures are complete;
reproducible artifacts, checksums, SBOMs, provenance, and signatures are
published; signed multi-architecture Wolfi and Debian containers run the complete
server as a fixed non-root user under qualified rootless Docker and Podman
topologies, with a read-only Wolfi default and documented Debian customization;
public APIs and configuration migrations
have compatibility gates; standards and first-party protocol provenance controls
are operational; and a reviewed candidate plus any documented later CodeQL
remediation has passed independent security review with all findings resolved.
