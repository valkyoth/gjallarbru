# Gjallarbru Supply-Chain Security

Status: policy

- Normal builds are offline with respect to specifications and generated
  sources.
- crates.io is the only allowed registry by default.
- Git sources are denied unless exact-revision pinned and explicitly reviewed.
- Default dependency features are never accepted without inspection.
- Dependencies are versioned centrally, locked, denied on unknown source, and
  checked for advisories, yanks, maintenance, licenses, and duplicates.
- Workspace resolution, MSRV checks, metadata, package archives, and publishing
  use `--locked`; CI fails instead of rewriting `Cargo.lock`.
- Publishable package inputs must be committed before archive allowlists run,
  and crate publishing rechecks the clean tree after all preflight commands.
- GitHub Actions use immutable full commit SHAs with release-tag comments.
- Dependabot covers Cargo and GitHub Actions weekly.
- CodeQL uses GitHub default setup, not a duplicate advanced workflow.
- RFC reference text and later IANA snapshots are checksum locked and updated
  only by deliberate networked tools.
- Release artifacts will include checksums, signatures, SBOMs, and provenance.
- Container final roots use reviewed, digest-pinned Wolfi/apko and Debian
  stable-slim definitions; each image has independent rebuild, package,
  customization, SBOM, signature, provenance, and vulnerability evidence
  rather than mutable `latest` inputs.
- A release does not rely on uncommitted local source, mutable network content,
  or one developer machine.

For `v0.1.0`, `scripts/test-foundation-dependency-surface.py` locks the observed
zero-third-party Cargo graph. The first external dependency must deliberately
update that baseline together with its version, feature, license, maintenance,
advisory, constant-time/secret-handling where applicable, and no_std review.

Freshness checks are intentionally networked and separate:

```bash
scripts/check_latest_tools.sh
```
