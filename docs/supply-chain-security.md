# Gjallarbru Supply-Chain Security

Status: policy

- Normal builds are offline with respect to specifications and generated
  sources.
- crates.io is the only allowed registry by default.
- Git sources are denied unless exact-revision pinned and explicitly reviewed.
- Default dependency features are never accepted without inspection.
- Dependencies are versioned centrally, locked, denied on unknown source, and
  checked for advisories, yanks, maintenance, licenses, and duplicates.
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

Freshness checks are intentionally networked and separate:

```bash
scripts/check_latest_tools.sh
```
