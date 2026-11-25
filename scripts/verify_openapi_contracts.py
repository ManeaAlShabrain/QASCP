"""P1 full OpenAPI 3.1 validation with bounded, JSON-only local references."""

import copy
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import url2pathname

if __package__:
    from .verify_foundation import strict_json_loads
    from .verify_openapi_policy import check_openapi_policy
else:
    from verify_foundation import strict_json_loads
    from verify_openapi_policy import check_openapi_policy

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = (ROOT / "contracts").resolve()
DOCUMENTS = (
    ROOT / "contracts/qascp-2/openapi.json",
    ROOT / "contracts/qascp-2/graph/openapi-0.2.json",
)


def contract_path(path, root=CONTRACTS):
    """Check lexical containment before resolution and resolved scope before reads."""
    root = root.resolve()
    path = Path(path)
    if path.drive.startswith("\\\\") or not path.absolute().is_relative_to(root):
        raise ValueError("Document leaves contract boundary")
    path = path.resolve()
    if not path.is_relative_to(root) or path.suffix != ".json":
        raise ValueError("Reference leaves JSON contract boundary")
    return path


def load_local_json(uri, root=CONTRACTS):
    """Permit file URIs only, inside the resolved contract root; no URL handlers."""
    parts = urlsplit(uri)
    if parts.scheme != "file" or parts.netloc or parts.query:
        raise ValueError("Only local file references are permitted")
    decoded = unquote(parts.path)
    if "\\" in decoded or decoded.startswith("//"):
        raise ValueError("Network-style file paths are prohibited")
    path = contract_path(Path(url2pathname(parts.path)), root)
    return strict_json_loads(path.read_text(encoding="utf-8"))


def check_reference_closure(path, document, root=CONTRACTS):
    """Resolve every JSON Pointer before invoking the third-party validator."""
    root = root.resolve()
    path = contract_path(path, root)
    documents, pending, references = {path: document}, [path], 0
    while pending:
        filename = pending.pop()
        def visit(value):
            nonlocal references
            if isinstance(value, dict):
                for keyword in ("$ref", "$dynamicRef", "$recursiveRef"):
                    if keyword not in value:
                        continue
                    references += 1
                    ref = value[keyword]
                    if not isinstance(ref, str):
                        raise ValueError("Reference must be a string")
                    parts = urlsplit(ref)
                    if parts.scheme or parts.netloc or parts.query:
                        raise ValueError("Remote or absolute URI references are prohibited")
                    target_uri = urljoin(filename.as_uri(), ref)
                    target_parts = urlsplit(target_uri)
                    decoded = unquote(target_parts.path)
                    if "\\" in decoded or decoded.startswith("//"):
                        raise ValueError("Network-style file paths are prohibited")
                    target_file = contract_path(Path(url2pathname(target_parts.path)), root)
                    # Load through the exact same bounded JSON reader used by validation.
                    if target_file not in documents:
                        documents[target_file] = load_local_json(target_uri, root)
                        pending.append(target_file)
                    target = documents[target_file]
                    pointer = unquote(target_parts.fragment)
                    if pointer and not pointer.startswith("/"):
                        raise ValueError("Only JSON Pointer fragments are permitted")
                    for key in pointer[1:].split("/") if pointer else []:
                        if "~" in key.replace("~0", "").replace("~1", ""):
                            raise ValueError("Invalid JSON Pointer escape")
                        key = key.replace("~1", "/").replace("~0", "~")
                        if isinstance(target, list):
                            if not key.isascii() or not key.isdigit() or (len(key) > 1 and key.startswith("0")):
                                raise ValueError("Invalid array JSON Pointer")
                            target = target[int(key)]
                        else:
                            target = target[key]
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)
        visit(documents[filename])
    return {"documents": len(documents), "references": references}


def validate_document(path, document=None, root=CONTRACTS):
    root = root.resolve()
    path = contract_path(path, root)
    source = strict_json_loads(path.read_text(encoding="utf-8")) if document is None else copy.deepcopy(document)
    if source.get("openapi") != "3.1.0":
        raise ValueError("This verifier explicitly targets OpenAPI 3.1.0")
    closure = check_reference_closure(path, source, root)

    def bounded_handler(uri):
        return load_local_json(uri, root)

    from openapi_spec_validator import OpenAPIV31SpecValidator

    class LocalOnlyOpenAPIValidator(OpenAPIV31SpecValidator):
        resolver_handlers = {"file": bounded_handler}

    # No default HTTP(S), urllib or all-URL resolver handlers are retained.
    LocalOnlyOpenAPIValidator(source, base_uri=path.as_uri()).validate()
    return {"path": str(path.relative_to(ROOT)), **closure}


def validate_all_documents():
    """Check specification validity and QASCP policy on the same input snapshot."""
    results = []
    for path in DOCUMENTS:
        source = strict_json_loads(contract_path(path).read_text(encoding="utf-8"))
        result = validate_document(path, source)
        result["policy_operations"] = check_openapi_policy(source)["operations"]
        results.append(result)
    return results


if __name__ == "__main__":
    print(json.dumps(validate_all_documents(), indent=2))
