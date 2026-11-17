"""Security-sensitive record type/outcome compatibility; no executor claim."""

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]


class ApprovalOutcomeContractTests(unittest.TestCase):
    def setUp(self):
        schema = json.loads((ROOT / "contracts/qascp-2/approval-lifecycle.schema.json").read_text(encoding="utf-8"))
        self.validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.record = {
            "schema_version": "1.0", "record_type": "execution_result",
            "tenant_id": "00000000-0000-4000-8000-000000000001",
            "proposal_id": "00000000-0000-4000-8000-000000000002",
            "proposal_version": 1, "action": "synthetic-action", "target_type": "asset",
            "target_id": "synthetic-target", "parameter_digest": "a" * 64,
            "occurred_at": "2026-11-17T10:00:00Z", "correlation_id": "synthetic-review",
            "decision_id": "00000000-0000-4000-8000-000000000003",
            "execution_id": "00000000-0000-4000-8000-000000000004",
            "executor_workload_id": "synthetic-executor",
            "idempotency_key": "synthetic-command", "remote_reference": "synthetic-result",
        }

    def test_outcomes_are_valid_for_their_lifecycle_stage(self):
        for kind, outcomes in (
            ("execution_result", ("succeeded", "failed", "partial", "indeterminate")),
            ("reconciliation", ("reconciled_succeeded", "reconciled_failed")),
        ):
            for outcome in outcomes:
                with self.subTest(kind=kind, outcome=outcome):
                    self.validator.validate({**self.record, "record_type": kind, "outcome": outcome})

    def test_outcome_from_another_lifecycle_stage_is_rejected(self):
        for kind, outcomes in (
            ("execution_result", ("reconciled_succeeded", "reconciled_failed")),
            ("reconciliation", ("succeeded", "failed", "partial", "indeterminate")),
        ):
            for outcome in outcomes:
                with self.subTest(kind=kind, outcome=outcome), self.assertRaises(ValidationError):
                    self.validator.validate({**self.record, "record_type": kind, "outcome": outcome})


if __name__ == "__main__":
    unittest.main()
