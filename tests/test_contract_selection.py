"""Guard the deliberately incompatible first-runtime API selection and its custody."""

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ContractSelectionTests(unittest.TestCase):
    def test_original_and_successor_have_distinct_versioned_boundaries(self):
        original = json.loads((ROOT / "contracts/qascp-2/openapi.json").read_text(encoding="utf-8"))
        successor = json.loads((ROOT / "contracts/qascp-2/graph/openapi-0.2.json").read_text(encoding="utf-8"))
        self.assertEqual(original["servers"], [{"url": "/api/v1"}])
        self.assertEqual(successor["servers"], [{"url": "/api/v2"}])
        self.assertNotEqual(original["servers"], successor["servers"])
        self.assertEqual(original["info"]["version"], "0.1.0")
        self.assertEqual(successor["info"]["version"], "0.2.0")

    def test_command_acceptance_is_not_an_observation_receipt(self):
        api = json.loads((ROOT / "contracts/qascp-2/graph/openapi-0.2.json").read_text(encoding="utf-8"))
        for path in ("/imports/resources", "/imports/relationships"):
            for code in ("200", "201"):
                with self.subTest(path=path, code=code):
                    response = api["paths"][path]["post"]["responses"][code]
                    self.assertEqual(response["content"]["application/json"]["schema"]["$ref"],
                                     "#/components/schemas/CommandReceipt")
        response = api["paths"]["/observations"]["post"]["responses"]["201"]
        self.assertEqual(response["content"]["application/json"]["schema"]["$ref"],
                         "#/components/schemas/Receipt")

    def test_selection_covers_exact_contract_bytes_without_identity_rewrite(self):
        selection = json.loads((ROOT / "docs/architecture/P1_CONTRACT_SELECTION.json").read_text(encoding="utf-8"))
        rows = selection["contracts"]
        paths = [row["path"] for row in rows]
        actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "contracts/qascp-2").rglob("*.json")}
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(set(paths), actual)
        for row in rows:
            with self.subTest(path=row["path"]):
                path = ROOT / row["path"]
                self.assertTrue(path.resolve().is_relative_to(ROOT / "contracts/qascp-2"))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(schema.get("$id"), row["schema_id"])
        self.assertFalse(selection["runtime_delivered"])
        # Frozen original at merged main b66d73c..., before successor URL selection.
        self.assertEqual(hashlib.sha256((ROOT / "contracts/qascp-2/openapi.json").read_bytes()).hexdigest(),
                         "c352320cc5e8e27ed06adbe808976117cd3d6af364f4db788779db38e60ea335")


if __name__ == "__main__":
    unittest.main()
