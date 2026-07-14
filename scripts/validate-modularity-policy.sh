#!/usr/bin/env sh
set -eu

limit=499
failed=0

find crates scripts -type f \( -name '*.rs' -o -name '*.py' -o -name '*.sh' \) \
    -print | while IFS= read -r file; do
    lines="$(wc -l < "$file")"
    if [ "$lines" -gt "$limit" ]; then
        echo "source file exceeds 499 lines: $file ($lines)" >&2
        exit 1
    fi
done || failed=1

for crate in wire crypto core; do
    file="crates/gjallarbru-${crate}/src/lib.rs"
    grep -Fq '#![no_std]' "$file" || {
        echo "$file must remain no_std" >&2
        failed=1
    }
    grep -Fq '#![forbid(unsafe_code)]' "$file" || {
        echo "$file must forbid unsafe code" >&2
        failed=1
    }
done

if [ "$failed" -ne 0 ]; then
    exit 1
fi
