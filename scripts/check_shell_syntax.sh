#!/usr/bin/env sh
set -eu

check_file() {
    file="$1"
    shebang="$(sed -n '1p' "$file")"
    case "$shebang" in
        '#!/usr/bin/env bash'|'#!/bin/bash') bash -n "$file" ;;
        *) sh -n "$file" ;;
    esac
}

if [ "$#" -gt 0 ]; then
    for file in "$@"; do
        check_file "$file"
    done
else
    find scripts -type f -name '*.sh' -print | while IFS= read -r file; do
        check_file "$file"
    done
fi
