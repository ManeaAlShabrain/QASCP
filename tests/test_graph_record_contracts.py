"""Static graph-record and fixture-oracle regressions, not runtime isolation tests."""

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

from scripts.verify_graph_record_fixtures import (
    receipt_key, validate_fixture_set, visible_fixture_version,
)

ROOT = Path(__file__).resolve().parents[1]


class GraphRecordContractTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            (ROOT / "tests/fixtures/graph-record-examples.json").read_text(encoding="utf-8")
        )

    def test_valid_record_set(self):
        self.assertEqual(validate_fixture_set(self.data),
                         {"receipts": 4, "claims": 3, "transitions": 3})

    def test_event_and_consumer_version_distinguish_keys_but_replica_does_not(self):
        first, other_event, replica, next_version = self.data["receipts"]
        self.assertNotEqual(receipt_key(first), receipt_key(other_event))
        self.assertEqual(receipt_key(first), receipt_key(replica))
        self.assertNotEqual(receipt_key(first), receipt_key(next_version))

    def test_two_processed_effects_for_one_key_fail(self):
        replay = copy.deepcopy(self.data["receipts"][0])
        replay.update(receipt_id="00000000-0000-4000-8000-000000000999",
                      consumer_workload_id="another-worker")
        self.data["receipts"].append(replay)
        with self.assertRaisesRegex(ValueError, "Duplicate processed effect"):
            validate_fixture_set(self.data)

    def test_duplicate_cannot_reference_another_event_or_tenant(self):
        for field, value in [("event_id", self.data["receipts"][1]["event_id"]),
                             ("tenant_id", "00000000-0000-4000-8000-000000000999")]:
            data = copy.deepcopy(self.data)
            data["receipts"][2][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(
                    ValueError, "Invalid duplicate receipt reference"):
                validate_fixture_set(data)

    def test_required_duplicate_reference_and_failure_reason(self):
        data = copy.deepcopy(self.data)
        del data["receipts"][2]["duplicate_of_receipt_id"]
        with self.assertRaises(ValidationError):
            validate_fixture_set(data)
        self.data["receipts"][0]["outcome"] = "failed"
        with self.assertRaises(ValidationError):
            validate_fixture_set(self.data)

    def test_expected_version_and_increment_cannot_conflict(self):
        for field, value in [("expected_version", 2), ("new_version", 7),
                             ("prior_version", 7)]:
            data = copy.deepcopy(self.data)
            data["transitions"][1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_fixture_set(data)

    def test_claim_endpoint_or_source_cannot_change_in_lineage(self):
        for field, value in [
            ("connector_id", "00000000-0000-4000-8000-000000000999"),
            ("source_claim_id", "other-source-claim"),
            ("source", {"kind": "identity", "id": "00000000-0000-4000-8000-000000000999"}),
            ("qualifier", "observed_use"),
        ]:
            data = copy.deepcopy(self.data)
            data["claims"][1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_fixture_set(data)

    def test_cross_tenant_claim_version_is_not_a_valid_transition_target(self):
        self.data["claims"][1]["tenant_id"] = "00000000-0000-4000-8000-000000000999"
        with self.assertRaisesRegex(ValueError, "same-tenant"):
            validate_fixture_set(self.data)

    def test_source_interval_and_knowledge_order(self):
        data = copy.deepcopy(self.data)
        data["claims"][1]["valid_to"] = data["claims"][1]["valid_from"]
        with self.assertRaisesRegex(ValueError, "Invalid source-valid interval"):
            validate_fixture_set(data)
        self.data["claims"][1]["recorded_at"] = "2026-11-16T09:59:00Z"
        self.data["transitions"][1]["recorded_at"] = "2026-11-16T09:59:00Z"
        with self.assertRaisesRegex(ValueError, "backwards"):
            validate_fixture_set(self.data)

    def test_late_correction_does_not_rewrite_prior_known_view(self):
        claim = self.data["claims"][0]
        args = (self.data, claim["tenant_id"], claim["claim_id"])
        self.assertEqual(visible_fixture_version(
            *args, "2026-11-16T09:30:00Z", "2026-11-16T10:30:00Z"), 1)
        self.assertEqual(visible_fixture_version(
            *args, "2026-11-16T09:30:00Z", "2026-11-16T11:30:00Z"), 2)
        self.assertIsNone(visible_fixture_version(
            *args, "2026-11-16T08:55:00Z", "2026-11-16T10:30:00Z"))
        self.assertEqual(visible_fixture_version(
            *args, "2026-11-16T08:55:00Z", "2026-11-16T11:30:00Z"), 2)

    def test_retraction_and_half_open_interval(self):
        claim = self.data["claims"][0]
        args = (self.data, claim["tenant_id"], claim["claim_id"])
        self.assertIsNone(visible_fixture_version(
            *args, "2026-11-16T09:30:00Z", "2026-11-16T12:30:00Z"))
        self.data["claims"][1]["valid_to"] = "2026-11-16T10:00:00Z"
        self.assertIsNone(visible_fixture_version(
            *args, "2026-11-16T10:00:00Z", "2026-11-16T11:30:00Z"))

    def test_orphan_and_duplicate_record_ids_fail(self):
        for field in ["receipts", "claims", "transitions"]:
            data = copy.deepcopy(self.data)
            data[field].append(copy.deepcopy(data[field][0]))
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_fixture_set(data)
        self.data["transitions"].pop()
        with self.assertRaisesRegex(ValueError, "Orphan"):
            validate_fixture_set(self.data)

    def test_internal_schema_version_and_unrecognized_fields_fail(self):
        for key, name in [
            ("receipts", "consumer-receipt-v2.schema.json"),
            ("claims", "claim-version.schema.json"),
            ("transitions", "claim-transition.schema.json"),
        ]:
            schema = json.loads((ROOT / "contracts/qascp-2/graph" / name).read_text())
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
            changed = copy.deepcopy(self.data[key][0])
            changed["model_authorized"] = True
            with self.subTest(key=key), self.assertRaises(ValidationError):
                validator.validate(changed)

    def test_retracted_lineage_cannot_be_resurrected(self):
        claim = copy.deepcopy(self.data["claims"][-1])
        claim.update(version=4, recorded_at="2026-11-16T13:00:00Z")
        transition = copy.deepcopy(self.data["transitions"][-1])
        transition.update(transition_id="00000000-0000-4000-8000-000000000999",
                          operation="correct", expected_version=3, prior_version=3,
                          new_version=4, recorded_at="2026-11-16T13:00:00Z")
        self.data["claims"].append(claim)
        self.data["transitions"].append(transition)
        with self.assertRaisesRegex(ValueError, "discontinuous"):
            validate_fixture_set(self.data)

    def test_non_synthetic_input_is_refused(self):
        self.data["synthetic"] = False
        with self.assertRaisesRegex(ValueError, "synthetic"):
            validate_fixture_set(self.data)

    def test_source_claim_identity_cannot_create_two_lineages(self):
        claim = copy.deepcopy(self.data["claims"][0])
        transition = copy.deepcopy(self.data["transitions"][0])
        claim["claim_id"] = "00000000-0000-4000-8000-000000000999"
        transition.update(claim_id=claim["claim_id"],
                          transition_id="00000000-0000-4000-8000-000000000998")
        self.data["claims"].append(claim)
        self.data["transitions"].append(transition)
        with self.assertRaisesRegex(ValueError, "multiple lineages"):
            validate_fixture_set(self.data)

    def test_same_source_claim_is_allowed_in_distinct_namespaces(self):
        for field in ("tenant_id", "connector_id"):
            data = copy.deepcopy(self.data)
            claim = copy.deepcopy(data["claims"][0])
            transition = copy.deepcopy(data["transitions"][0])
            value = "00000000-0000-4000-8000-000000000999"
            claim[field] = transition[field] = value
            claim["claim_id"] = "00000000-0000-4000-8000-000000000997"
            transition.update(claim_id=claim["claim_id"],
                              transition_id="00000000-0000-4000-8000-000000000998")
            data["claims"].append(claim)
            data["transitions"].append(transition)
            with self.subTest(namespace=field):
                self.assertEqual(validate_fixture_set(data)["claims"], 4)


if __name__ == "__main__":
    unittest.main()
