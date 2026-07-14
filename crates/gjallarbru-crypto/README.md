<p align="center">
  <b>no_std STUN/TURN cryptographic boundaries for Gjallarbru.</b><br>
  RFC-traceable protocol processing, bounded state, and portable relay runtimes.
</p>

<div align="center">
  <a href="https://crates.io/crates/gjallarbru">Gjallarbru crate</a>
  |
  <a href="https://docs.rs/gjallarbru-crypto">Docs.rs</a>
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

# gjallarbru-crypto

Support crate for the planned `gjallarbru` facade: provider-neutral integrity,
credential derivation, constant-time verification, authenticated nonce, token,
secret-wrapper, and key-generation composition for STUN/TURN.

Most users should eventually depend on the facade crate:

```toml
[dependencies]
gjallarbru = "0.55.1"
```

Direct use remains supported for applications that need only the cryptographic
protocol boundary. This package is kept separate so primitive providers can be
reviewed without importing sockets, TLS/DTLS, allocation state, or a runtime.

The crate is currently unpublished repository-foundation scaffolding. It does
not implement TLS or DTLS and exposes no cryptographic protocol API yet.

