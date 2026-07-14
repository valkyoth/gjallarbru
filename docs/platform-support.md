# Gjallarbru Platform Support

Status: platform policy from repository foundation

The protocol authority is platform-neutral. Platform support is an evidence
claim, not merely a successful cross-compile.

| Platform | Foundation status | Production evidence required by 1.0 |
| --- | --- | --- |
| Linux | workspace builds; portable runtime scaffold | UDP/TCP/TLS/DTLS, privilege, batching, accelerated/fallback differential tests |
| Windows | workspace builds in CI | socket/event backend, service lifecycle, IPv4/IPv6, secure key/config handling |
| BSD | core is OS-neutral | at least FreeBSD runtime/interop CI or documented maintained test host evidence |
| macOS | workspace builds in CI | socket/event backend, launch lifecycle, IPv4/IPv6, TLS/DTLS interoperability |
| Android | core is OS-neutral | NDK build, embedding API, app lifecycle, suspend/resume, network-change tests |
| iOS | core is OS-neutral | Apple target build, embedding API, lifecycle, background constraints, network-change tests |
| Aesynx | no OS dependency in core | compile/test against future Aesynx network, time, randomness, and fixed-storage adapters |

Rules:

- No `cfg` branch changes protocol validity or authorization.
- A platform backend may report unsupported capability; it may not emulate an
  unsafe approximation silently.
- The safe portable backend is the correctness reference.
- Linux-only acceleration is optional and removable.
- Configuration, key, service-manager, and sandbox behavior stays in platform
  modules rather than leaking into core types.
- Every platform queue, socket registry, partial stream, and buffer pool has an
  item and byte ceiling.

