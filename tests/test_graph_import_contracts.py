"""Validate proposed graph commands against Draft 2020-12, without runtime claims."""

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "contracts/qascp-2/graph"


class GraphImportContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.examples = json.loads(
            (ROOT / "tests/fixtures/graph-import-examples.json").read_text(encoding="utf-8")
        )["examples"]
        cls.validators = {}
        checker = FormatChecker()
        if "date-time" not in checker.checkers or "uuid" not in checker.checkers:
            raise RuntimeError("Required format checkers are unavailable")
        for name in ["resource-import.schema.json", "relationship-import.schema.json"]:
            schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            cls.validators[name] = Draft202012Validator(schema, format_checker=checker)

    def assert_rejected(self, schema_name, command):
        self.assertTrue(list(self.validators[schema_name].iter_errors(command)))

    def test_all_json_schema_documents_pass_meta_schema_validation(self):
        paths = list((ROOT / "contracts").rglob("*.schema.json"))
        self.assertGreaterEqual(len(paths), 10)
        for path in paths:
            with self.subTest(schema=path.name):
                Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))

    def test_synthetic_commands_and_resource_update_are_valid(self):
        self.assertEqual(len(self.examples), 9)
        for example in self.examples:
            with self.subTest(example=example["name"]):
                self.validators[example["schema"]].validate(example["command"])
        update = copy.deepcopy(self.examples[0]["command"])
        update.update(operation="update", expected_version=1, command_id="update-assistant")
        self.validators["resource-import.schema.json"].validate(update)

    def test_missing_required_fields_fail(self):
        for example in self.examples[:5]:
            schema = self.validators[example["schema"]].schema
            for field in schema["required"]:
                with self.subTest(example=example["name"], field=field):
                    changed = copy.deepcopy(example["command"])
                    del changed[field]
                    self.assert_rejected(example["schema"], changed)

    def test_client_tenant_unknown_fields_and_secrets_fail(self):
        for example in self.examples[:5]:
            for field in ["tenant_id", "authorization_version", "token", "trusted"]:
                with self.subTest(example=example["name"], field=field):
                    changed = copy.deepcopy(example["command"])
                    changed[field] = "caller-controlled"
                    self.assert_rejected(example["schema"], changed)
        changed = copy.deepcopy(self.examples[0]["command"])
        changed["resource"]["tenant_id"] = "tenant-b"
        self.assert_rejected("resource-import.schema.json", changed)

    def test_bad_version_ids_times_and_empty_source_fail(self):
        for field, value in [
            ("schema_version", "1.0"), ("connector_id", "invalid-uuid"),
            ("observed_at", "2026-02-30T10:00:00Z"),
            ("observed_at", "2026-11-15T10:00:00+03:00"),
            ("command_id", ""), ("command_id", "   "), ("command_id", "x" * 257),
            ("evidence_event_id", ""),
        ]:
            with self.subTest(field=field, value=value):
                changed = copy.deepcopy(self.examples[0]["command"])
                changed[field] = value
                self.assert_rejected("resource-import.schema.json", changed)

    def test_resource_union_and_phase_limits_fail_closed(self):
        changed = copy.deepcopy(self.examples[0]["command"])
        changed["resource"]["resource_kind"] = "ai_system"
        self.assert_rejected("resource-import.schema.json", changed)
        changed = copy.deepcopy(self.examples[2]["command"])
        changed["resource"]["asset_kind"] = "database"
        self.assert_rejected("resource-import.schema.json", changed)
        for value in ["", "safe", None]:
            changed = copy.deepcopy(self.examples[0]["command"])
            changed["resource"]["criticality"] = value
            self.assert_rejected("resource-import.schema.json", changed)

    def test_expected_version_is_bound_to_mutation_operation(self):
        for operation, version in [("create", 1), ("update", None), ("update", 0),
                                   ("update", -1), ("update", True)]:
            changed = copy.deepcopy(self.examples[0]["command"])
            changed["operation"] = operation
            if version is not None:
                changed["expected_version"] = version
            self.assert_rejected("resource-import.schema.json", changed)
        for operation, version in [("assert", 1), ("correct", None), ("retract", None),
                                   ("correct", 0), ("retract", True)]:
            changed = copy.deepcopy(self.examples[4]["command"])
            changed["operation"] = operation
            if version is not None:
                changed["expected_version"] = version
            self.assert_rejected("relationship-import.schema.json", changed)

    def test_wrong_relation_endpoint_pairs_fail(self):
        expected = {"owns": ("identity", "asset"), "runs_as": ("asset", "identity"),
                    "accesses": ("identity", "asset")}
        for relation, valid_pair in expected.items():
            for src in ["asset", "identity"]:
                for dst in ["asset", "identity"]:
                    if (src, dst) == valid_pair:
                        continue
                    with self.subTest(relation=relation, source=src, target=dst):
                        changed = copy.deepcopy(self.examples[4]["command"])
                        changed.update(relation=relation)
                        if relation != "accesses":
                            changed.pop("qualifier", None)
                        changed["source"]["resource_kind"] = src
                        changed["target"]["resource_kind"] = dst
                        self.assert_rejected("relationship-import.schema.json", changed)

    def test_access_qualifier_is_required_and_cannot_be_misapplied(self):
        changed = copy.deepcopy(self.examples[4]["command"])
        del changed["qualifier"]
        self.assert_rejected("relationship-import.schema.json", changed)
        changed = copy.deepcopy(self.examples[3]["command"])
        changed["qualifier"] = "entitlement"
        self.assert_rejected("relationship-import.schema.json", changed)
        changed = copy.deepcopy(self.examples[4]["command"])
        changed["qualifier"] = "compromised"
        self.assert_rejected("relationship-import.schema.json", changed)

    def test_future_relations_and_cross_source_selectors_fail(self):
        for relation in ["supports", "affects", "observed_on", "executes"]:
            changed = copy.deepcopy(self.examples[4]["command"])
            changed["relation"] = relation
            self.assert_rejected("relationship-import.schema.json", changed)
        for field in ["connector_id", "tenant_id", "canonical_id"]:
            changed = copy.deepcopy(self.examples[4]["command"])
            changed["source"][field] = "untrusted-selector"
            self.assert_rejected("relationship-import.schema.json", changed)


if __name__ == "__main__":
    unittest.main()
