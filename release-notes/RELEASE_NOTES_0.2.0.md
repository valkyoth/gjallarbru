# Gjallarbru 0.2.0 Release Notes

Release type: RFC requirement and errata traceability foundation

## Scope

`0.2.0` makes the complete RFC 8489 STUN and RFC 8656 TURN base structure
visible before protocol implementation. It adds a checksum-bound section
inventory, normative keyword ledger, strict schema, reviewed errata decisions,
and negative validation fixtures.

This release also plans the future `gjallarbru` facade and brings the reusable
support-crate READMEs into the common project branding and security-navigation
style.

## Requirement Evidence

- All 184 numbered body and appendix sections from RFC 8489 and RFC 8656 are
  inventoried, including sections with no extracted normative keyword.
- All 393 uppercase RFC 2119/8174 keyword occurrences outside terminology
  boilerplate and bibliographic references are bound to physical source lines
  and normalized line hashes.
- Every extracted entry identifies its RFC, section, level, profile, component,
  planned implementation symbol, planned test, status, and security note.
- Planned references must target an existing version milestone.
- Implemented or verified entries cannot retain planned evidence.
- Excluded and not-applicable entries require explicit reviewed evidence.

## Errata Decisions

- Verified RFC 8489 errata 6268 and 6290 are assigned to implementation and
  regression milestones.
- Verified editorial erratum 8434 is recorded as behavior-neutral.
- Reported errata 8746, 8900, and 8901 are tracked but do not silently override
  the immutable RFC publications.
- Normal CI validates the committed decisions offline; an explicit live command
  compares them with the official RFC Editor service during source review.

## Security

- The RFC bytes remain unmodified and checksum-locked.
- Missing fields, duplicate IDs, invalid levels, unassigned references, unknown
  milestones, orphaned sections, false completion, evidence-free exclusions,
  and premature application of unverified errata fail regression tests.
- The ledger contains no third-party dependency and introduces no parser,
  listener, authentication, allocation, or relay attack surface.
- Requirement extraction is a traceability anchor, not a semantic conformance
  claim. Each implementation milestone must refine and verify its assigned
  rules before changing status.

## Crate Publication

No crate is published to crates.io for `v0.2.0`. The reusable support crates
remain at their unpublished `0.1.0` package versions, and the facade is planned
for its dedicated `v0.55.1` admission milestone.

## Known Limitations

- No STUN or TURN packet is parsed or emitted.
- No server or relay socket is opened.
- All base requirements remain `planned`; no protocol compliance profile is
  claimed.
- This version must not be deployed as a server.

## Verification

```bash
scripts/validate-requirements.sh
scripts/checks.sh
scripts/check-rust-version-matrix.sh
cargo deny --locked check
cargo audit
```

The optional networked errata freshness check is:

```bash
scripts/rfc_errata.py --live
```

Tagging requires a green pentest/retest report, final green GitHub CI and
CodeQL, and the `v0.2.0` release-readiness gate.
