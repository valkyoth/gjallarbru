#!/usr/bin/env python3
"""Negative fixtures for the base requirement ledger and errata decisions."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


requirements = load_module("requirements_policy", ROOT / "scripts/requirements.py")
errata = load_module("errata_policy", ROOT / "scripts/rfc_errata.py")


def assert_fails(expected: str, function, value: dict) -> None:
    try:
        function(value)
    except (requirements.RequirementError, errata.ErrataError) as error:
        if expected not in str(error):
            raise AssertionError(f"expected {expected!r} in {error!r}") from error
        return
    raise AssertionError(f"expected failure containing {expected!r}")


def load_ledger() -> dict:
    return json.loads(requirements.OUTPUT.read_text(encoding="utf-8"))


def load_errata() -> dict:
    return json.loads(errata.OUTPUT.read_text(encoding="utf-8"))


def test_generated_ledger_matches_sources() -> None:
    actual = load_ledger()
    expected = requirements.build_ledger()
    requirements.validate(actual)
    assert requirements.render(actual) == requirements.render(expected)
    assert {document["rfc"] for document in actual["documents"]} == {8489, 8656}
    assert len(actual["sections"]) >= 180
    assert len(actual["requirements"]) >= 390
    by_line = {(item["rfc"], item["line"], item["level"]) for item in actual["requirements"]}
    assert (8656, 1288, "MUST NOT") in by_line
    assert (8656, 1288, "MUST") not in by_line
    assert (8656, 1290, "MUST NOT") in by_line
    assert (8656, 1290, "MUST") not in by_line
    assert (8489, 810, "MUST NOT") in by_line


def test_schema_names_every_contract_field() -> None:
    schema = json.loads(requirements.SCHEMA.read_text(encoding="utf-8"))
    item = schema["properties"]["requirements"]["items"]
    assert set(item["required"]) == {
        "id",
        "rfc",
        "section",
        "line",
        "level",
        "profile",
        "component",
        "symbol",
        "test",
        "status",
        "security",
        "source_sha256",
    }
    assert item["additionalProperties"] is False


def test_missing_field_rejected() -> None:
    ledger = load_ledger()
    del ledger["requirements"][0]["security"]
    assert_fails("fields differ", requirements.validate, ledger)


def test_duplicate_requirement_rejected() -> None:
    ledger = load_ledger()
    duplicate = copy.deepcopy(ledger["requirements"][0])
    ledger["requirements"].append(duplicate)
    assert_fails("duplicate", requirements.validate, ledger)


def test_invalid_level_rejected() -> None:
    ledger = load_ledger()
    ledger["requirements"][0]["level"] = "ALWAYS"
    assert_fails("invalid RFC or level", requirements.validate, ledger)


def test_unassigned_reference_rejected() -> None:
    ledger = load_ledger()
    ledger["requirements"][0]["symbol"] = "unassigned"
    assert_fails("unassigned symbol", requirements.validate, ledger)


def test_complete_without_evidence_rejected() -> None:
    ledger = load_ledger()
    ledger["requirements"][0]["status"] = "verified"
    assert_fails("complete without implementation evidence", requirements.validate, ledger)


def test_unknown_milestone_rejected() -> None:
    ledger = load_ledger()
    ledger["requirements"][0]["symbol"] = "planned:v9.9.9"
    ledger["requirements"][0]["test"] = "planned:v9.9.9"
    assert_fails("unknown milestone", requirements.validate, ledger)


def test_exclusion_without_evidence_rejected() -> None:
    ledger = load_ledger()
    ledger["requirements"][0]["status"] = "excluded"
    assert_fails("excluded without reviewed evidence", requirements.validate, ledger)


def test_missing_and_duplicate_section_rejected() -> None:
    missing = load_ledger()
    removed = missing["sections"].pop(4)
    assert removed["requirements"]
    assert_fails("orphaned", requirements.validate, missing)

    duplicate = load_ledger()
    duplicate["sections"].append(copy.deepcopy(duplicate["sections"][0]))
    assert_fails("duplicate or invalid section", requirements.validate, duplicate)


def test_errata_decisions_and_negative_fixtures() -> None:
    snapshot = load_errata()
    errata.validate(snapshot)
    assert len(snapshot["errata"]) == 6

    duplicate = copy.deepcopy(snapshot)
    duplicate["errata"].append(copy.deepcopy(duplicate["errata"][0]))
    assert_fails("duplicate", errata.validate, duplicate)

    invalid = copy.deepcopy(snapshot)
    invalid["errata"][0]["status"] = "Unknown"
    assert_fails("invalid RFC or status", errata.validate, invalid)

    invalid_rfc = copy.deepcopy(snapshot)
    invalid_rfc["errata"][0]["rfc"] = "8489"
    assert_fails("invalid RFC or status", errata.validate, invalid_rfc)

    unassigned = copy.deepcopy(snapshot)
    unassigned["errata"][0]["implementation"] = "unassigned"
    assert_fails("unassigned implementation", errata.validate, unassigned)

    unapplied = copy.deepcopy(snapshot)
    unapplied["errata"][0]["disposition"] = "track-not-applied"
    assert_fails("is not applied", errata.validate, unapplied)

    premature = copy.deepcopy(snapshot)
    reported = next(item for item in premature["errata"] if item["status"] == "Reported")
    reported["disposition"] = "apply"
    assert_fails("unverified erratum", errata.validate, premature)


def main() -> None:
    tests = [
        test_generated_ledger_matches_sources,
        test_schema_names_every_contract_field,
        test_missing_field_rejected,
        test_duplicate_requirement_rejected,
        test_invalid_level_rejected,
        test_unassigned_reference_rejected,
        test_complete_without_evidence_rejected,
        test_unknown_milestone_rejected,
        test_exclusion_without_evidence_rejected,
        test_missing_and_duplicate_section_rejected,
        test_errata_decisions_and_negative_fixtures,
    ]
    for test in tests:
        test()
    print(f"requirement ledger tests passed ({len(tests)} tests)")


if __name__ == "__main__":
    main()
