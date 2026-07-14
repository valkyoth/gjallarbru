#!/usr/bin/env sh
set -eu

python3 scripts/requirements.py
python3 scripts/rfc_errata.py
python3 scripts/test-requirements.py
