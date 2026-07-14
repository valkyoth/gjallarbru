# RFC Reference Copies

This directory contains exact, unmodified plain-text copies downloaded from
the [RFC Editor](https://www.rfc-editor.org/). Gjallarbru uses them as local
normative references for requirement matrices, implementation review, test
vectors, errata decisions, and security analysis.

Gjallarbru and its maintainers claim no copyright in these RFC documents. Each
RFC retains its original copyright notices, authorship, status, disclaimers,
and legal terms. The RFC files are not licensed under the project's EUPL-1.2,
MIT, or Apache-2.0 software licenses; they remain governed by their own notices
and the [IETF Trust Legal Provisions](https://trustee.ietf.org/license-info).

The RFC Editor permits unmodified reproduction. These copies must never be
edited, reformatted, annotated, line-ending normalized, or stripped of
notices. Project notes belong in `docs/` or later requirement/errata data.

The machine-readable base section inventory, normative keyword ledger, and
reviewed errata decisions live in [`requirements/`](../requirements/README.md).
They bind back to these checksum-locked bytes and never modify them.

## Tracked Baseline

| RFC | Role |
| --- | --- |
| RFC 2119 and RFC 8174 | Normative requirement language |
| RFC 5769 | Official STUN test vectors |
| RFC 5780 | Experimental NAT behavior discovery profile |
| RFC 5928 | TURN DNS resolution procedures |
| RFC 6062 | TURN TCP peer relaying |
| RFC 6679 | ECN check attributes and procedures; explicit profile disposition required |
| RFC 7064 | STUN and STUNS URI syntax |
| RFC 7065 | TURN and TURNS URI syntax and transport selection |
| RFC 7350 | STUN/TURN over DTLS |
| RFC 7376 | Long-term authentication weaknesses and deployment mitigations |
| RFC 7443 | STUN/TURN ALPN protocol identifiers |
| RFC 7635 | TURN third-party authorization |
| RFC 7982 | STUN loss and RTT measurement attributes |
| RFC 7983 | Shared-port packet demultiplexing |
| RFC 8016 | TURN allocation mobility |
| RFC 8155 | TURN server auto-discovery |
| RFC 8265 | Current PRECIS username and password profiles |
| RFC 8489 | Current STUN base |
| RFC 8656 | Current TURN base, including IPv6 |
| RFC 9147 | DTLS 1.3 provider and deployment considerations |
| RFC 9325 | Current TLS/DTLS deployment recommendations |
| RFC 9443 | QUIC/TURN shared-port demultiplexing, not TURN-over-QUIC |

The set grows when the requirement ledger proves another normative reference
or extension is needed. Missing work is added immediately; the list is not a
ceiling.

## Integrity Lock

- `SOURCES` is the reviewed URL and role allowlist.
- `SHA256SUMS` pins the exact bytes of every `rfc*.txt` file.
- `scripts/verify-rfcs.sh` rejects changed, missing, extra, or corrupt text.
- `scripts/fetch-rfcs.sh` downloads only missing allowlisted HTTPS sources,
  verifies them, and makes the local copies read-only.
- `scripts/lock-rfcs.sh` reapplies the local read-only guard.
- `scripts/test-rfc-sources.py` tests the complete source/checksum baseline.
- `scripts/validate-requirements.sh` rejects missing, stale, duplicate,
  invalid, falsely completed, or unassigned RFC 8489/8656 requirements and
  errata decisions.
- `.gitattributes` disables text and line-ending normalization for RFC text.
- `CODEOWNERS` protects this directory when branch rules require review.

Git does not portably preserve read-only permissions; checksums and review are
the authoritative guard.

## Update Procedure

1. Add the exact RFC Editor URL and role to `SOURCES`.
2. Download to a temporary directory and inspect provenance and document
   identity.
3. Add the untouched file and its SHA-256 checksum in one reviewed change.
4. Run `scripts/fetch-rfcs.sh`, `scripts/verify-rfcs.sh`, and the full checks.
5. Update the requirement inventory, errata decisions, plans, and release
   notes.

Published RFCs are immutable. Corrections are tracked as RFC Editor errata or
new RFCs, never by modifying local RFC text.

## crates.io Exclusion

The root is a virtual Cargo workspace. Publishable packages live below
`crates/` and must use strict package allowlists; RFC text must never enter a
crate archive.
