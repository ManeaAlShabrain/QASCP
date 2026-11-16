"""Full specification and bounded-reference failures supplement graph structural tests."""

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

from scripts.verify_openapi_contracts import (
    DOCUMENTS, ROOT, check_reference_closure, load_local_json, validate_all_documents,
    validate_document,
)


class OpenAPIContractTests(unittest.TestCase):
    def setUp(self):
        self.path = DOCUMENTS[1]
        self.spec = json.loads(self.path.read_text(encoding="utf-8"))

    def test_both_versioned_documents_pass_full_validation_without_network(self):
        with patch("socket.create_connection", side_effect=AssertionError("Network forbidden")), \
             patch("requests.sessions.Session.request", side_effect=AssertionError("HTTP forbidden")), \
             patch("urllib.request.urlopen", side_effect=AssertionError("URL handlers forbidden")):
            results = validate_all_documents()
        self.assertEqual(len(results), 2)
        self.assertTrue(all(result["references"] > 0 for result in results))

    def test_missing_info_and_invalid_response_status_fail_full_validation(self):
        for mutation in ("info", "status"):
            spec = copy.deepcopy(self.spec)
            if mutation == "info":
                del spec["info"]
            else:
                operation = spec["paths"]["/observations"]["post"]
                operation["responses"]["XYZ"] = {"description": "invalid"}
            with self.subTest(mutation=mutation), self.assertRaises(OpenAPIValidationError):
                validate_document(self.path, spec)

    def test_unresolved_path_parameter_and_duplicate_operation_fail(self):
        for mutation in ("path", "operation"):
            spec = copy.deepcopy(self.spec)
            operation = spec["paths"]["/graph/nodes/{node_id}/neighbors"]["get"]
            if mutation == "path":
                operation["parameters"] = [
                    p for p in operation["parameters"] if p.get("in") != "path"
                ]
            else:
                operation["operationId"] = "ingestObservation"
            with self.subTest(mutation=mutation), self.assertRaises(OpenAPIValidationError):
                validate_document(self.path, spec)

    def test_remote_reference_is_rejected_before_network(self):
        for ref in ("https://example.invalid/schema.json", "//example.invalid/schema.json",
                    "file:///etc/passwd", "urn:untrusted:source"):
            spec = copy.deepcopy(self.spec)
            spec["paths"]["/observations"]["post"]["requestBody"]["content"][
                "application/json"]["schema"] = {"$ref": ref}
            with self.subTest(ref=ref), \
                 patch("socket.create_connection", side_effect=AssertionError("Network forbidden")), \
                 self.assertRaises(ValueError):
                validate_document(self.path, spec)

    def test_dynamic_reference_cannot_bypass_the_preflight(self):
        for keyword in ("$dynamicRef", "$recursiveRef"):
            spec = copy.deepcopy(self.spec)
            spec["components"]["schemas"]["Escape"] = {
                keyword: "https://example.invalid/schema.json"
            }
            with self.subTest(keyword=keyword), self.assertRaises(ValueError):
                check_reference_closure(self.path, spec)

    def test_encoded_traversal_query_and_bad_pointer_fail(self):
        for ref, error in [
            ("%2e%2e/%2e%2e/%2e%2e/README.md", ValueError),
            ("./neighborhood-page.schema.json?token=forbidden", ValueError),
            ("./neighborhood-page.schema.json#/missing", KeyError),
            ("./neighborhood-page.schema.json#/$defs/~2bad", ValueError),
            ("./neighborhood-page.schema.json#named-anchor", ValueError),
        ]:
            spec = copy.deepcopy(self.spec)
            spec["paths"]["/observations"]["post"]["requestBody"]["content"][
                "application/json"]["schema"] = {"$ref": ref}
            with self.subTest(ref=ref), self.assertRaises(error):
                check_reference_closure(self.path, spec)

    def test_local_reader_has_no_http_unc_or_non_json_fallback(self):
        for uri in ("https://example.invalid/data", "file://host/share/data.json",
                    (ROOT / "README.md").as_uri()):
            with self.subTest(uri=uri), self.assertRaises(ValueError):
                load_local_json(uri)

    def test_verifier_version_is_explicit(self):
        self.spec["openapi"] = "3.0.3"
        with self.assertRaisesRegex(ValueError, "3.1.0"):
            validate_document(self.path, self.spec)


if __name__ == "__main__":
    unittest.main()
