#!/usr/bin/env sh
set -eu

for package in gjallarbru-wire gjallarbru-crypto gjallarbru-core; do
    cargo package -p "$package" --allow-dirty --no-verify --list | \
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
