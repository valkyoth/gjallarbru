# GitHub Security Settings

GitHub CodeQL default setup is required for the public repository.

This project intentionally has no advanced CodeQL workflow because running
default and advanced analysis for the same language can create duplicate or
conflicting SARIF uploads.

Before a release tag:

1. Open repository settings and select Code security.
2. Confirm CodeQL default setup is active for the default branch.
3. Confirm Dependabot alerts, security updates, and secret scanning settings
   appropriate to the repository are enabled.
4. Confirm the exact candidate's latest CI and CodeQL analyses succeeded.
5. Record this evidence in the permanent pentest report.

