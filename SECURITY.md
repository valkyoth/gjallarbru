# Security Policy

`gjallarbru` is security-sensitive Internet protocol and relay software. Treat
wire parsing, message integrity, authentication, nonce and token handling,
allocation state, permissions, channels, destination policy, runtime I/O,
administration, release scripts, CI, and dependency changes as high risk.

## Current Status

The repository is a foundation scaffold. It is not a functioning STUN/TURN
server and must not be deployed as one.

## Routine Checks

Run these regularly and before releases:

```bash
scripts/checks.sh
scripts/check-rust-version-matrix.sh
scripts/check_latest_tools.sh
cargo deny check
cargo audit
```

GitHub Actions run CI. GitHub CodeQL default setup must be enabled in repository
security settings. Do not add an advanced CodeQL workflow while default setup
is active. See
[`docs/github-security-settings.md`](docs/github-security-settings.md).

## Release Gate

Every release requires:

- a clean implementation stop;
- all local checks and dependency policy checks passing;
- release notes for the exact candidate;
- a security review and pentest of the exact commit;
- remediation and retest of findings;
- a permanent `Status: PASS` report under `security/pentest/`;
- confirmation that GitHub CI and CodeQL default setup are green.

Tags and release publication occur only when explicitly requested after those
conditions are satisfied.

## Dependency Policy

The dependency policy lives in `deny.toml`. Unknown registries and git sources
are denied. Git dependencies require an exact revision and an explicit,
reviewed exception.

Every new or updated crate requires:

- a current crates.io version check;
- license and maintenance review;
- advisory and feature review;
- proof that `no_std` packages retain their intended boundary;
- proof that it does not import a third-party STUN/TURN implementation;
- tests for the admitted behavior;
- `cargo deny check` and `cargo audit` evidence.

## Reporting

Do not publish exploitable details before a fix is available. Use a private
GitHub security advisory or contact the maintainers through the repository's
configured private security channel.

