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
- keep every numbered RFC 8489/8656 section visible, including sections with
  no extracted normative keyword;
- apply Verified errata and track unresolved errata without silently changing
  immutable RFC text;
- use IANA registries, not RFC memory, for current assignments;
- never place RFC text inside published crates or software-license claims.

See [`rfc/README.md`](../rfc/README.md), the
[`requirements` ledger](../requirements/README.md), and the scripts named
there.
