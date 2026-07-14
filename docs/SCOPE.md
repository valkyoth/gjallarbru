# Gjallarbru Scope

Status: policy

Gjallarbru builds a first-party STUN/TURN protocol implementation and server.
Its production scope through `1.0.0` is the set of profiles in
[`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md): STUN base, TURN UDP,
standard client transports, TCP relaying, third-party authorization, mobility,
behavior discovery, shared-port demultiplexing, portable runtimes, security
hardening, acceleration, packaging, and operations.

The project does not build cryptographic primitives, TLS, DTLS, X.509,
Unicode, or PRECIS from scratch. Those capabilities use reviewed providers
behind local interfaces.

TURN-over-QUIC, TURN-over-WebTransport, proprietary relay protocols, ICE agent
behavior, and application media security are not silently treated as STUN/TURN
features. A future custom protocol must have a distinct identifier, negotiation
path, threat model, conformance suite, and repository/version decision.

