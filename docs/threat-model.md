# Gjallarbru Threat Model

Status: foundation threat model

## Assets

- Correct STUN/TURN protocol interpretation and RFC conformance.
- Relay authorization, addresses, ports, permissions, and channel bindings.
- Credential-derived keys, nonce keys, tokens, certificates, and private keys.
- Client and peer address privacy.
- Destination policy and internal infrastructure boundaries.
- Runtime availability, capacity, fairness, and billing/quota accuracy.
- Administrative authority, configuration, audit evidence, and release
  artifacts.

## Adversaries

- Unauthenticated remote clients sending malformed, spoofed, duplicated,
  reordered, oversized, or high-rate traffic.
- Authenticated but abusive tenants, users, peers, or administrators.
- Peers attempting unsolicited delivery through relays.
- Attackers targeting internal services through TURN as an SSRF primitive.
- Slow stream clients and handshake floods consuming bounded resources.
- Dependency, CI, registry, build, and release supply-chain attackers.
- Local attackers seeking secrets from logs, panics, dumps, files, or process
  memory.
- Stale runtime completions, timers, fast-path entries, and reused handles.

## Trust Boundaries

- Network bytes to wire-safe borrowed views.
- Wire-safe views to authenticated semantic requests.
- Authenticated requests to allocation and policy state.
- Core commands to operating-system runtime effects.
- Peer datagrams to client delivery.
- Credential, crypto, TLS/DTLS, time, randomness, and storage providers to
  first-party protocol decisions.
- Configuration/admin requests to immutable worker generations.
- Core authority to optional kernel/fast-path rules.
- Source, dependencies, CI actions, RFC/IANA snapshots, and release artifacts.

## Baseline Mitigations

- `no_std`, no-unsafe protocol authority with checked parsing.
- Explicit capacities, quotas, timers, queues, operation limits, and timeouts.
- Authentication and policy before relay resource creation.
- Generational identifiers and two-phase state commits.
- Permissions enforced in both relay directions.
- Source-bound authenticated nonces and rotating keys.
- Default-deny public destination policy and relay-loop prevention.
- Bounded/redacted logs, metrics, errors, and administration.
- Least-privilege runtime and optional sandboxing.
- Locked dependency sources, RFC text, action SHAs, and release evidence.

## Residual Risks

- `no_std` and safe Rust do not prevent protocol or policy logic errors.
- TURN does not provide end-to-end authenticity or confidentiality for relayed
  application payloads.
- Legacy authentication may be required for interoperability and has weaker
  properties than the hardened SHA-256 profile.
- TLS/DTLS providers, OS kernels, credential sources, CSPRNGs, and clocks remain
  trusted dependencies.
- Zeroization cannot prove erasure of compiler-created or historical copies.
- Public TURN service remains a high-value denial-of-service target even with
  bounded degradation.

