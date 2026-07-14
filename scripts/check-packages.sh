#!/usr/bin/env sh
set -eu

dirty="$(git status --porcelain --untracked-files=all -- \
    Cargo.toml Cargo.lock \
    crates/gjallarbru-wire \
    crates/gjallarbru-crypto \
    crates/gjallarbru-core)"
test -z "$dirty" || {
    echo "publishable package inputs are dirty:" >&2
    printf '%s\n' "$dirty" >&2
    echo "commit the reviewed package inputs before checking archives" >&2
    exit 1
}

for package in gjallarbru-wire gjallarbru-crypto gjallarbru-core; do
    cargo package -p "$package" --locked --no-verify --list | \
        while IFS= read -r path; do
            case "$path" in
                .cargo_vcs_info.json|Cargo.lock|Cargo.toml|Cargo.toml.orig|README.md|LICENSE-MIT|LICENSE-APACHE|src/*.rs)
                    ;;
                *)
                    echo "$package contains unexpected packaged path: $path" >&2
                    exit 1
                    ;;
            esac
        done
done
