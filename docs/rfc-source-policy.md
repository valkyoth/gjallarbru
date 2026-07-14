# RFC Source Policy

Status: policy

Gjallarbru uses exact RFC Editor plain-text publications as local normative
references. They are fetched manually, checked into `rfc/`, and bound to
`rfc/SHA256SUMS`. Builds and tests do not download them.

Requirements:

- use only HTTPS RFC Editor URLs listed in `rfc/SOURCES`;
- keep RFC text byte-for-byte unmodified;
- reject missing, extra, changed, empty, or writable tracked RFC text;
- prevent Git line-ending normalization with `.gitattributes`;
- record errata separately rather than editing an RFC;
- review source-list and checksum changes together;
- map normative rules to a machine-readable ledger before implementation;
- use IANA registries, not RFC memory, for current assignments;
- never place RFC text inside published crates or software-license claims.

See [`rfc/README.md`](../rfc/README.md) and the scripts named there.
