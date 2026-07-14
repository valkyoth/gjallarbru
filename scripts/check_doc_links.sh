#!/usr/bin/env sh
set -eu

missing=0
find README.md CHANGELOG.md SECURITY.md docs rfc release-notes security \
    -type f -name '*.md' -print | while IFS= read -r file; do
    sed -n 's/.*](\([^)]*\.md\)).*/\1/p' "$file" | while IFS= read -r link; do
        case "$link" in
            http://*|https://*) continue ;;
            /*) target=".$link" ;;
            *) target="$(dirname "$file")/$link" ;;
        esac
        if [ ! -f "$target" ]; then
            echo "missing markdown link target: $file -> $link" >&2
            exit 1
        fi
    done || missing=1
done

if [ "$missing" -ne 0 ]; then
    exit 1
fi

