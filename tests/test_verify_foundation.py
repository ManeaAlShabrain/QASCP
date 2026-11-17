"""Fail-closed regression coverage for the P1 foundation verifier."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.verify_foundation import (
    HANDBOOKS, REGISTER, REQUIRED_FILES, ROOT, PRODUCT_BACKLOG,
    PRODUCT_REQUIREMENTS, strict_json_loads, verify_foundation,
)


class FoundationVerifierTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for relative_path in (*REQUIRED_FILES, "scripts/verify_foundation.py"):
            destination = self.root / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative_path, destination)

    def update(self, relative_path, old, new):
        path = self.root / relative_path
        content = path.read_text(encoding="utf-8")
        self.assertIn(old, content)
        path.write_text(content.replace(old, new, 1), encoding="utf-8")

    def assert_rejected(self, message):
        self.assertIn(message, "\n".join(verify_foundation(self.root)))

    def test_valid_repository(self):
        self.assertEqual(verify_foundation(self.root), [])

    def test_missing_product_documents_report_failure_without_traceback(self):
        for name in (PRODUCT_BACKLOG, PRODUCT_REQUIREMENTS):
            path = self.root / name
            original = path.read_bytes()
            for payload in (None, b"", b"\xff"):
                with self.subTest(name=name, payload=payload):
                    if payload is None:
                        path.unlink()
                    else:
                        path.write_bytes(payload)
                    result = subprocess.run(
                        [sys.executable, str(self.root / "scripts/verify_foundation.py")],
                        capture_output=True, text=True, check=False)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(name, result.stdout)
                    self.assertNotIn("Traceback", result.stderr)
                    path.write_bytes(original)

    def test_ambiguous_and_nonfinite_json_are_rejected(self):
        for payload in ('{"a":1,"a":2}', '{"nested":{"x":1,"x":2}}',
                        '{"n":NaN}', '{"n":Infinity}', '{"n":1e999}'):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                strict_json_loads(payload)
        self.assertEqual(strict_json_loads('{"a":1.5,"b":[true,null]}'),
                         {"a": 1.5, "b": [True, None]})

    def test_invalid_contract_json_is_rejected_by_foundation(self):
        name = "contracts/qascp-2/observation.schema.json"
        for payload in ('{"type":"object","type":"string"}', '{"x":NaN}', '{'):
            (self.root / name).write_text(payload, encoding="utf-8")
            self.assert_rejected(name + ": invalid JSON")

    def test_missing_language(self):
        (self.root / HANDBOOKS[1]).unlink()
        self.assert_rejected(f"Missing or out-of-scope file: {HANDBOOKS[1]}")

    def test_out_of_scope_symlink(self):
        path = self.root / HANDBOOKS[1]
        path.unlink()
        path.symlink_to(ROOT / HANDBOOKS[1])
        self.assert_rejected(f"Missing or out-of-scope file: {HANDBOOKS[1]}")

    def test_unreadable_utf8(self):
        (self.root / HANDBOOKS[1]).write_bytes(b"\xff")
        self.assert_rejected(f"Unreadable file: {HANDBOOKS[1]}")

    def test_one_edition_omits_requirement(self):
        self.update(HANDBOOKS[1], "### QASCP-GOV-001", "### UNCOVERED")
        self.assert_rejected(f"{HANDBOOKS[1]}: requirement IDs or order differ")

    def test_missing_requirement_body(self):
        self.update(HANDBOOKS[0], "Every work item MUST name", "### Every work item MUST name")
        self.assert_rejected(f"{HANDBOOKS[0]}: requirement IDs or order differ")

    def test_duplicate_requirement_in_register(self):
        path = self.root / REGISTER
        content = json.loads(path.read_text())
        content["requirements"].append(content["requirements"][0])
        path.write_text(json.dumps(content))
        self.assert_rejected("duplicate requirement IDs")

    def test_missing_product_requirement_in_register(self):
        path = self.root / REGISTER
        content = json.loads(path.read_text())
        content["product_requirements"].pop()
        path.write_text(json.dumps(content))
        self.assert_rejected("expected PRD-01 through PRD-10 once in order")

    def test_duplicate_product_requirement_in_register(self):
        path = self.root / REGISTER
        content = json.loads(path.read_text())
        content["product_requirements"].append(content["product_requirements"][0])
        path.write_text(json.dumps(content))
        self.assert_rejected("duplicate product requirement IDs")

    def test_invalid_product_requirement_references(self):
        path = self.root / REGISTER
        content = json.loads(path.read_text())
        content["product_requirements"][0]["phases"] = ["P7"]
        content["product_requirements"][0]["verification"] = ["P1-V99"]
        path.write_text(json.dumps(content))
        self.assert_rejected("PRD-01: invalid or unordered phase references")
        self.assert_rejected("PRD-01: unknown verification ID P1-V99")

    def test_broken_product_backlog_mapping(self):
        path = self.root / REGISTER
        content = json.loads(path.read_text())
        content["product_requirements"][0]["backlog"] = ["V2-P2-99"]
        path.write_text(json.dumps(content))
        self.assert_rejected("PRD-01: unknown backlog ID V2-P2-99")

    def test_mixed_versions(self):
        self.update(HANDBOOKS[1], "الإصدار 1.0", "الإصدار 1.1")
        self.assert_rejected(f"{HANDBOOKS[1]}: baseline version differs")

    def test_invalid_phase(self):
        self.update(HANDBOOKS[0], "| P4 —", "| P7 —")
        self.assert_rejected(f"{HANDBOOKS[0]}: expected P1 through P6 once in order")

    def test_invalid_json(self):
        (self.root / REGISTER).write_text("{")
        self.assert_rejected(f"{REGISTER}: invalid JSON")

    def test_unknown_evidence_reference(self):
        self.update(REGISTER, '"P1-V04"', '"P1-V99"')
        self.assert_rejected("unknown verification ID P1-V99")

    def test_missing_verification_list(self):
        self.update(REGISTER, '["P1-V04"]', "[]")
        self.assert_rejected("QASCP-GOV-001: expected nonempty verification IDs")

    def test_broken_link_blocks_cli(self):
        self.update("README.md", "](SECURITY.md)", "](missing.md)")
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts/verify_foundation.py")],
            cwd=self.root.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("README.md: unresolved local link missing.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
