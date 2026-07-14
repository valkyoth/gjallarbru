#!/usr/bin/env python3
"""Tests for Gjallarbru's independent crate-release policy."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release_crates.py"


def load_release_crates():
    spec = importlib.util.spec_from_file_location("release_crates", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load release_crates.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


release_crates = load_release_crates()


def entry(
    *,
    previous: str = "unpublished",
    version: str = "0.1.0",
    change: str = "unpublished",
    publish: bool = False,
) -> dict:
    return {
        "previous_version": previous,
        "version": version,
        "change": change,
        "publish": publish,
        "reason": "test reason",
    }


def package(
    name: str,
    version: str = "0.1.0",
    dependencies: tuple[str, ...] = (),
    publish=None,
) -> dict:
    return {
        "name": name,
        "version": version,
        "dependencies": [{"name": dependency} for dependency in dependencies],
        "publish": publish,
    }


def base_plan() -> dict:
    return {
        "version": "0.1.0",
        "crates": {name: entry() for name in release_crates.PUBLISH_ORDER},
    }


def base_packages() -> dict[str, dict]:
    packages = {
        "gjallarbru-wire": package("gjallarbru-wire"),
        "gjallarbru-crypto": package("gjallarbru-crypto"),
        "gjallarbru-core": package(
            "gjallarbru-core",
            dependencies=("gjallarbru-wire", "gjallarbru-crypto"),
        ),
        "gjallarbru-runtime": package("gjallarbru-runtime", publish=[]),
        "gjallarbru-server": package("gjallarbru-server", publish=[]),
    }
    return packages


def assert_fails(expected: str, function, *args) -> None:
    try:
        function(*args)
    except RuntimeError as error:
        if expected not in str(error):
            raise AssertionError(f"expected {expected!r} in {error!r}") from error
        return
    raise AssertionError("expected failure")


def test_current_unpublished_plan_is_valid() -> None:
    plan = release_crates.release_plan(release_crates.DEFAULT_PLAN)
    release_crates.verify_workspace(base_packages(), plan)


def test_unpublished_crate_cannot_be_selected() -> None:
    planned = entry(publish=True)
    assert_fails(
        "unpublished but publish is true",
        release_crates.validate_plan_entry,
        "gjallarbru-wire",
        planned,
    )


def test_initial_release_must_be_selected() -> None:
    planned = entry(change="initial")
    assert_fails(
        "initial release but publish is false",
        release_crates.validate_plan_entry,
        "gjallarbru-wire",
        planned,
    )


def test_code_change_uses_next_independent_minor() -> None:
    planned = entry(
        previous="0.3.2",
        version="0.4.0",
        change="code",
        publish=True,
    )
    release_crates.validate_plan_entry("gjallarbru-wire", planned)
    planned["version"] = "0.5.0"
    assert_fails(
        "independent version 0.4.0",
        release_crates.validate_plan_entry,
        "gjallarbru-wire",
        planned,
    )


def test_dependency_change_uses_exact_next_patch() -> None:
    planned = entry(
        previous="0.3.2",
        version="0.3.3",
        change="dependency",
        publish=True,
    )
    release_crates.validate_plan_entry("gjallarbru-core", planned)
    planned["version"] = "0.3.4"
    assert_fails(
        "next patch version",
        release_crates.validate_plan_entry,
        "gjallarbru-core",
        planned,
    )


def test_fix_uses_exact_next_patch() -> None:
    planned = entry(
        previous="1.3.2",
        version="1.3.3",
        change="fix",
        publish=True,
    )
    release_crates.validate_plan_entry("gjallarbru-wire", planned)


def test_stable_breaking_change_uses_next_major() -> None:
    planned = entry(
        previous="1.3.2",
        version="2.0.0",
        change="breaking",
        publish=True,
    )
    release_crates.validate_plan_entry("gjallarbru-core", planned)
    planned["version"] = "1.4.0"
    assert_fails(
        "independent version 2.0.0",
        release_crates.validate_plan_entry,
        "gjallarbru-core",
        planned,
    )


def test_metadata_change_uses_exact_next_patch() -> None:
    planned = entry(
        previous="0.3.2",
        version="0.3.3",
        change="metadata",
        publish=True,
    )
    release_crates.validate_plan_entry("gjallarbru-crypto", planned)


def test_unchanged_crate_is_not_republished() -> None:
    planned = entry(
        previous="0.3.2",
        version="0.3.2",
        change="unchanged",
        publish=True,
    )
    assert_fails(
        "unchanged but publish is true",
        release_crates.validate_plan_entry,
        "gjallarbru-crypto",
        planned,
    )


def test_private_packages_must_disable_publication() -> None:
    packages = base_packages()
    packages["gjallarbru-runtime"]["publish"] = None
    assert_fails(
        "private package gjallarbru-runtime must set publish = false",
        release_crates.verify_workspace,
        packages,
        base_plan(),
    )


def test_dependency_order_is_enforced() -> None:
    packages = base_packages()
    packages["gjallarbru-wire"]["dependencies"] = [{"name": "gjallarbru-core"}]
    assert_fails(
        "appears later in PUBLISH_ORDER",
        release_crates.verify_workspace,
        packages,
        base_plan(),
    )


def test_publish_plan_skips_unpublished_and_unchanged() -> None:
    plan = base_plan()
    plan["crates"]["gjallarbru-wire"] = entry(change="initial", publish=True)
    assert release_crates.publish_plan(plan) == ("gjallarbru-wire",)


def run_tests() -> None:
    tests = (
        test_current_unpublished_plan_is_valid,
        test_unpublished_crate_cannot_be_selected,
        test_initial_release_must_be_selected,
        test_code_change_uses_next_independent_minor,
        test_dependency_change_uses_exact_next_patch,
        test_fix_uses_exact_next_patch,
        test_stable_breaking_change_uses_next_major,
        test_metadata_change_uses_exact_next_patch,
        test_unchanged_crate_is_not_republished,
        test_private_packages_must_disable_publication,
        test_dependency_order_is_enforced,
        test_publish_plan_skips_unpublished_and_unchanged,
    )
    for test in tests:
        test()
    print(f"release crate policy tests passed ({len(tests)} tests)")


if __name__ == "__main__":
    run_tests()
