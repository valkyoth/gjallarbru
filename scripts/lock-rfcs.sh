#!/usr/bin/env sh
set -eu

chmod a-w rfc/rfc*.txt rfc/SHA256SUMS
scripts/verify-rfcs.sh

