#!/usr/bin/env sh
set -eu

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
validator="$(pwd)/scripts/validate-release-readiness.sh"

make_fixture() {
    name="$1"
    repo="$tmp/$name"
    mkdir -p "$repo/scripts" "$repo/release-notes" "$repo/security/pentest"
    cp "$validator" "$repo/scripts/validate-release-readiness.sh"
    (
        cd "$repo"
        git init -q
        git config user.email "release-readiness@example.invalid"
        git config user.name "Release Readiness Test"
        printf 'fixture\n' >README.md
        mkdir -p release-notes
        printf '# Release 0.1.0\n' >release-notes/RELEASE_NOTES_0.1.0.md
        git add README.md release-notes/RELEASE_NOTES_0.1.0.md \
            scripts/validate-release-readiness.sh
        git commit -q -m "implementation candidate"
    )
    printf '%s\n' "$repo"
}

write_report() {
    reviewed="$1"
    mkdir -p security/pentest
    {
        printf 'Status: PASS\n'
        printf 'Reviewed-Commit: %s\n' "$reviewed"
        printf 'Tester: Release Readiness Test\n'
        printf 'Date: 2026-07-14\n'
        printf 'Scope: Fixture release workflow.\n'
    } >security/pentest/v0.1.0.md
}

assert_fails_with() {
    expected="$1"
    shift
    if "$@" >"$tmp/stdout" 2>"$tmp/stderr"; then
        echo "expected command to fail: $*" >&2
        exit 1
    fi
    grep -Fq "$expected" "$tmp/stderr" || {
        echo "expected stderr to contain: $expected" >&2
        sed -n '1,120p' "$tmp/stderr" >&2
        exit 1
    }
}

repo="$(make_fixture missing-report)"
(
    cd "$repo"
    assert_fails_with "missing pentest report" \
        scripts/validate-release-readiness.sh v0.1.0
)

repo="$(make_fixture scratch-findings)"
(
    cd "$repo"
    printf 'finding\n' >PENTEST.md
    assert_fails_with "remove root PENTEST.md" \
        scripts/validate-release-readiness.sh v0.1.0
)

repo="$(make_fixture uncommitted-report)"
(
    cd "$repo"
    write_report "$(git rev-parse HEAD)"
    assert_fails_with "pentest report must be committed" \
        scripts/validate-release-readiness.sh v0.1.0
)

repo="$(make_fixture unrelated-review)"
(
    cd "$repo"
    base="$(git symbolic-ref --short HEAD)"
    git checkout -q -b unrelated
    printf 'unrelated\n' >unrelated.txt
    git add unrelated.txt
    git commit -q -m "unrelated"
    unrelated="$(git rev-parse HEAD)"
    git checkout -q "$base"
    write_report "$unrelated"
    git add security/pentest/v0.1.0.md
    git commit -q -m "pentest report"
    assert_fails_with "not in the tag candidate history" \
        scripts/validate-release-readiness.sh v0.1.0
)

repo="$(make_fixture green-report)"
(
    cd "$repo"
    reviewed="$(git rev-parse HEAD)"
    write_report "$reviewed"
    git add security/pentest/v0.1.0.md
    git commit -q -m "pentest report"
    scripts/validate-release-readiness.sh v0.1.0
)

repo="$(make_fixture codeql-remediation)"
(
    cd "$repo"
    reviewed="$(git rev-parse HEAD)"
    write_report "$reviewed"
    git add security/pentest/v0.1.0.md
    git commit -q -m "pentest report"
    printf 'codeql remediation\n' >>README.md
    printf '\nCodeQL remediation: fixed and verified.\n' \
        >>security/pentest/v0.1.0.md
    git add README.md security/pentest/v0.1.0.md
    git commit -q -m "fix CodeQL finding and update report"
    scripts/validate-release-readiness.sh v0.1.0
)

printf 'release readiness workflow tests passed\n'
