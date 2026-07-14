# Gjallarbru Licensing

Status: policy

Gjallarbru uses package-specific licenses.

## EUPL-1.2 Application Code

These packages and their source are EUPL-1.2:

- `crates/gjallarbru-runtime`
- `crates/gjallarbru-server`
- future `crates/gjallarbru-cluster` introduced by `v0.96.1`
- future deployment, administration, and binary-only internal crates unless
  their manifests state otherwise

The distributed `gjallarbru` server application is EUPL-1.2. The authoritative
text is [`LICENSE-EUPL-1.2`](../LICENSE-EUPL-1.2).

## MIT OR Apache-2.0 Reusable Crates

These crates are dual-licensed under MIT OR Apache-2.0:

- `crates/gjallarbru-wire`
- `crates/gjallarbru-crypto`
- `crates/gjallarbru-core`

Their manifest metadata is the package boundary used by crates.io. The license
texts are [`LICENSE-MIT`](../LICENSE-MIT) and
[`LICENSE-APACHE`](../LICENSE-APACHE), with matching copies included in each
crate archive.

This split is practical: permissively licensed reusable crates can be linked
into the EUPL application, while the final runtime/server distribution remains
EUPL-1.2. New cross-boundary shared code must be placed deliberately; code is
not copied from the EUPL runtime into a permissive crate without provenance and
licensing review.

## RFC Documents

Files under `rfc/rfc*.txt` retain their IETF notices and are not licensed under
any Gjallarbru software license. See [`rfc/README.md`](../rfc/README.md).

## Contributions

Contributions are licensed according to the package or directory they modify.
A contribution spanning both license domains is provided under each applicable
license for the respective files.
