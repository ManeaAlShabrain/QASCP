"""P1 graph-boundary oracle over explicit synthetic fixtures, not an API/policy engine."""

import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit
from uuid import UUID
import re

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "contracts/qascp-2/graph"
PAIRS = {
    "owns": {("identity", "asset")}, "runs_as": {("asset", "identity")},
    "accesses": {("identity", "asset")}, "affects": {("finding", "asset")},
    "observed_on": {("event", "asset"), ("event", "identity")},
    "supports": {("evidence", "assertion")}, "evaluates": {("assertion", "control")},
    "depends_on": {("asset", "asset"), ("assertion", "evidence")},
}


def validate(name, value):
    schema = json.loads((FOLDER / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)


def instant(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def normalize_query(query, fixture):
    validate("neighborhood-query.schema.json", query)
    result = {"node_id": str(UUID(query["node_id"])), "depth": query.get("depth", 1),
              "limit": query.get("limit", 100), "direction": query.get("direction", "both"),
              "valid_at": query.get("valid_at", fixture["snapshot"]["valid_at"]),
              "known_at": query.get("known_at", fixture["snapshot"]["knowledge_cutoff"])}
    if (result["valid_at"] != fixture["snapshot"]["valid_at"]
            or result["known_at"] != fixture["snapshot"]["knowledge_cutoff"]):
        raise ValueError("Fixture snapshot does not match selected times")
    return result


def query_digest(normalized):
    encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def check_cursor_binding(cursor, normalized, fixture, now):
    """Check payload bindings only; real signature/key validation is not implemented."""
    validate("cursor-binding.schema.json", cursor)
    expected = {
        "tenant_id": fixture["tenant_id"], "principal_id": fixture["principal_id"],
        "authorization_version": fixture["authorization_version"],
        "root_id": normalized["node_id"], "snapshot_id": fixture["snapshot"]["snapshot_id"],
        "generation_id": fixture["snapshot"]["generation_id"],
        "query_digest": query_digest(normalized),
        "knowledge_cutoff": fixture["snapshot"]["knowledge_cutoff"],
        "valid_at": fixture["snapshot"]["valid_at"],
        "expires_at": fixture["snapshot"]["expires_at"],
    }
    if any(cursor[key] != value for key, value in expected.items()):
        raise ValueError("Cursor binding changed")
    if (instant(cursor["issued_at"]) > instant(now)
            or instant(now) >= instant(cursor["expires_at"])
            or instant(cursor["issued_at"]) < instant(cursor["knowledge_cutoff"])):
        raise ValueError("Cursor expired or issued outside snapshot interval")


def validate_page(page):
    validate("neighborhood-page.schema.json", page)
    nodes = {node["id"]: node for node in page["nodes"]}
    if len(nodes) != len(page["nodes"]) or page["root_id"] not in nodes:
        raise ValueError("Duplicate nodes or missing root")
    ids = set()
    for edge in page["edges"]:
        if edge["id"] in ids:
            raise ValueError("Duplicate edge ID")
        ids.add(edge["id"])
        if edge["source_id"] not in nodes or edge["target_id"] not in nodes:
            raise ValueError("Dangling endpoint")
        pair = (nodes[edge["source_id"]]["kind"], nodes[edge["target_id"]]["kind"])
        if pair not in PAIRS[edge["relation"]]:
            raise ValueError("Prohibited relation type pair")
        if ("valid_to" in edge
                and instant(edge["valid_to"]) <= instant(edge["valid_from"])):
            raise ValueError("Invalid edge interval")
        if instant(edge["recorded_at"]) > instant(page["snapshot"]["knowledge_cutoff"]):
            raise ValueError("Edge is newer than knowledge cutoff")
        valid_at = instant(page["snapshot"]["valid_at"])
        if (instant(edge["valid_from"]) > valid_at
                or ("valid_to" in edge and valid_at >= instant(edge["valid_to"]))):
            raise ValueError("Edge is outside source-valid snapshot")
    if instant(page["snapshot"]["expires_at"]) <= instant(page["snapshot"]["knowledge_cutoff"]):
        raise ValueError("Invalid snapshot expiry")


def fixture_page(fixture, query, now, cursor=None):
    """Model policy-filter-before-expansion; permissions are fixture inputs, not trusted auth."""
    if fixture.get("synthetic") is not True or fixture.get("fixture_version") != "0.2":
        raise ValueError("Only synthetic fixtures are supported")
    normalized = normalize_query(query, fixture)
    snapshot = fixture["snapshot"]
    if instant(now) >= instant(snapshot["expires_at"]):
        raise ValueError("Snapshot expired")
    if instant(now) < instant(snapshot["knowledge_cutoff"]):
        raise ValueError("Snapshot is newer than request")
    if "cursor" in query and cursor is None:
        raise ValueError("Opaque cursor verification is not available in fixture oracle")
    if cursor is not None:
        check_cursor_binding(cursor, normalized, fixture, now)
    nodes = {n["id"]: n for n in fixture["nodes"] if n["id"] in fixture["allowed_node_ids"]}
    root = normalized["node_id"]
    if root not in nodes:
        raise ValueError("Root unavailable")
    permitted = [
        e for e in fixture["edges"] if e["id"] in fixture["allowed_edge_ids"]
        and e["observation_id"] in fixture["allowed_observation_ids"]
        and e["source_id"] in nodes and e["target_id"] in nodes
        and instant(e["recorded_at"]) <= instant(snapshot["knowledge_cutoff"])
        and instant(e["valid_from"]) <= instant(snapshot["valid_at"])
        and ("valid_to" not in e or instant(snapshot["valid_at"]) < instant(e["valid_to"]))
    ]
    found, frontier, visited = {}, {root}, {root}
    for hop in range(1, normalized["depth"] + 1):
        following = set()
        for edge in permitted:
            targets = []
            if normalized["direction"] in ("outgoing", "both") and edge["source_id"] in frontier:
                targets.append(edge["target_id"])
            if normalized["direction"] in ("incoming", "both") and edge["target_id"] in frontier:
                targets.append(edge["source_id"])
            if targets:
                found.setdefault(edge["id"], (hop, edge))
                following.update(targets)
        frontier = following - visited
        visited.update(following)
    ordered = sorted(found.values(), key=lambda item: (item[0], item[1]["id"]))
    if cursor is not None:
        last = (cursor["last_hop"], cursor["last_edge_id"])
        if last not in [(hop, edge["id"]) for hop, edge in ordered]:
            raise ValueError("Cursor ordering key is unavailable")
        ordered = [(hop, edge) for hop, edge in ordered if (hop, edge["id"]) > last]
    selected, endpoint_ids = [], {root}
    for hop, edge in ordered:
        candidate_ids = endpoint_ids | {edge["source_id"], edge["target_id"]}
        if len(selected) >= normalized["limit"] or len(candidate_ids) > 201:
            break
        selected.append((hop, edge))
        endpoint_ids = candidate_ids
    truncated = len(selected) < len(ordered)
    page = {
        "contract_version": "0.2", "tenant_id": fixture["tenant_id"], "root_id": root,
        "nodes": [copy.deepcopy(nodes[key]) for key in sorted(endpoint_ids)],
        "edges": [copy.deepcopy(edge) for _, edge in selected],
        "snapshot": copy.deepcopy(snapshot), "truncated": truncated,
    }
    binding = None
    if truncated:
        if not selected:
            raise ValueError("Cannot produce progressing continuation")
        hop, edge = selected[-1]
        # This explicit marker is not a production token or cryptographic signature.
        page["next_cursor"] = "synthetic-unsigned:" + edge["id"]
        binding = {
            "cursor_version": "0.2", "tenant_id": fixture["tenant_id"],
            "principal_id": fixture["principal_id"],
            "authorization_version": fixture["authorization_version"], "root_id": root,
            "snapshot_id": snapshot["snapshot_id"], "generation_id": snapshot["generation_id"],
            "query_digest": query_digest(normalized),
            "knowledge_cutoff": snapshot["knowledge_cutoff"], "valid_at": snapshot["valid_at"],
            "issued_at": now, "expires_at": snapshot["expires_at"],
            "last_hop": hop, "last_edge_id": edge["id"], "key_id": "synthetic-no-signature",
        }
        validate("cursor-binding.schema.json", binding)
    validate_page(page)
    return {"page": page, "cursor_binding": binding}



def check_openapi_structure(document=None):
    """QASCP-specific static checks, not a full OpenAPI specification validator."""
    start = FOLDER / "openapi-0.2.json"
    spec = document if document is not None else json.loads(start.read_text(encoding="utf-8"))
    if (spec.get("openapi") != "3.1.0" or spec.get("info", {}).get("version") != "0.2.0"
            or spec.get("security") != [{"oidcBearer": []}]):
        raise ValueError("Invalid API version or bearer security")
    operations, count = set(), 0
    for path, path_item in spec["paths"].items():
        if path_item.get("parameters") != [{"$ref": "#/components/parameters/TenantSelector"}]:
            raise ValueError("Missing trusted tenant selector")
        for method in ("get", "post", "put", "patch", "delete"):
            if method not in path_item:
                continue
            operation = path_item[method]
            if "security" in operation or operation.get("operationId") in operations:
                raise ValueError("Security override or duplicate operation ID")
            if not operation.get("operationId"):
                raise ValueError("Missing operation ID")
            operations.add(operation["operationId"])
            parameters = operation.get("parameters", [])
            actual = {p["name"] for p in parameters if p.get("in") == "path" and p.get("required")}
            if actual != set(re.findall(r"\{([^}]+)\}", path)):
                raise ValueError("Path parameter mismatch")
            for required_status in ("200", "400", "401", "403", "429", "503"):
                if required_status not in operation["responses"]:
                    raise ValueError("Missing documented response")
            if method == "post":
                body = operation["requestBody"]
                if body.get("required") is not True or set(body["content"]) != {"application/json"}:
                    raise ValueError("Invalid import body binding")
    for value in spec.get("components", {}).get("schemas", {}).values():
        Draft202012Validator.check_schema(value)
    documents, queue = {start.resolve(): spec}, [start.resolve()]
    base = (ROOT / "contracts").resolve()
    while queue:
        filename = queue.pop()
        def visit(value):
            nonlocal count
            if isinstance(value, dict):
                if "$ref" in value:
                    count += 1
                    parts = urlsplit(value["$ref"])
                    if parts.scheme or parts.netloc or parts.query:
                        raise ValueError("Remote references are not permitted")
                    target_file = (filename.parent / unquote(parts.path)).resolve() if parts.path else filename
                    if not target_file.is_relative_to(base):
                        raise ValueError("Reference leaves contract root")
                    if target_file not in documents:
                        documents[target_file] = json.loads(target_file.read_text(encoding="utf-8"))
                        queue.append(target_file)
                    target = documents[target_file]
                    pointer = unquote(parts.fragment)
                    if pointer and not pointer.startswith("/"):
                        raise ValueError("Only local JSON pointers are supported here")
                    for key in pointer.strip("/").split("/") if pointer else []:
                        key = key.replace("~1", "/").replace("~0", "~")
                        target = target[int(key)] if isinstance(target, list) else target[key]
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)
        visit(documents[filename])
    return {"operations": len(operations), "references": count, "documents": len(documents)}


if __name__ == "__main__":
    fixture = json.loads((ROOT / "tests/fixtures/graph-query-examples.json").read_text())
    result = fixture_page(fixture, {"node_id": fixture["nodes"][0]["id"], "depth": 2},
                          "2026-11-16T10:01:00Z")
    print(json.dumps({"visible_nodes": len(result["page"]["nodes"]),
                      "visible_edges": len(result["page"]["edges"])}))
