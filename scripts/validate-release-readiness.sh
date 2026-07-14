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
git cat-file -e "HEAD:$report" 2>/dev/null || {
    echo "pentest report must be committed in the tag candidate: $report" >&2
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

reviewed_commit="$(sed -n 's/^Reviewed-Commit: //p' "$report")"
git cat-file -e "${reviewed_commit}^{commit}" 2>/dev/null || {
    echo "pentest Reviewed-Commit does not exist: $reviewed_commit" >&2
    exit 1
}
git merge-base --is-ancestor "$reviewed_commit" HEAD || {
    echo "pentest Reviewed-Commit is not in the tag candidate history" >&2
    exit 1
}

if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
    echo "tag already exists: $tag" >&2
    exit 1
fi
