<p align="center">
  <b>allocation-free no_std STUN/TURN wire processing for Gjallarbru.</b><br>
  RFC-traceable protocol processing, bounded state, and portable relay runtimes.
</p>

<div align="center">
  <a href="https://crates.io/crates/gjallarbru">Gjallarbru crate</a>
  |
  <a href="https://docs.rs/gjallarbru-wire">Docs.rs</a>
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

# gjallarbru-wire

Support crate for the planned `gjallarbru` facade: allocation-free, zero-copy
STUN/TURN wire parsing, encoding, attribute views, framing, and integrity-range
calculation.

Most users should eventually depend on the facade crate:

```toml
[dependencies]
gjallarbru = "0.55.1"
```

Direct use remains supported for applications that need only the wire layer.
This package is kept separate so its `no_std`, no-allocation, unsafe-free trust
boundary can be audited and versioned independently.

The crate is currently unpublished repository-foundation scaffolding. It does
not parse or emit a STUN/TURN packet yet and makes no protocol compliance claim.

