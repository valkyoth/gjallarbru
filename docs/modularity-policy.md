# Gjallarbru Modularity Policy

`gjallarbru` must not become a monolithic source tree or one platform-specific
server.

Rules:

- the future `gjallarbru` package is a `no_std` facade of namespaced public
  re-exports, never an implementation or runtime home;
- `gjallarbru-wire` owns syntax, never authentication databases or state.
- `gjallarbru-crypto` owns protocol cryptographic composition and provider
  traits, never sockets or allocation state.
- `gjallarbru-core` owns protocol authority, never operating-system I/O.
- `gjallarbru-runtime` executes core commands but cannot expand authority.
- future `gjallarbru-cluster` owns bounded node coordination but cannot parse
  public TURN traffic, carry relay payload, or mutate core allocation state.
- `gjallarbru-server` orchestrates configuration and process lifecycle.
- `lib.rs` and `main.rs` remain wiring/orchestration files.
- Parsing, semantic validation, authentication, state, storage, policy,
  platform I/O, and tests use focused modules.
- Non-generated Rust files must remain below 500 lines.
- A Rust file approaching 300 lines must be reviewed for a coherent split.
- Tests may be separate sibling modules; production files do not grow to keep
  tests inline.
- New crates require a trust, dependency, publication, or platform boundary.
- Platform adapters depend inward; core crates never depend outward.
- Feature flags never silently enable networking, legacy cryptography,
  administrative access, custom protocols, or acceleration.

The local gate is:

```bash
scripts/validate-modularity-policy.sh
```
