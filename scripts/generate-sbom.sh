#!/usr/bin/env sh
set -eu

mode="${1:---write}"
target="sbom/gjallarbru.spdx.json"
temporary="$(mktemp "${TMPDIR:-/tmp}/gjallarbru-sbom.XXXXXX")"
trap 'rm -f "$temporary"' EXIT HUP INT TERM

cargo sbom --output-format spdx_json_2_3 > "$temporary"
test -s "$temporary"

case "$mode" in
    --check)
        test -s "$target"
        python3 scripts/compare_sbom.py "$target" "$temporary"
        ;;
    --write)
        mkdir -p sbom
        mv "$temporary" "$target"
        ;;
    *)
        echo "usage: scripts/generate-sbom.sh [--check|--write]" >&2
        exit 2
        ;;
esac

