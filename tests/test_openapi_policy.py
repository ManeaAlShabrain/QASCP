"""Exercise both preserved API policies without optional validator dependencies."""

import copy
import unittest
from unittest.mock import patch

from scripts import verify_openapi_contracts as contracts
from scripts.verify_foundation import strict_json_loads
from scripts.verify_openapi_policy import check_openapi_policy


class OpenAPIPolicyTests(unittest.TestCase):
    def setUp(self):
        self.specs = [
            strict_json_loads(path.read_text(encoding="utf-8"))
            for path in contracts.DOCUMENTS
        ]

    def test_both_preserved_contracts_keep_their_authorized_operations(self):
        for spec, count in zip(self.specs, (2, 4)):
            with self.subTest(version=spec["info"]["version"]):
                self.assertEqual(check_openapi_policy(spec), {"operations": count})

    def test_global_and_operation_security_cannot_be_disabled_on_either_version(self):
        for original in self.specs:
            for security in ([], [{}]):
                for location in ("global", "operation"):
                    spec = copy.deepcopy(original)
                    if location == "global":
                        spec["security"] = security
                    else:
                        spec["paths"]["/observations"]["post"]["security"] = security
                    with self.subTest(version=spec["info"]["version"],
                                      location=location, security=security):
                        with self.assertRaises(ValueError):
                            check_openapi_policy(spec)

    def test_scheme_and_tenant_definition_cannot_be_weakened_on_either_version(self):
        for original in self.specs:
            for mutation in ("scheme", "tenant", "path"):
                spec = copy.deepcopy(original)
                if mutation == "scheme":
                    spec["components"]["securitySchemes"]["oidcBearer"] = {
                        "type": "apiKey", "in": "query", "name": "token"}
                elif mutation == "tenant":
                    spec["components"]["parameters"]["TenantSelector"]["required"] = False
                else:
                    spec["paths"]["/observations"]["parameters"] = []
                with self.subTest(version=spec["info"]["version"], mutation=mutation):
                    with self.assertRaises(ValueError):
                        check_openapi_policy(spec)

    def test_every_http_method_and_aliased_tenant_override_is_checked_on_both(self):
        for original in self.specs:
            for method in ("get", "post", "put", "patch", "delete", "head", "options", "trace"):
                spec = copy.deepcopy(original)
                operation = copy.deepcopy(spec["paths"]["/observations"]["post"])
                operation.update(operationId="anonymousProbe", security=[])
                spec["paths"]["/observations"][method] = operation
                with self.subTest(version=spec["info"]["version"], method=method):
                    with self.assertRaisesRegex(ValueError, "Security override"):
                        check_openapi_policy(spec)
            spec = copy.deepcopy(original)
            override = copy.deepcopy(spec["components"]["parameters"]["TenantSelector"])
            override.update(name="x-tenant-id", required=False)
            spec["components"]["parameters"]["Alias"] = override
            spec["paths"]["/observations"]["post"]["parameters"] = [
                {"$ref": "#/components/parameters/Alias"}]
            with self.subTest(version=spec["info"]["version"], alias=True):
                with self.assertRaisesRegex(ValueError, "overrides"):
                    check_openapi_policy(spec)

    def test_batch_runner_applies_policy_to_both_same_snapshot_inputs(self):
        # The independent full-validator regression remains mandatory in CI.
        with patch.object(contracts, "validate_document", side_effect=lambda path, doc: {
                "path": str(path), "references": 1}) as full:
            results = contracts.validate_all_documents()
        self.assertEqual([r["policy_operations"] for r in results], [2, 4])
        self.assertEqual(full.call_count, 2)
        self.assertEqual([call.args[1] for call in full.call_args_list], self.specs)

    def test_batch_runner_rejects_a_weakened_preserved_or_successor_document(self):
        for index, original in enumerate(self.specs):
            spec = copy.deepcopy(original)
            spec["paths"]["/observations"]["post"]["security"] = []
            inputs = copy.deepcopy(self.specs)
            inputs[index] = spec
            # Isolate the real batch/policy path from unavailable optional packages.
            with self.subTest(version=original["info"]["version"]):
                with patch.object(contracts, "strict_json_loads", side_effect=inputs):
                    with patch.object(contracts, "validate_document", return_value={}):
                        with self.assertRaisesRegex(ValueError, "Security override"):
                            contracts.validate_all_documents()


if __name__ == "__main__":
    unittest.main()
