#!/usr/bin/env python3
"""Publish Gjallarbru reusable crates in crates.io dependency order."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - release host guard.
    print("Python 3.11+ is required because this script uses tomllib.", file=sys.stderr)
    raise


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "release-crates.toml"
CHANGE_KINDS = (
    "unpublished",
    "initial",
    "code",
    "breaking",
    "fix",
    "dependency",
    "metadata",
    "unchanged",
)
PUBLISH_ORDER = (
    "gjallarbru-wire",
    "gjallarbru-crypto",
    "gjallarbru-core",
)
PRIVATE_PACKAGES = (
    "gjallarbru-runtime",
    "gjallarbru-server",
)


def run(command: list[str], *, dry_run: bool) -> None:
    print(f"+ {' '.join(command)}", flush=True)
    if not dry_run:
        subprocess.run(command, cwd=ROOT, check=True)


def capture(command: list[str]) -> str:
    return subprocess.check_output(command, cwd=ROOT, text=True).strip()


def try_capture(command: list[str]) -> str | None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def parse_version(version: str) -> tuple[int, int, int]:
    parts = version.split(".")
    if len(parts) != 3:
        raise RuntimeError(f"version must be MAJOR.MINOR.PATCH: {version}")
    try:
        parsed = tuple(int(part) for part in parts)
    except ValueError as exc:
        raise RuntimeError(f"version must be numeric: {version}") from exc
    if any(part < 0 for part in parsed):
        raise RuntimeError(f"version components must be non-negative: {version}")
    return parsed  # type: ignore[return-value]


def cargo_metadata() -> dict:
    raw = capture(["cargo", "metadata", "--format-version", "1", "--no-deps"])
    return json.loads(raw)


def workspace_packages(metadata: dict) -> dict[str, dict]:
    workspace_ids = set(metadata["workspace_members"])
    return {
        package["name"]: package
        for package in metadata["packages"]
        if package["id"] in workspace_ids
    }


def release_plan(plan_path: Path) -> dict:
    plan = load_toml(plan_path)
    release = plan.get("release", {})
    crates = plan.get("crates", {})
    version = release.get("version")
    policy = release.get("policy")
    if not isinstance(version, str):
        raise RuntimeError("release-crates.toml is missing [release].version")
    if policy != "independent":
        raise RuntimeError("release-crates.toml policy must be 'independent'")
    if set(crates) != set(PUBLISH_ORDER):
        raise RuntimeError(
            "release-crates.toml crates are not in sync with PUBLISH_ORDER: "
            f"expected {tuple(sorted(PUBLISH_ORDER))}, actual {tuple(sorted(crates))}"
        )
    parse_version(version)
    for package_name, entry in crates.items():
        validate_plan_entry(package_name, entry)
    return {"version": version, "crates": crates}


def validate_plan_entry(package_name: str, entry: dict) -> None:
    previous = entry.get("previous_version")
    version = entry.get("version")
    change = entry.get("change")
    publish = entry.get("publish")
    reason = entry.get("reason")
    if not all(isinstance(value, str) for value in (previous, version, change, reason)):
        raise RuntimeError(f"{package_name} has incomplete release plan metadata")
    if change not in CHANGE_KINDS:
        raise RuntimeError(f"{package_name} has invalid change kind {change!r}")
    if not isinstance(publish, bool):
        raise RuntimeError(f"{package_name} publish must be true or false")
    if not reason.strip():
        raise RuntimeError(f"{package_name} release reason must not be empty")

    planned_version = parse_version(version)
    if change in ("unpublished", "initial"):
        if previous != "unpublished":
            raise RuntimeError(f"{package_name} {change} state needs previous_version unpublished")
        if change == "unpublished" and publish:
            raise RuntimeError(f"{package_name} is unpublished but publish is true")
        if change == "initial" and not publish:
            raise RuntimeError(f"{package_name} initial release but publish is false")
        return

    if previous == "unpublished":
        raise RuntimeError(f"{package_name} {change} state needs a published previous_version")
    previous_version = parse_version(previous)

    if change in ("code", "breaking"):
        if change == "breaking" and previous_version[0] > 0:
            expected = (previous_version[0] + 1, 0, 0)
        else:
            expected = (previous_version[0], previous_version[1] + 1, 0)
        label = "breaking changes" if change == "breaking" else "code changes"
        if planned_version != expected:
            expected_text = ".".join(str(part) for part in expected)
            raise RuntimeError(
                f"{package_name} {label} require independent version {expected_text}"
            )
        if not publish:
            raise RuntimeError(f"{package_name} has {label} but publish is false")
    elif change in ("fix", "dependency", "metadata"):
        expected = (previous_version[0], previous_version[1], previous_version[2] + 1)
        if planned_version != expected:
            raise RuntimeError(f"{package_name} {change} changes require the next patch version")
        if not publish:
            raise RuntimeError(f"{package_name} has {change} changes but publish is false")
    else:
        if planned_version != previous_version:
            raise RuntimeError(
                f"{package_name} is unchanged but version differs from previous_version"
            )
        if publish:
            raise RuntimeError(f"{package_name} is unchanged but publish is true")


def verify_workspace(packages: dict[str, dict], plan: dict) -> None:
    expected = set(PUBLISH_ORDER) | set(PRIVATE_PACKAGES)
    if set(packages) != expected:
        raise RuntimeError(
            "release_crates.py package policy is not in sync with the workspace: "
            f"expected {tuple(sorted(expected))}, actual {tuple(sorted(packages))}"
        )

    for package_name in PRIVATE_PACKAGES:
        if packages[package_name].get("publish") != []:
            raise RuntimeError(f"private package {package_name} must set publish = false")

    seen: set[str] = set()
    for package_name in PUBLISH_ORDER:
        package = packages[package_name]
        if package.get("publish") == []:
            raise RuntimeError(f"reusable package {package_name} unexpectedly disables publishing")
        planned_version = plan["crates"][package_name]["version"]
        if package["version"] != planned_version:
            raise RuntimeError(
                f"{package_name} is version {package['version']}, expected {planned_version}"
            )
        for dependency in package["dependencies"]:
            dependency_name = dependency["name"]
            if dependency_name in PUBLISH_ORDER and dependency_name not in seen:
                raise RuntimeError(
                    f"{package_name} depends on {dependency_name}, but "
                    f"{dependency_name} appears later in PUBLISH_ORDER"
                )
        seen.add(package_name)


def require_clean_tree(*, dry_run: bool) -> None:
    if dry_run:
        return
    status = capture(["git", "status", "--porcelain"])
    if status:
        print("Refusing to publish from a dirty worktree:", file=sys.stderr)
        print(status, file=sys.stderr)
        print("Commit or stash changes before publishing.", file=sys.stderr)
        raise SystemExit(1)


def check_release_tag(version: str, *, dry_run: bool) -> None:
    tag = f"v{version}"
    head = try_capture(["git", "rev-parse", "HEAD"])
    tagged_commit = try_capture(["git", "rev-list", "-n", "1", tag])
    if head is None or tagged_commit is None:
        message = f"release tag {tag!r} was not found"
    elif head != tagged_commit:
        message = f"HEAD is not tagged as {tag} (HEAD {head}, {tag} {tagged_commit})"
    else:
        print(f"Release tag {tag} points at HEAD.")
        return
    if not dry_run:
        print(f"Refusing to publish: {message}.", file=sys.stderr)
        raise SystemExit(1)
    print(f"Warning: {message}.", file=sys.stderr)


def run_preflight(args: argparse.Namespace) -> None:
    release = parse_version(args.version)
    gate = ROOT / "scripts" / f"release_{release[0]}_{release[1]}_gate.sh"
    run([str(gate.relative_to(ROOT))] if gate.exists() else ["scripts/checks.sh"], dry_run=args.dry_run)
    run(["scripts/check-rust-version-matrix.sh"], dry_run=args.dry_run)
    run(["cargo", "deny", "check"], dry_run=args.dry_run)
    run(["cargo", "audit"], dry_run=args.dry_run)


def publish_plan(plan: dict) -> tuple[str, ...]:
    return tuple(
        package for package in PUBLISH_ORDER if plan["crates"][package]["publish"]
    )


def selected_steps(start_at: str, steps: tuple[str, ...]) -> tuple[str, ...]:
    if not steps:
        return ()
    try:
        return steps[steps.index(start_at) :]
    except ValueError as exc:
        raise RuntimeError(f"unknown selected package for --start-at: {start_at}") from exc


def publish(package: str, args: argparse.Namespace) -> None:
    command = ["cargo", "publish", "-p", package]
    if args.no_verify:
        command.append("--no-verify")
    run(command, dry_run=args.dry_run)


def wait_for_index(package: str, version: str, *, dry_run: bool) -> None:
    print(f"Published {package} {version}.")
    print(f"Wait until crates.io shows: https://crates.io/crates/{package}/{version}")
    if dry_run:
        print("[dry-run] skipping wait")
        return
    input("Press Enter after crates.io indexes the package: ")
    time.sleep(5)


def confirm_no_verify(args: argparse.Namespace) -> bool:
    if not args.no_verify or args.dry_run:
        return True
    print(
        "WARNING: --no-verify bypasses cargo package verification.\n"
        "Type 'no-verify confirmed' to continue:",
        file=sys.stderr,
    )
    return input().strip() == "no-verify confirmed"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Publish Gjallarbru reusable crates in crates.io order."
    )
    parser.add_argument("--version", default=None, help="Expected server release version.")
    parser.add_argument("--plan", default=str(DEFAULT_PLAN), help="Per-crate release plan.")
    parser.add_argument("--start-at", choices=PUBLISH_ORDER, default=None)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-verify", action="store_true")
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()

    raw_plan_path = Path(args.plan)
    plan_path = raw_plan_path if raw_plan_path.is_absolute() else (ROOT / raw_plan_path).resolve()
    plan = release_plan(plan_path)
    if args.version is None:
        args.version = plan["version"]
    elif args.version != plan["version"]:
        print(
            f"Refusing to publish: --version {args.version} does not match "
            f"{plan_path.name} release {plan['version']}.",
            file=sys.stderr,
        )
        return 1

    verify_workspace(workspace_packages(cargo_metadata()), plan)
    if args.check:
        print("release_crates.py package policy and publish order are up to date.")
        print(f"release_crates.py server release plan is {args.version}.")
        return 0

    require_clean_tree(dry_run=args.dry_run)
    check_release_tag(args.version, dry_run=args.dry_run)
    planned = publish_plan(plan)
    start_at = args.start_at or (planned[0] if planned else "")
    steps = selected_steps(start_at, planned)

    print(f"Server release: {args.version}")
    print("Publish sequence:")
    for package in steps:
        entry = plan["crates"][package]
        print(f"  - {package} {entry['version']} ({entry['change']})")
    if not steps:
        print("  - no crates selected for publishing")

    if not args.yes and input("Type the server release version to continue: ").strip() != args.version:
        print("Version confirmation did not match; aborting.", file=sys.stderr)
        return 1
    if not confirm_no_verify(args):
        print("No-verify confirmation did not match; aborting.", file=sys.stderr)
        return 1

    run_preflight(args)
    for index, package in enumerate(steps):
        publish(package, args)
        if index + 1 < len(steps):
            wait_for_index(package, plan["crates"][package]["version"], dry_run=args.dry_run)

    print("Release publish sequence completed.")
    for package in steps:
        print(f"Verify: cargo info {package}@{plan['crates'][package]['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
