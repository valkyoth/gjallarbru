# RFC Requirement Ledger

Status: `v0.2.0` base inventory

Gjallarbru binds its implementation plan to the exact RFC 8489 and RFC 8656
bytes already locked under [`rfc/`](../rfc/README.md). The ledger makes every
numbered section and every uppercase RFC 2119/8174 keyword occurrence visible
before protocol implementation begins.

## Artifacts

- [`SCHEMA.json`](SCHEMA.json) defines the machine-readable document, section,
  and requirement fields.
- [`BASE_REQUIREMENTS.json`](BASE_REQUIREMENTS.json) contains 184 numbered
  sections and 393 normative keyword occurrences from RFC 8489 and RFC 8656.
- [`ERRATA.json`](ERRATA.json) records all six RFC Editor errata visible on
  2026-07-14 together with reviewed implementation and security dispositions.

Every requirement records its RFC, section, physical source line, normative
level, conformance profile, owning component, planned or real implementation
symbol, planned or real test, status, security note, and normalized source-line
SHA-256. The containing document is separately bound to `rfc/SHA256SUMS`.

## Status and Assignment Policy

- `planned` requires matching `planned:vX.Y.Z` symbol and test assignments to
  an existing version-plan milestone.
- `implemented` and `verified` cannot retain planned references; they require
  concrete implementation and test evidence.
- `excluded` and `not-applicable` require explicit reviewed evidence rather
  than an empty, unknown, or unassigned field.
- A section with no normative keyword remains in the inventory with an empty
  requirement list. It cannot disappear silently.

The generated keyword records are traceability anchors, not a claim that one
uppercase word always equals one complete semantic rule. During each
implementation milestone, reviewers split or refine anchors when one sentence
contains multiple conditions, inherited requirements, or distinct testable
behaviors. The immutable RFC line and hash remain the provenance boundary.

BCP 14 terminology boilerplate and bibliographic reference sections are
excluded from normative keyword extraction. All numbered body and appendix
sections remain inventoried.

## Errata Policy

- Verified technical errata are applied at their assigned implementation
  milestone and tested against the uncorrected failure case.
- Verified editorial errata are recorded even when they change no behavior.
- Reported, Held for Document Update, and Rejected errata remain visible but do
  not silently override the published RFC text.
- A live status or record change requires explicit review and a committed
  decision update; ordinary CI never depends on the network.

Current decisions apply Verified RFC 8489 errata 6268 and 6290, record Verified
editorial erratum 8434, and track without applying Reported errata 8746, 8900,
and 8901.

## Commands

Run the complete offline gate:

```bash
scripts/validate-requirements.sh
```

Regenerate the deterministic ledger after a reviewed RFC-source or assignment
change:

```bash
scripts/requirements.py --write
```

Compare the committed decisions with the official RFC Editor service during a
deliberate source review:

```bash
scripts/rfc_errata.py --live
```

The live command never rewrites decisions. New or changed errata must be read,
assigned, tested where applicable, and edited through normal review.
