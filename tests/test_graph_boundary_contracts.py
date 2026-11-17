"""P1 boundary fixtures and contract checks; no deployed authorization claim."""

import copy
import json
import unittest
from pathlib import Path

from jsonschema import ValidationError

from scripts.verify_graph_query_fixtures import (
    check_cursor_binding, check_openapi_structure, fixture_page, normalize_query,
    validate, validate_page,
)

ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-11-16T10:01:00Z"


def uid(n):
    return "00000000-0000-4000-8000-" + str(n).zfill(12)


class GraphBoundaryContractTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(
            (ROOT / "tests/fixtures/graph-query-examples.json").read_text(encoding="utf-8")
        )
        self.query = {"node_id": uid(1), "depth": 2}

    def page(self, query=None):
        return fixture_page(self.fixture, query or self.query, NOW)

    def test_valid_neighborhood_and_cycle_terminate(self):
        result = self.page()["page"]
        self.assertEqual(len(result["nodes"]), 5)
        self.assertEqual(len(result["edges"]), 5)
        self.assertFalse(result["truncated"])
        self.assertNotIn("next_cursor", result)

    def test_hidden_intermediate_cannot_reveal_visible_endpoint(self):
        self.fixture["allowed_node_ids"].remove(uid(2))
        result = self.page()["page"]
        ids = {node["id"] for node in result["nodes"]}
        self.assertNotIn(uid(2), ids)
        self.assertNotIn(uid(3), ids)

    def test_hidden_edge_and_provenance_are_filtered_before_counts(self):
        self.fixture["allowed_observation_ids"].remove(uid(201))
        self.fixture["allowed_edge_ids"].remove(uid(103))
        result = self.page()["page"]
        ids = {edge["id"] for edge in result["edges"]}
        self.assertNotIn(uid(101), ids)
        self.assertNotIn(uid(103), ids)
        self.assertNotIn(uid(3), {node["id"] for node in result["nodes"]})

    def test_invisible_and_absent_root_have_same_fixture_error(self):
        for root in [uid(2), uid(999)]:
            self.fixture["allowed_node_ids"] = [uid(1)]
            with self.subTest(root=root), self.assertRaisesRegex(ValueError, "Root unavailable"):
                self.page({"node_id": root})

    def test_direction_and_depth(self):
        outgoing = self.page({"node_id": uid(1), "depth": 1, "direction": "outgoing"})["page"]
        incoming = self.page({"node_id": uid(1), "depth": 1, "direction": "incoming"})["page"]
        self.assertEqual({e["id"] for e in outgoing["edges"]}, {uid(101), uid(103)})
        self.assertEqual({e["id"] for e in incoming["edges"]}, {uid(105)})

    def test_query_bounds_unknown_fields_and_bad_ids(self):
        for field, value in [("depth", 3), ("limit", 201), ("depth", 0), ("limit", True),
                             ("direction", "all"), ("node_id", "not-a-uuid"),
                             ("tenant_id", uid(999)), ("known_at", "yesterday")]:
            query = {**self.query, field: value}
            with self.subTest(field=field, value=value), self.assertRaises(ValidationError):
                self.page(query)

    def test_pages_cover_exactly_visible_edges_without_duplicates(self):
        query = {**self.query, "limit": 2}
        cursor, collected = None, []
        for _ in range(4):
            result = fixture_page(self.fixture, query, NOW, cursor)
            collected.extend(e["id"] for e in result["page"]["edges"])
            cursor = result["cursor_binding"]
            if cursor is None:
                break
        self.assertIsNone(cursor)
        self.assertEqual(len(collected), 5)
        self.assertEqual(len(set(collected)), 5)

    def test_cursor_binds_tenant_principal_authority_snapshot_and_query(self):
        query = {**self.query, "limit": 1}
        cursor = self.page(query)["cursor_binding"]
        for field in ["tenant_id", "principal_id", "authorization_version"]:
            data = copy.deepcopy(self.fixture)
            data[field] = uid(999) if field == "tenant_id" else "changed"
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "binding"):
                fixture_page(data, query, NOW, cursor)
        for field in ["snapshot_id", "generation_id"]:
            data = copy.deepcopy(self.fixture)
            data["snapshot"][field] = uid(999)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "binding"):
                fixture_page(data, query, NOW, cursor)
        with self.assertRaisesRegex(ValueError, "binding"):
            fixture_page(self.fixture, {**query, "direction": "incoming"}, NOW, cursor)

    def test_expiry_and_future_issue_time_fail(self):
        query = {**self.query, "limit": 1}
        cursor = self.page(query)["cursor_binding"]
        with self.assertRaisesRegex(ValueError, "expired"):
            fixture_page(self.fixture, query, "2026-11-16T10:10:00Z", cursor)
        cursor["issued_at"] = "2026-11-16T10:05:00Z"
        with self.assertRaisesRegex(ValueError, "outside"):
            check_cursor_binding(cursor, normalize_query(query, self.fixture), self.fixture, NOW)

    def test_opaque_real_cursor_is_not_treated_as_verified(self):
        with self.assertRaisesRegex(ValueError, "verification is not available"):
            self.page({**self.query, "cursor": "not-a-verified-signature"})

    def test_truncation_and_cursor_schema_are_coupled(self):
        page = self.page({**self.query, "limit": 1})["page"]
        del page["next_cursor"]
        with self.assertRaises(ValidationError):
            validate_page(page)
        page = self.page()["page"]
        page["next_cursor"] = "unexpected"
        with self.assertRaises(ValidationError):
            validate_page(page)

    def test_dangling_duplicate_and_invalid_pair_fail(self):
        for mutation in ["dangling", "duplicate", "pair"]:
            page = self.page()["page"]
            if mutation == "dangling":
                page["nodes"] = [n for n in page["nodes"] if n["id"] != uid(2)]
            elif mutation == "duplicate":
                edge = copy.deepcopy(page["edges"][0])
                edge["confidence"] = 0.5
                page["edges"].append(edge)
            else:
                page["nodes"][0]["kind"] = "identity"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_page(page)

    def test_access_qualifier_and_unexpected_metadata(self):
        page = self.page()["page"]
        page["edges"][0]["relation"] = "accesses"
        with self.assertRaises(ValidationError):
            validate_page(page)
        page = self.page()["page"]
        page["nodes"][0]["raw_secret"] = "forbidden"
        with self.assertRaises(ValidationError):
            validate_page(page)

    def test_future_and_expired_claims_do_not_appear(self):
        self.fixture["edges"][0]["recorded_at"] = "2026-11-16T10:01:00Z"
        self.fixture["edges"][2]["valid_to"] = self.fixture["snapshot"]["valid_at"]
        result = self.page()["page"]
        self.assertNotIn(uid(101), {e["id"] for e in result["edges"]})
        self.assertNotIn(uid(103), {e["id"] for e in result["edges"]})

    def test_lag_is_explicit_even_when_no_visible_edges(self):
        self.fixture["snapshot"]["projection_state"] = "lagging"
        self.fixture["allowed_edge_ids"] = []
        page = self.page()["page"]
        self.assertEqual(page["snapshot"]["projection_state"], "lagging")
        self.assertEqual(page["edges"], [])

    def test_two_hundred_edges_do_not_override_node_budget(self):
        data = copy.deepcopy(self.fixture)
        data["nodes"] = [{"id": uid(1), "kind": "asset"}]
        data["edges"] = []
        template = self.fixture["edges"][0]
        for i in range(200):
            parent, leaf = uid(1000+i), uid(2000+i)
            data["nodes"] += [{"id": parent, "kind": "asset"}, {"id": leaf, "kind": "asset"}]
            data["edges"] += [
                {**template, "id": uid(3000+i), "source_id": uid(1), "target_id": parent},
                {**template, "id": uid(4000+i), "source_id": parent, "target_id": leaf},
            ]
        data["allowed_node_ids"] = [n["id"] for n in data["nodes"]]
        data["allowed_edge_ids"] = [e["id"] for e in data["edges"]]
        query = {"node_id": uid(1), "depth": 2, "direction": "outgoing", "limit": 200}
        cursor, collected, sizes = None, [], []
        for _ in range(4):
            result = fixture_page(data, query, NOW, cursor)
            page = result["page"]
            self.assertLessEqual(len(page["nodes"]), 201)
            sizes.append(len(page["edges"]))
            collected.extend(e["id"] for e in page["edges"])
            cursor = result["cursor_binding"]
            if cursor is None:
                break
        self.assertEqual(sizes, [200, 100, 100])
        self.assertEqual(len(set(collected)), 400)

    def test_api_operations_and_local_references_resolve(self):
        result = check_openapi_structure()
        self.assertEqual(result["operations"], 4)
        self.assertGreater(result["references"], 0)

    def test_api_security_path_and_reference_regressions(self):
        path = ROOT / "contracts/qascp-2/graph/openapi-0.2.json"
        original = json.loads(path.read_text())
        for mutation in ["security", "path", "operation", "reference"]:
            spec = copy.deepcopy(original)
            op = spec["paths"]["/graph/nodes/{node_id}/neighbors"]["get"]
            if mutation == "security":
                op["security"] = []
            elif mutation == "path":
                op["parameters"] = []
            elif mutation == "operation":
                op["operationId"] = "ingestObservation"
            else:
                op["responses"]["200"]["content"]["application/json"]["schema"]["$ref"] = "./missing.json"
            with self.subTest(mutation=mutation), self.assertRaises((ValueError, FileNotFoundError)):
                check_openapi_structure(spec)

    def test_non_synthetic_data_is_refused(self):
        self.fixture["synthetic"] = False
        with self.assertRaisesRegex(ValueError, "synthetic"):
            self.page()

    def test_duplicate_fixture_ids_are_rejected_before_collapse(self):
        for collection in ("nodes", "edges"):
            data = copy.deepcopy(self.fixture)
            data[collection].append(copy.deepcopy(data[collection][0]))
            with self.subTest(collection=collection), self.assertRaisesRegex(ValueError, "Duplicate fixture"):
                fixture_page(data, self.query, NOW)

    def test_hidden_invalid_fixture_edges_are_not_silently_ignored(self):
        for mutation in ("endpoint", "pair", "interval"):
            data = copy.deepcopy(self.fixture)
            edge = data["edges"][0]
            data["allowed_edge_ids"].remove(edge["id"])
            if mutation == "endpoint":
                edge["target_id"] = uid(999)
            elif mutation == "pair":
                edge["relation"] = "owns"
            else:
                edge["valid_to"] = edge["valid_from"]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                fixture_page(data, self.query, NOW)

    def test_structural_checker_shares_strict_reference_policy(self):
        original = json.loads((ROOT / "contracts/qascp-2/graph/openapi-0.2.json").read_text())
        for ref in ("./neighborhood-page.schema.json#/required/-1",
                    "./neighborhood-page.schema.json#/required/01",
                    "https://example.invalid/schema.json"):
            spec = copy.deepcopy(original)
            spec["components"]["schemas"]["Probe"] = {"$ref": ref}
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                check_openapi_structure(spec)


if __name__ == "__main__":
    unittest.main()
