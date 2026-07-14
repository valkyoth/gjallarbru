# Gjallarbru Toolchain Policy

Status: policy

Gjallarbru pins stable Rust `1.97.0` and supports Rust `1.90.0` through
`1.97.0`. Rust `1.97.0` was confirmed as stable from the official Rust release
announcement on July 9, 2026.

## Update Rule

Before changing the pinned toolchain:

1. Check the official Rust release announcement and release notes.
2. Review compiler, Cargo, Clippy, rustfmt, target, and security changes.
3. Run `scripts/check-rust-version-matrix.sh` with the new stable included.
4. Run the full repository and release gates.
5. Update README, this policy, CI pins, and release notes.

The MSRV remains `1.90.0` until an explicit semver and ecosystem decision says
otherwise. Resolver 3 is used so dependency selection respects package
`rust-version` declarations.

## Third-Party Crate Rule

Before adding or updating a crate:

1. Check the latest stable release on crates.io.
2. Confirm Rust `1.90.0` support for every required feature.
3. Review license compatibility for the consuming package and EUPL binary.
4. Review maintenance, advisories, unsafe code, build scripts, native code,
   transitive graph, defaults, and feature unification.
5. Disable default features unless each default is explicitly admitted.
6. Confirm core crates retain `no_std` and packet-path allocation policy.
7. Add tests for the behavior and failure modes introduced by the dependency.
8. Record the decision in documentation and release notes.

No build or normal test may fetch specifications or generated source at build
time.

