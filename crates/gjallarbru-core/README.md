<p align="center">
  <b>deterministic no_std STUN/TURN server state for Gjallarbru.</b><br>
  RFC-traceable protocol processing, bounded state, and portable relay runtimes.
</p>

<div align="center">
  <a href="https://crates.io/crates/gjallarbru">Gjallarbru crate</a>
  |
  <a href="https://docs.rs/gjallarbru-core">Docs.rs</a>
  |
  <a href="https://github.com/valkyoth/gjallarbru/blob/main/docs/RELEASE_PLAN.md">Release Plan</a>
  |
  <a href="https://github.com/valkyoth/gjallarbru/blob/main/docs/threat-model.md">Threat Model</a>
  |
  <a href="https://github.com/valkyoth/gjallarbru/blob/main/SECURITY.md">Security</a>
</div>

<br>

<p align="center">
  <a href="https://github.com/valkyoth/gjallarbru">
    <img src="https://raw.githubusercontent.com/valkyoth/gjallarbru/main/.github/images/gjallarbru.webp" alt="Gjallarbru STUN and TURN server overview">
  </a>
</p>

# gjallarbru-core

Support crate for the planned `gjallarbru` facade: deterministic, bounded,
Sans-I/O STUN/TURN authentication, transaction, allocation, permission,
channel, timer, quota, destination-policy, and relay-authority state.

Most users should eventually depend on the facade crate:

```toml
[dependencies]
gjallarbru = "0.55.1"
```

Direct use remains supported for alternate runtimes, embedded systems,
simulators, and future Aesynx integration. This package never owns sockets,
system time, TLS/DTLS, operating-system types, or process configuration.

The crate is currently unpublished repository-foundation scaffolding. It
exposes no server state engine and makes no protocol compliance claim yet.

