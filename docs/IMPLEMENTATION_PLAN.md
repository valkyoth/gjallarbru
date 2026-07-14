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
- Destination policy, quotas, rate limits, relay-loop prevention, and bounded
  operational telemetry.
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

## 5. Core Data Model

Core address and transport types use byte arrays and integers rather than
`std::net` types. Client paths include remote/local addresses, transport kind,
and a connection generation so reused TCP/TLS endpoints cannot inherit stale
authority.

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

Monotonic `Tick` and absolute credential time are distinct types. The runtime
injects both; the core never reads a clock.

## 6. Wire Processing

### 6.1 Checked cursor

A small internal cursor owns all length and offset arithmetic. It uses checked
addition, bounds-checked slice methods, exact 4-byte padding rules, and stable
parse errors. No generic parser or serialization framework is used.

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

The encoder writes once into caller storage, reserves integrity fields,
computes over the prescribed adjusted length, writes FINGERPRINT last, and
returns a length without partially committing a failed message.

The stream framer accepts arbitrary partial reads and coalesced frames, caps
retained bytes and frame counts, and applies ChannelData stream padding without
including it in the ChannelData length.

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

Credentials are returned as bounded derived-key records. Slow providers are
represented by pending operations and bounded caches; the core never performs
an external lookup while holding an incomplete mutation.

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
and a maximum probe count. Direct relay-port indexes avoid attacker-keyed hash
lookups on the hottest peer path.

One hierarchical timing wheel per worker manages allocations, permissions,
channels, reuse blocks, transactions, reservations, nonces, credentials,
pending operations, TCP connections, mobility overlap, and fast-path rules.
Stale timer entries are ignored by generation rather than searched and removed.

The transaction cache records a request digest and pending/completed outcome.
An exact retransmission repeats no side effect and reuses the prior response;
the same transaction key with different bytes is treated as suspicious.

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

The relay-port allocator maintains state per relay IP, family, transport, and
shard. It selects bounded randomized candidates, supports atomic even-port
reservation, consumes authenticated reservation tokens once, and releases all
state on failed opens.

## 11. Runtime and Platforms

The safe portable backend is the behavior reference on every supported OS. It
uses bounded buffers and no task or timer per allocation.

Linux adds worker-local `SO_REUSEPORT` steering, batched receive/send,
scatter-gather buffers, then `io_uring` only after measurement. Optional eBPF
and AF_XDP can filter or accelerate already-authorized plaintext UDP paths but
cannot authenticate, create state, refresh lifetimes, or independently decide
policy.

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

Resource accounting is hierarchical: global, listener, relay IP, worker,
source address/prefix, realm, tenant, identity, allocation, and peer.
Authentication attempts, allocations, relay ports, permissions, channels, TCP
connections, credential lookups, transactions, packets, bytes, handshakes,
buffers, errors, audits, and admin calls all have limits.

Public-server destination policy denies unsafe special-use destinations,
control infrastructure, metadata services, listeners, relay pools, and relay
loops. Private unicast is controlled by explicit public, enterprise, test, or
custom profiles rather than universally rejected.

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

IANA registries are updated only by a manually invoked tool. Normal builds are
offline and consume reviewed, dated snapshots. Numeric protocol assignments
are generated from that snapshot rather than scattered through source.

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
wire/core/crypto remain `no_std`; packet processing allocates nothing after
startup; all supported transports and address-family combinations
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
