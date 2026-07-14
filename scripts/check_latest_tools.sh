#!/usr/bin/env sh
set -eu

ci_file=".github/workflows/ci.yml"

ci_tool_version() {
    tool="$1"
    sed -n "s/.*cargo install --locked ${tool} --version \([0-9][^ ]*\).*/\1/p" \
        "$ci_file" | head -n 1
}

latest_crate_version() {
    crate="$1"
    cargo info "$crate" | sed -n 's/^version: //p' | head -n 1
}

check_cargo_tool() {
    tool="$1"
    pinned="$(ci_tool_version "$tool")"
    latest="$(latest_crate_version "$tool")"

    test -n "$pinned" || {
        echo "missing pinned CI version for $tool" >&2
        exit 1
    }
    test -n "$latest" || {
        echo "could not determine latest crates.io version for $tool" >&2
        exit 1
    }
    test "$pinned" = "$latest" || {
        echo "$tool is not latest: pinned $pinned, latest $latest" >&2
        exit 1
    }
}

check_action_pins() {
    failed=0
    for file in .github/workflows/*.yml; do
        sed -n 's/^[[:space:]]*uses: [^@][^@]*@\([^[:space:]]*\).*/\1/p' \
            "$file" | while IFS= read -r ref; do
            case "$ref" in
                [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]) ;;
                *)
                    echo "GitHub Actions ref is not a full SHA: $file: $ref" >&2
                    exit 1
                    ;;
            esac
        done || failed=1
    done
    test "$failed" -eq 0
}

check_checkout_currency() {
    pin_line="$(sed -n 's/.*uses: actions\/checkout@\([0-9a-f]\{40\}\) # \(v[0-9][0-9.]*\).*/\1 \2/p' "$ci_file" | head -n 1)"
    test -n "$pin_line" || {
        echo "actions/checkout pin and tag comment are missing" >&2
        exit 1
    }
    pinned_sha="$(printf '%s\n' "$pin_line" | awk '{ print $1 }')"
    pinned_tag="$(printf '%s\n' "$pin_line" | awk '{ print $2 }')"
    latest_tag="$(git ls-remote --tags --refs https://github.com/actions/checkout.git 'refs/tags/v*' | sed 's#.*refs/tags/##' | grep -E '^v[0-9]+(\.[0-9]+)*$' | sort -V | tail -n 1)"
    latest_sha="$(git ls-remote --tags --refs https://github.com/actions/checkout.git "refs/tags/${latest_tag}" | awk '{ print $1 }')"
    test "$pinned_tag" = "$latest_tag" || {
        echo "actions/checkout is not latest: pinned $pinned_tag, latest $latest_tag" >&2
        exit 1
    }
    test "$pinned_sha" = "$latest_sha" || {
        echo "actions/checkout $latest_tag SHA mismatch" >&2
        exit 1
    }
}

check_cargo_tool cargo-deny
check_cargo_tool cargo-audit
check_cargo_tool cargo-sbom
check_action_pins
check_checkout_currency
