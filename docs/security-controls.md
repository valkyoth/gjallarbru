# Gjallarbru Security Controls

Status: control baseline

| Control area | Required control |
| --- | --- |
| Parsing | checked cursor, bounded linear work, no unsafe, exact padding/length validation |
| Authentication | RFC ordering, modern SHA-256 preference, explicit legacy profile, constant-time verification |
| Nonces/tokens | authenticated, versioned, scoped, expiring, key identified, replay tested |
| State | generational handles, bounded storage, atomic transitions, deterministic time |
| Relay | authenticated allocation, unique ownership, randomized bounded port selection |
| Permissions | live peer-IP permission in both directions; channel also requires permission |
| SSRF | destination profiles, special-range denial, metadata/control isolation, relay-loop rejection |
| Availability | hierarchical quotas/rate limits, bounded queues/buffers/lookups/errors/logs |
| Streams | partial-frame limits, queued-byte limits, backpressure, write-age/handshake timeouts |
| Acceleration | authorization subset invariant, generation/epoch/expiry, fail-closed fallback |
| Secrets | no debug/log/metric output, separate key domains, rotation, dump restrictions |
| Administration | separate authenticated endpoint, immutable generations, auditable commands |
| Supply chain | crates.io only by default, action SHA pins, cargo-deny/audit, SBOM/provenance |
| Releases | candidate tests, pentest/retest, documented CodeQL remediation, final green CI, signed evidence |

Every control gains an implementation symbol, test identifier, and release
evidence before its associated compliance profile is claimed.
