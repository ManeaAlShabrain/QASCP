"""P1 fixture-only conformance oracle; no service, DB, authorization or executor."""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("tenant_id", "event_id", "logical_consumer_id", "consumer_version",
          "purpose", "input_version")


def receipt_key(record):
    """Return the documented logical identity, independent of worker replica."""
    return tuple(record[field] for field in FIELDS)


def instant(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_fixture_set(data):
    """Reject schema/lineage contradictions in an explicitly synthetic fixture."""
    if data.get("synthetic") is not True or data.get("fixture_version") != "0.1":
        raise ValueError("Only versioned synthetic fixtures are supported")
    checker = FormatChecker()
    for field, filename in (
        ("receipts", "consumer-receipt-v2.schema.json"),
        ("claims", "claim-version.schema.json"),
        ("transitions", "claim-transition.schema.json"),
    ):
        schema = json.loads(
            (ROOT / "contracts/qascp-2/graph" / filename).read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=checker)
        for record in data[field]:
            validator.validate(record)

    receipt_ids, processed = {}, set()
    for record in data["receipts"]:
        rid = (record["tenant_id"], record["receipt_id"])
        if rid in receipt_ids:
            raise ValueError("Duplicate receipt ID")
        key = receipt_key(record)
        if record["outcome"] == "processed":
            if key in processed:
                raise ValueError("Duplicate processed effect")
            processed.add(key)
        elif record["outcome"] == "duplicate":
            prior = receipt_ids.get(
                (record["tenant_id"], record["duplicate_of_receipt_id"])
            )
            if (prior is None or prior["outcome"] != "processed"
                    or receipt_key(prior) != key
                    or instant(record["recorded_at"]) < instant(prior["recorded_at"])):
                raise ValueError("Invalid duplicate receipt reference")
        receipt_ids[rid] = record

    versions, lineages, transition_ids = {}, defaultdict(list), set()
    for claim in data["claims"]:
        key = (claim["tenant_id"], claim["claim_id"], claim["version"])
        if key in versions:
            raise ValueError("Duplicate claim version")
        if ("valid_to" in claim
                and instant(claim["valid_to"]) <= instant(claim["valid_from"])):
            raise ValueError("Invalid source-valid interval")
        versions[key] = claim

    for transition in data["transitions"]:
        tid = (transition["tenant_id"], transition["transition_id"])
        if tid in transition_ids:
            raise ValueError("Duplicate transition ID")
        transition_ids.add(tid)
        lineages[(transition["tenant_id"], transition["claim_id"])].append(transition)

    consumed_versions = set()
    immutable = ("connector_id", "source_claim_id", "source", "target", "relation", "qualifier")
    for scope, transitions in lineages.items():
        previous, last_time, retracted, first = 0, None, False, None
        for transition in sorted(transitions, key=lambda item: item["new_version"]):
            new = transition["new_version"]
            if (retracted or transition["expected_version"] != previous
                    or new != previous + 1):
                raise ValueError("Stale or discontinuous transition")
            if previous == 0:
                if transition["operation"] != "assert":
                    raise ValueError("Lineage must begin with assert")
            elif (transition["operation"] == "assert"
                  or transition["prior_version"] != previous):
                raise ValueError("Invalid prior-version lineage")
            key = (*scope, new)
            claim = versions.get(key)
            if claim is None:
                raise ValueError("Transition has no same-tenant claim version")
            if (claim["connector_id"] != transition["connector_id"]
                    or claim["recorded_at"] != transition["recorded_at"]):
                raise ValueError("Transition provenance mismatch")
            if first is None:
                first = claim
            elif any(claim.get(field) != first.get(field) for field in immutable):
                raise ValueError("Immutable claim lineage changed")
            now = instant(transition["recorded_at"])
            if last_time is not None and now < last_time:
                raise ValueError("Knowledge time moved backwards")
            last_time, previous = now, new
            retracted = transition["operation"] == "retract"
            consumed_versions.add(key)
    if set(versions) != consumed_versions:
        raise ValueError("Orphan claim versions")
    return {"receipts": len(receipt_ids), "claims": len(versions),
            "transitions": len(transition_ids)}


def visible_fixture_version(data, tenant_id, claim_id, valid_at, known_at):
    """Demonstrate dual-time expectations on synthetic data, without access policy."""
    validate_fixture_set(data)
    visible = [item for item in data["transitions"]
               if item["tenant_id"] == tenant_id and item["claim_id"] == claim_id
               and instant(item["recorded_at"]) <= instant(known_at)]
    if not visible:
        return None
    latest = max(visible, key=lambda item: item["new_version"])
    if latest["operation"] == "retract":
        return None
    claim = next(item for item in data["claims"]
                 if item["tenant_id"] == tenant_id and item["claim_id"] == claim_id
                 and item["version"] == latest["new_version"])
    if instant(valid_at) < instant(claim["valid_from"]):
        return None
    if "valid_to" in claim and instant(valid_at) >= instant(claim["valid_to"]):
        return None
    return claim["version"]


if __name__ == "__main__":
    fixture = ROOT / "tests/fixtures/graph-record-examples.json"
    print(json.dumps(validate_fixture_set(json.loads(fixture.read_text(encoding="utf-8")))))
