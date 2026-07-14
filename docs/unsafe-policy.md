# Gjallarbru Unsafe Code Policy

Status: policy

`gjallarbru-wire`, `gjallarbru-crypto`, and `gjallarbru-core` forbid unsafe
code. Protocol parsing, authentication composition, state transitions, policy,
timers, and bounded storage must remain safe Rust.

The foundation runtime and server also forbid unsafe code. A later runtime may
admit unsafe only when a safe implementation cannot express a required system
call, buffer-ownership, eBPF, AF_XDP, or platform FFI boundary.

Before any unsafe is admitted:

- isolate it in a named runtime module;
- document invariants at module and call sites;
- add a `SAFETY:` explanation for every unsafe block;
- test alignment, validity, aliasing, lifetime, concurrency, cancellation, and
  stale-generation behavior;
- compare behavior with the safe portable backend;
- run Miri where applicable and sanitizers for the compiled runtime path;
- update the threat model and release notes;
- obtain explicit security review.

Unsafe code is never admitted merely for speculative performance.

