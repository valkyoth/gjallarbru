#!/usr/bin/env python3
"""Regression tests for locked Cargo and interpreter-aware tooling policy."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_locked_commands() -> None:
    checks = text("scripts/checks.sh")
    assert "cargo check --workspace --all-features --locked" in checks
    assert "cargo clippy --workspace --all-targets --all-features --locked" in checks
    assert "cargo test --workspace --all-features --locked" in checks

    matrix = text("scripts/check-rust-version-matrix.sh")
    assert "check --workspace --all-targets --all-features --locked" in matrix

    ci = text(".github/workflows/ci.yml")
    assert "check --workspace --all-targets --all-features --locked" in ci
    assert "cargo test --workspace --all-features --locked" in ci
    assert "cargo deny --locked check" in ci

    packages = text("scripts/check-packages.sh")
    assert "cargo package -p \"$package\" --locked --no-verify --list" in packages
    assert "--allow-dirty" not in packages
    assert "publishable package inputs are dirty" in packages

    metadata = text("scripts/validate-release-metadata.sh")
    assert "cargo metadata --locked --format-version 1 --no-deps" in metadata
    security = text("scripts/validate-security-policy.sh")
    assert "cargo tree --locked --workspace" in security

    release = text("scripts/release_crates.py")
    assert '["cargo", "metadata", "--locked"' in release
    assert '["cargo", "deny", "--locked", "check"]' in release
    assert '["cargo", "publish", "--locked", "-p", package]' in release
    assert release.count("require_clean_tree(dry_run=args.dry_run)") == 2

    gate = text("scripts/release_0_1_gate.sh")
    assert "cargo deny --locked check" in gate


def make_wrapper(path: Path, interpreter: str, real: str) -> None:
    path.write_text(
        "#!/bin/sh\n"
        f"printf '{interpreter} %s\\n' \"$2\" >>\"$SHELL_POLICY_LOG\"\n"
        f"exec {real} \"$@\"\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


def assert_shebang_dispatch() -> None:
    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        bin_dir = tmp / "bin"
        bin_dir.mkdir()
        log = tmp / "dispatch.log"
        bash_sample = tmp / "bash-sample.sh"
        sh_sample = tmp / "sh-sample.sh"
        bash_sample.write_text(
            "#!/usr/bin/env bash\nvalues=(one two)\n: \"${values[@]}\"\n",
            encoding="utf-8",
        )
        sh_sample.write_text("#!/usr/bin/env sh\nvalue=one\n: \"$value\"\n", encoding="utf-8")
        make_wrapper(bin_dir / "bash", "bash", "/bin/bash")
        make_wrapper(bin_dir / "sh", "sh", "/bin/sh")
        env = os.environ.copy()
        env["PATH"] = f"{bin_dir}:{env['PATH']}"
        env["SHELL_POLICY_LOG"] = str(log)
        subprocess.run(
            ["/bin/sh", "scripts/check_shell_syntax.sh", str(bash_sample), str(sh_sample)],
            cwd=ROOT,
            env=env,
            check=True,
        )
        actual = log.read_text(encoding="utf-8").splitlines()
        expected = [
            f"bash {bash_sample}",
            f"sh {sh_sample}",
        ]
        assert actual == expected, f"shell dispatch differs: {actual!r}"


def assert_dirty_package_rejected() -> None:
    probe = ROOT / "crates" / "gjallarbru-wire" / "src" / "lib.rs"
    original = probe.read_bytes()
    try:
        probe.write_bytes(original + b"\n// Uncommitted package-content probe.\n")
        result = subprocess.run(
            ["scripts/check-packages.sh"],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        assert result.returncode != 0, "dirty publishable crate unexpectedly packaged"
        assert "publishable package inputs are dirty" in result.stdout
    finally:
        probe.write_bytes(original)


def main() -> None:
    assert_locked_commands()
    assert_shebang_dispatch()
    assert_dirty_package_rejected()
    print("tooling policy tests passed")


if __name__ == "__main__":
    main()
