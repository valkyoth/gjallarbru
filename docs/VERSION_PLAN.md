# Gjallarbru Version Plan

Status: planning document

`v1.0.0` is the first serious production-ready STUN/TURN server application.
The `0.x` sequence uses one narrow, testable primary outcome per minor release.
Patch releases remain available for remediation and follow-up work. Nothing
required by the declared `1.0.0` profiles is postponed until after `1.0.0`.

This file is the compact release index. [`RELEASE_PLAN.md`](RELEASE_PLAN.md) is
the authoritative contract and gives every indexed version its goal,
deliverables, verification, exit criteria, and exact-commit pentest stop.

## Release Rules

Every version must have updated RFC evidence, positive and negative tests,
capacity behavior, documentation, release notes, a clean implementation stop,
and a pentest of the exact candidate before tagging. Milestone claims require
all relevant normative requirements to be `verified`, not merely implemented.
The index and detailed contracts are checked together by
`scripts/validate-release-plan.py`.

## Phase A: Repository and Specification Foundation

| Version | Primary outcome | Completion gate |
| --- | --- | --- |
| `0.1.0` | Repository foundation | Workspace, licenses, policies, CI, RFC tooling, and all foundation checks pass |
| `0.2.0` | RFC requirement-ledger schema | Every section of RFC 8489 and RFC 8656 is indexed with no silent gaps |
| `0.2.1` | Deterministic architecture contract | Reducer inputs, output atomicity, time, entropy, storage, capability, lease, and protocol-name rules are frozen before APIs |
| `0.2.2` | Executed requirement evidence | Semantic requirements can become verified only when CI resolves their real symbol and observes their named test |
| `0.3.0` | IANA snapshot tooling | Reviewed registry snapshot deterministically regenerates protocol assignments |
| `0.4.0` | Primitive domains | Addresses, methods, classes, transactions, monotonic time, absolute-time trust/source generations, limits, and errors have boundary tests |
| `0.4.1` | Complete client-path identity | Listener, socket, provenance, interface, configuration, connection, and worker generations prevent stale or cross-realm authority |
| `0.5.0` | Checked cursors | Exhaustive read/write bounds and arbitrary-slice no-panic tests pass |
| `0.5.1` | Hostile-input parser foundation | Progress, termination, checked padding, complexity, size, and early fuzz obligations are executable |
| `0.6.0` | Generational storage | Fixed slab rejects stale handles and capacity overflow under model/Kani tests |
| `0.6.1` | Freestanding and storage qualification | No-allocator downstream fixtures and bounded storage contracts pass without OS assumptions |

## Phase B: First-Party Wire Protocol

| Version | Primary outcome | Completion gate |
| --- | --- | --- |
| `0.7.0` | STUN header decoder | Type bits, cookie, length, alignment, transaction, truncation, and trailing-byte cases pass |
| `0.8.0` | Borrowed attribute iterator | Padding, duplicates, unknowns, offsets, and truncation pass without allocation |
| `0.8.1` | Authenticated attribute boundary | Nonzero receive padding is accepted structurally and post-integrity attributes cannot affect authenticated semantics |
| `0.9.0` | Frame classifier | STUN/ChannelData/impossible-prefix classification is deterministic across transports |
| `0.10.0` | Address attributes | IPv4/IPv6 mapped and XOR address vectors round trip |
| `0.11.0` | Raw text attributes | USERNAME, REALM, NONCE, SOFTWARE, and ERROR-CODE stay byte-oriented and bounded |
| `0.12.0` | Authentication attributes | Integrity, USERHASH, password algorithms, and exact encoded ranges are exposed safely |
| `0.12.1` | Forward-compatible STUN surface | Alternate routing, security negotiation, unknown methods, and unknown optional attributes remain byte-exact and reviewable |
| `0.13.0` | Allocation attributes | Transport, lifetime, families, even-port, reservation, and fragmentation cases pass |
| `0.14.0` | Permission/channel attributes | Peer, channel, data, and ICMP attributes cover every valid and invalid length |
| `0.15.0` | ChannelData codec | Datagram and stream length/padding boundaries round trip |
| `0.15.1` | UDP ChannelData alignment closure | Both legal datagram forms are accepted while arbitrary trailing bytes remain rejected |
| `0.16.0` | STUN encoder typestate engine | Plan-bound exact-once finalizer slots follow an explicit dependency graph before one transactional caller-buffer commit |
| `0.17.0` | FINGERPRINT finalization | RFC 5769 and corruption vectors pass with CRC finalization integrated and FINGERPRINT last |
| `0.17.1` | Crypto provider and secret contract | Capability-specific fixed-output providers, opaque keys, redacted secrets, and fail-closed errors are proven |
| `0.17.2` | Synchronous and external crypto split | Packet crypto is bounded and deterministic; HSM/KMS work is asynchronous and cannot hide I/O or entropy |
| `0.17.3` | External packet-crypto ownership | Base packet HMAC stays synchronous; any admitted asynchronous profile retains immutable bounded message input through completion |
| `0.18.0` | Legacy message integrity | HMAC-SHA-1 ranges and long-term legacy derivation pass official/project vectors |
| `0.19.0` | SHA-256 message integrity | RFC 8489 SHA-256, errata, ordering, and downgrade cases pass |
| `0.19.1` | Integrity failure closure | Adjusted original-byte ranges, legal truncation, provider failures, mixed algorithms, and response-key uncertainty fail closed |
| `0.20.0` | USERHASH and text preparation | Reviewed PRECIS boundary, canonicalization, and rejection vectors pass |
| `0.20.1` | RFC 8265 PRECIS closure | Current username/password profiles, Unicode versions, migration, and rejection behavior have normative evidence |
| `0.21.0` | Incremental stream framer | Every split/coalescing pattern and bounded partial-frame case passes |
| `0.22.0` | Wire assurance milestone | All wire fuzzers, properties, RFC vectors, MSRV builds, and requirement links pass |
| `0.22.1` | Wire resource and typestate closure | Linear scans, operation ceilings, allocation/copy counters, and authenticated typestate transitions are enforced |

## Phase C: STUN Server Core

| Version | Primary outcome | Completion gate |
| --- | --- | --- |
| `0.23.0` | Sans-I/O event/command API | Synthetic events produce bounded commands with no borrowed data escaping |
| `0.23.1` | Atomic deterministic reducer | Identical explicit inputs produce byte-identical results and capacity failure leaves state and runtime untouched |
| `0.23.2` | Prepared transition and atomic admission | One bounded preparation pass computes exact requirements; permit acquisition and commit never repeat attacker-controlled work |
| `0.23.3` | Linear permit and operation-ID authority | Single-use generation-bound permits release deterministically, while only core creates semantic operation IDs |
| `0.23.4` | Atomic publication memory model | Worker-owned state and reserved command slots become visible through one release/acquire batch-ready publication |
| `0.23.5` | Composable runtime effect envelope | Semantic authority, resource ownership, delivery guarantee, and durability combine orthogonally without false completions |
| `0.23.6` | Chargeable-work accounting | Occupancy, attempt, completion, and retry charges have explicit non-refundable and exactly-once semantics |
| `0.23.7` | Authoritative control-lane progress | Admitted operations reserve terminal completion, compensation, cancellation, shutdown, and ownership-release capacity unavailable to packet traffic |
| `0.23.8` | Bounded observation snapshots | Redacted worker snapshots have fixed size/frequency/retention and can never become protocol authority |
| `0.23.9` | Post-publication crash reconciliation | Every accepted batch is executed, reconciled, or deterministically cancelled across queue/resource/worker failure boundaries |
| `0.23.10` | Portable publication adapters | Core APIs require no atomics or Send/Sync; single-thread and atomic runtime adapters remain behaviorally equivalent |
| `0.23.11` | Terminal mailbox race semantics | Cancellation requests, late success, duplicate terminals, and conflicting observations follow one deterministic fail-closed state machine |
| `0.24.0` | Binding state processing | Correct XOR-MAPPED responses and error paths without sockets |
| `0.25.0` | Stateless authenticated nonces | Source/realm/time-trust binding, stale handling, tamper rejection, and key overlap pass |
| `0.25.1` | Absolute-clock trust model | Uncertain, unavailable, rollback, forward-jump, and recovery generations fail closed without changing monotonic lifetimes |
| `0.26.0` | Credential provider boundary | Fixed and asynchronous lookup models fail closed under timeout/capacity |
| `0.26.1` | Credential timing and provider assurance | Dummy-user work, negative-cache normalization, opaque handles, provider substitution, and leakage tests pass |
| `0.27.0` | Long-term authentication | 401, 438, success, bad integrity, realm, nonce, and identity ordering pass |
| `0.28.0` | Password negotiation profiles | Hardened SHA-256 and legacy interoperability profiles resist downgrade |
| `0.29.0` | Unknown/invalid attribute ordering | Authenticated 420 and method-schema errors match RFC ordering |
| `0.30.0` | Transaction cache | Exact retransmission is idempotent; digest mismatch and exhaustion are safe |
| `0.30.1` | Transaction identity and byte budgets | Keyed strong identity prevents collision confusion and cached responses obey explicit byte ceilings |
| `0.30.2` | Transaction invalidation semantics | Normal reloads pin decisions while revocation explicitly defines replay, error, discard, teardown, and path termination |
| `0.30.3` | Linear ingress work permits | Cheap admission grants finite parse, HMAC, lookup, response, and preparation allowances with monotonic non-refundable refill |
| `0.30.4` | Ingress reservation fairness | Permits are acquired just in time, retained briefly, bounded per listener/worker, and never batch-reserved into starvation |
| `0.31.0` | Portable UDP Binding runtime | Real IPv4 Binding works through the same core path as synthetic tests |
| `0.31.1` | First hot-path resource baseline | Fail-after-startup allocation, copy, task, descriptor, and response-byte instrumentation stays within budget |
| `0.32.0` | IPv6 Binding runtime | IPv6 and dual-stack listener/path identity tests pass |
| `0.33.0` | STUN error and retransmission closure | Error construction, UDP caching, reliable transport, and amplification tests pass |
| `0.33.1` | Alternate routing and security negotiation | 300 Try Alternate, ALTERNATE-SERVER/DOMAIN, loops, trust, and security-feature downgrade cases pass |
| `0.34.0` | `stun-base` milestone | Published RFC 8489 matrix, interoperability, fuzz, and pentest evidence is complete |

## Phase D: RFC 8656 UDP TURN

| Version | Primary outcome | Completion gate |
| --- | --- | --- |
| `0.35.0` | Allocation indexes and records | Path/relay ownership and capacity invariants match a simple reference model |
| `0.36.0` | Hierarchical timing wheel | Allocation, permission, channel, reservation, and stale-generation tests pass |
| `0.36.1` | Timing-wheel debt and jump closure | Stale debt, reschedule policy, expiration work, backlog fairness, and large time jumps remain bounded and cannot extend authority |
| `0.37.0` | Relay-port allocator | Randomized bounded search, collision, exhaustion, and atomic pair tests pass |
| `0.37.1` | Relay-port entropy profile | Explicit worker seeds or completions, unbiased unique candidates, fork/restart handling, and deterministic exhaustion are proven |
| `0.37.2` | Canonical effective destinations | IPv4-mapped, NAT64, scoped IPv6, translated local, multicast, broadcast, and special destinations classify with translation generations |
| `0.37.3` | Translation-generation lifecycle | RFC 6052 mappings are unambiguous, one-step, generation-bound, and safely pin or invalidate dependent authority |
| `0.37.4` | Typed authorized endpoints | Runtime commands carry generation-bound approved peer/relay capabilities and never reconstruct raw policy endpoints |
| `0.37.5` | Execution-time endpoint authority | Queued endpoint capabilities are single-use, deadline-bound, command-bound, charged exactly, and fenced before authority reuse |
| `0.37.6` | Minimum relay safety baseline | Canonical destination/loop denials and fixed relay resource ceilings exist before relay methods |
| `0.38.0` | Allocate semantic validation | Every RFC error path executes without opening a relay resource |
| `0.39.0` | Two-phase allocation state | Duplicate/reordered relay completions cannot duplicate or leak state |
| `0.39.1` | Early state-model assurance | Reference-model and bounded model checks cover duplicate, reordered, stale, and capacity-failed transitions |
| `0.40.0` | Portable relay socket adapter | Exact bind success/failure/close behavior matches synthetic runtime results |
| `0.40.1` | Relay address topology | Bind/public addresses, one-to-one NAT, multi-homing, and public relay-IP pools validate and advertise correctly |
| `0.41.0` | Allocate completion | Success/error responses, actual lifetime, mapped/relayed addresses, and caching pass |
| `0.42.0` | Refresh and delete | Identity match, lifetime changes, zero-delete, and cleanup are atomic |
| `0.43.0` | CreatePermission | Multi-peer atomicity, peer-IP identity, policy denial, and 300-second expiry pass |
| `0.43.1` | Relay payload ownership baseline | Send/Data paths use runtime-owned bounded copies until generation-tagged zero-copy leases are admitted |
| `0.44.0` | Send indication | Authorized relay works; invalid/missing permission paths silently discard |
| `0.45.0` | Peer Data indication | Permission filtering, zero-length data, and rate limits pass |
| `0.46.0` | ChannelBind | Channel/peer uniqueness, refresh, reuse block, and permission coupling pass |
| `0.47.0` | ChannelData relay | Both directions, no lifetime refresh, quotas, and stream padding pass |
| `0.47.1` | Relay buffer-lease ownership | Generation-tagged receive leases and scatter transmit plans cannot outlive or alias reused buffers |
| `0.48.0` | IPv6 relays | IPv4/IPv6 allocation and family mismatch behavior interoperates |
| `0.49.0` | Additional address family | One allocation safely owns two relay families and independent permissions |
| `0.50.0` | EVEN-PORT and reservation tokens | Adjacent reservation, expiry, atomic consume, replay, and tamper tests pass |
| `0.51.0` | DONT-FRAGMENT | Supported/unsupported platform behavior and response mapping pass |
| `0.52.0` | ICMP forwarding | Only correlated, permitted peer errors produce bounded indications |
| `0.53.0` | TURN state model milestone | Arbitrary event sequences preserve all allocation/permission/channel invariants |
| `0.54.0` | UDP interoperability | Browsers, native clients, and coturn oracle scenarios pass IPv4/IPv6/loss tests |
| `0.54.1` | URI, DNS, and discovery profile | RFC 7064/7065 URI handling and RFC 5928/8155 deployment discovery are interoperable and downgrade-safe |
| `0.55.0` | `turn-udp-base` conformance | RFC 8656 requirement and errata matrix is verified end to end |
| `0.55.1` | `gjallarbru` facade crate | A no_std MIT/Apache facade exposes wire, crypto, and core through stable namespaces, uses the repository README without drift, and publishes last |

## Phase E: Security and Operations

| Version | Primary outcome | Completion gate |
| --- | --- | --- |
| `0.56.0` | Destination policy profiles | Public, enterprise, custom, and test profiles pass special-prefix tests |
| `0.57.0` | SSRF and relay-loop prevention | Metadata, control, listener, relay-pool, and self-loop cases fail closed |
| `0.58.0` | Hierarchical quotas | Every global-to-peer capacity dimension remains within configured limits |
| `0.59.0` | Deterministic rate limiting | The v0.30.3 token-bucket primitive extends hierarchically with fairness, spoofable-source, and clock-jump tests |
| `0.60.0` | Credential cache/revocation | Bounded cache, timeout, negative result, revoke, and allocation teardown pass |
| `0.61.0` | Key lifecycle | Credential, nonce, reservation, mobility, and ticket keys rotate independently |
| `0.62.0` | Metrics and audit sinks | Cardinality, redaction, sampling, backpressure, and sink-failure tests pass |
| `0.63.0` | Configuration model | Unknown, duplicate, unsafe, conflicting, and oversized configuration fails closed |
| `0.64.0` | Administrative control plane | Authenticated local control cannot directly mutate worker state |
| `0.64.1` | Tenant and realm isolation | Realm selection, keys, policies, state, certificates, revocation, and usage remain tenant-separated |
| `0.65.0` | Graceful drain/shutdown | New-allocation policy, expiry, forced deadline, and restart tests pass |
| `0.66.0` | Process hardening | Privilege drop, secret handling, filesystem/syscall policy, and failure evidence pass |
| `0.66.1` | Panic blast-radius containment | Supervised worker processes restart after forced aborts within the availability SLO without leaking authority or secrets |
| `0.67.0` | Portable desktop/server runtime | Linux, Windows, BSD, and macOS safe backends pass the common conformance suite |
| `0.68.0` | Mobile embedding | Android and iOS builds, lifecycle, suspension, and bounded background behavior pass |
| `0.69.0` | Aesynx readiness contract | Fixed storage and explicit time/random/network traits compile without OS assumptions |
| `0.70.0` | Security-reviewed UDP server | Full-scope audit/pentest, overload, soak, incident, and recovery findings are closed |

## Phase F: Secure Client Transports and Performance

| Version | Primary outcome | Completion gate |
| --- | --- | --- |
| `0.71.0` | TURN over TCP | Path identity, framing, disconnect, retransmission, and allocation cleanup pass |
| `0.72.0` | Stream backpressure | Slow clients cannot exceed frame, byte, or age ceilings |
| `0.73.0` | TLS provider adapter | Provider-neutral plaintext integration, failure isolation, and pre-semantic early-data rejection pass |
| `0.74.0` | Hardened TLS deployment | Current BCP 195 policy, handshake quotas, rotation, and interoperability pass |
| `0.74.1` | TLS identity and termination | ALPN, SNI, certificate/realm mapping, trusted termination, and PROXY-source handling fail closed |
| `0.75.0` | DTLS provider adapter | Sessions, replay, retransmission, early-data rejection, disconnect, and datagram boundaries pass |
| `0.76.0` | DTLS anti-abuse | Cookie/handshake/time/size/prefix limits resist amplification and exhaustion |
| `0.76.1` | DTLS 1.3 policy | RFC 9147 applicability, TLS/DTLS version profiles, provider capability, and interop evidence are explicit |
| `0.76.2` | Cross-provider early-data closure | Every TLS/DTLS provider, termination topology, resumption path, and node rejects 0-RTT application data consistently |
| `0.77.0` | Standard shared-port demux | RFC 7983/RFC 9443 ranges classify without claiming TURN-over-QUIC |
| `0.77.1` | Common transport ingress accounting | UDP, TCP, TLS, DTLS, trusted termination, and shared-port paths all charge the same normalized per-frame semantic work permit |
| `0.78.0` | Per-core ownership | Stable flow steering and initial Loom models remove global allocation locks without behavior drift |
| `0.78.1` | Expanded concurrency-model closure | Loom inventory expands across reload, rollback, restart, cancellation, shutdown, and promoted counterexamples |
| `0.79.0` | Batched portable/Linux I/O | Batching improves measured throughput while fairness and results remain identical |
| `0.79.1` | Batch completion semantics | Normalized path metadata, partial sends, unsent work, and stale batch results preserve scalar behavior |
| `0.80.0` | Buffer pools and scatter/gather | Allocator instrumentation proves zero packet-path allocations/copies where planned |
| `0.81.0` | `io_uring` backend | Differential, cancellation, stale completion, fallback, and overload tests pass |
| `0.82.0` | Optional eBPF/AF_XDP fast path | Installed rules remain a verified subset of live core authority and fail closed |
| `0.82.1` | Fast-path revocation closure | Revocation, expiry, map loss, reuse, and reconciliation cannot leave kernel authority broader or longer-lived than core state |
| `0.82.2` | Fast-path quota leases | Kernel byte/packet authority is finite, generation-bound, reconciled before renewal, and never independently refillable |

## Phase G: Extensions and Final Assurance

| Version | Primary outcome | Completion gate |
| --- | --- | --- |
| `0.83.0` | RFC 6062 state model | All TCP allocation states and duplicate/reorder cases pass without sockets |
| `0.84.0` | TCP relay allocation/listener | Bounded listener ownership, expiry, close, and port allocation pass |
| `0.85.0` | CONNECT | Authorized outbound connect, timeout, duplicate, quota, and policy tests pass |
| `0.86.0` | CONNECTION-ATTEMPT/BIND | Incoming/outgoing peer connections bind only to the correct allocation |
| `0.87.0` | TCP relay buffering | Pre-bind and bidirectional backpressure remain bounded under slow/failing peers |
| `0.88.0` | `turn-tcp-relay` conformance | RFC 6062 requirement/errata matrix and interoperability are verified |
| `0.89.0` | RFC 7635 authorization | Token format, session keys, audience, expiry, replay, and rotation pass |
| `0.90.0` | RFC 8016 mobility | Protected tickets, old/new path transition, overlap, and replay handling pass |
| `0.91.0` | Shared-secret compatibility auth | De-facto REST-style credentials are isolated, labeled non-RFC, and abuse-tested |
| `0.91.1` | Pawalyze credential issuance | OpenBao-rotated, short-lived, purpose-bound browser credentials enforce user and tenant quotas without reusable passwords |
| `0.92.0` | RFC 5780 diagnostic profile | Isolated listeners, alternate addresses, quotas, and experimental labeling pass |
| `0.93.0` | Formal/static assurance | Selected cursor, slab, state, queue, Miri, Loom, and sanitizer obligations pass |
| `0.94.0` | Long-duration fuzz/soak | Wire/auth/state/timer/runtime campaigns have no unresolved crash or invariant failure |
| `0.95.0` | Platform/interoperability closure | Declared OS, address, transport, client, loss, NAT, and upgrade matrix is complete |

## Phase H: Distributed Production Deployment

| Version | Primary outcome | Completion gate |
| --- | --- | --- |
| `0.96.0` | Multi-node failure contract | Allocations are explicitly node-local; node loss and bounded ICE-restart recovery have tested SLOs |
| `0.96.1` | Secure cluster protocol | Mutually authenticated nodes exchange bounded, versioned control messages without carrying relay payload or client authority |
| `0.96.2` | Cluster membership and load coordination | Two-or-more-node membership, health, capacity, drain, and convergence behavior pass partition and overload tests |
| `0.97.0` | Traffic and relay-pool distribution | DNS/L4/region routing, allocation affinity, relay-IP ownership, and port partitioning avoid collisions and stale nodes |
| `0.97.1` | Fluxheim compatibility profile | TURN/TCP and TURN/TLS pass through Fluxheim with trusted PROXY v2 and affinity; UDP uses a documented direct path until Fluxheim supports generic production UDP |
| `0.98.0` | Coordinated rolling upgrades | Mixed versions, key/certificate distribution, drain, split-brain fencing, rollback, and region failover pass |
| `0.99.0` | Rootless network qualification | Supported Docker/RootlessKit/Podman modes preserve five-tuple identity, publish relay ranges, support 443 options, and meet throughput bounds |
| `0.100.0` | Rootless Wolfi container | Signed multi-arch image runs the full qualified topology as non-root with read-only storage and no added capabilities |
| `0.100.1` | Rootless Debian container | Signed Debian stable-slim image offers a more customizable base while retaining non-root defaults and the qualified network contract |
| `0.101.0` | Pawalyze integration closure | Short-lived credentials and browser calls pass the full transport/NAT/failure matrix; group media is explicitly out of TURN scope |
| `0.102.0` | Production IP-path correctness | IPv6-only, NAT64/464XLAT, multiple public IPs, PMTU, and ICMPv6 Packet Too Big behavior pass |
| `0.103.0` | Network DDoS containment | Edge scrubbing, admission, link-saturation detection, emergency policy, and provider escalation are rehearsed |
| `0.104.0` | Capacity, cost, and autoscaling | Relay ports, bandwidth, egress cost, saturation headroom, SLOs, and scale signals are forecast and load-tested |
| `0.105.0` | Privacy and durable usage | Client-IP retention, regional residency, deletion, redaction, and tenant bandwidth accounting are enforceable and auditable |

## Phase I: Standards Evolution and Final Assurance

| Version | Primary outcome | Completion gate |
| --- | --- | --- |
| `0.106.0` | RFC 7982 measurement profile | Transmit count, loss, and RTT attributes are implemented or explicitly disabled with bounded, interoperable semantics |
| `0.107.0` | RFC 6679 ECN disposition | ECN-check applicability is reviewed and every supported or excluded behavior has conformance and security evidence |
| `0.108.0` | API and configuration evolution | Public semver tests, versioned schemas, migrations, rollback, and mixed-version compatibility pass |
| `0.109.0` | Standards and extension governance | Scheduled RFC/errata/IANA/browser/TLS/dependency reviews and future-extension/unsupported-draft rules are executable |
| `0.110.0` | First-party protocol provenance | Automated dependency and source gates prevent third-party STUN/TURN authority from entering shipped artifacts |
| `0.111.0` | Reproducible packaging | Signed binaries, checksums, SBOM, provenance, containers, and OS package tests pass |
| `0.112.0` | Operational closure | Install, configure, rotate, drain, monitor, respond, upgrade, and rollback guides pass drills |
| `0.113.0` | Specification closure | Every in-scope MUST/MUST NOT/SHOULD, registry entry, and relevant erratum has reviewed evidence |
| `0.114.0` | Independent audit closure | Wire, crypto composition, core, runtime, multi-node, platform, deployment, and supply-chain findings resolve |
| `0.115.0` | Final production release candidate | Only release-blocking fixes remain; the complete release gate passes on the exact candidate |
| `1.0.0` | Production-ready Gjallarbru | Compliance profiles, audits, artifacts, platform evidence, and operational guarantees publish |
