#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
    echo "usage: scripts/validate-release-readiness.sh vX.Y.Z" >&2
    exit 2
fi

tag="$1"
version="${tag#v}"
report="security/pentest/${tag}.md"
notes="release-notes/RELEASE_NOTES_${version}.md"

test "$tag" != "$version" || {
    echo "release tag must start with v" >&2
    exit 1
}
test ! -e PENTEST.md || {
    echo "remove root PENTEST.md before release readiness" >&2
    exit 1
}
test -s "$notes" || {
    echo "missing release notes: $notes" >&2
    exit 1
}
test -s "$report" || {
    echo "missing pentest report: $report" >&2
    exit 1
}
grep -Eq '^Status: PASS$' "$report"
grep -Eq '^Reviewed-Commit: [0-9a-f]{40}$' "$report"
grep -Eq '^Tester: .+' "$report"
grep -Eq '^Date: [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$report"
grep -Eq '^Scope: .+' "$report"

test -z "$(git status --porcelain)" || {
    echo "release readiness requires a clean worktree" >&2
    exit 1
}

parent_fields="$(git rev-list --parents -n 1 HEAD | awk '{print NF}')"
test "$parent_fields" -eq 2 || {
    echo "pentest report must be a non-merge commit directly after the reviewed commit" >&2
    exit 1
}

reviewed_commit="$(sed -n 's/^Reviewed-Commit: //p' "$report")"
parent_commit="$(git rev-parse HEAD^)"
test "$reviewed_commit" = "$parent_commit" || {
    echo "pentest Reviewed-Commit is not the report commit's parent" >&2
    exit 1
}

changed_files="$(git diff-tree --no-commit-id --name-only -r HEAD)"
test "$changed_files" = "$report" || {
    echo "pentest report commit must change only: $report" >&2
    exit 1
}

if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
    echo "tag already exists: $tag" >&2
    exit 1
fi
