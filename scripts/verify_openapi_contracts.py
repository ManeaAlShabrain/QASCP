"""P1 full OpenAPI 3.1 validation with bounded, JSON-only local references."""

import copy
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import url2pathname

from openapi_spec_validator import OpenAPIV31SpecValidator

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = (ROOT / "contracts").resolve()
DOCUMENTS = (
    ROOT / "contracts/qascp-2/openapi.json",
    ROOT / "contracts/qascp-2/graph/openapi-0.2.json",
)


def load_local_json(uri, root=CONTRACTS):
    """Permit file URIs only, inside the resolved contract root; no URL handlers."""
    parts = urlsplit(uri)
    if parts.scheme != "file" or parts.netloc or parts.query:
        raise ValueError("Only local file references are permitted")
    path = Path(url2pathname(parts.path)).resolve()
    if not path.is_relative_to(root.resolve()) or path.suffix != ".json":
        raise ValueError("Reference leaves JSON contract boundary")
    return json.loads(path.read_text(encoding="utf-8"))


def check_reference_closure(path, document, root=CONTRACTS):
    """Resolve every JSON Pointer before invoking the third-party validator."""
    path, root = path.resolve(), root.resolve()
    if not path.is_relative_to(root):
        raise ValueError("Document leaves contract boundary")
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
                    target_file = Path(url2pathname(target_parts.path)).resolve()
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
                            if not key.isdigit() or (len(key) > 1 and key.startswith("0")):
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
    path, root = path.resolve(), root.resolve()
    source = json.loads(path.read_text(encoding="utf-8")) if document is None else copy.deepcopy(document)
    if source.get("openapi") != "3.1.0":
        raise ValueError("This verifier explicitly targets OpenAPI 3.1.0")
    closure = check_reference_closure(path, source, root)

    def bounded_handler(uri):
        return load_local_json(uri, root)

    class LocalOnlyOpenAPIValidator(OpenAPIV31SpecValidator):
        resolver_handlers = {"file": bounded_handler}

    # No default HTTP(S), urllib or all-URL resolver handlers are retained.
    LocalOnlyOpenAPIValidator(source, base_uri=path.as_uri()).validate()
    return {"path": str(path.relative_to(ROOT)), **closure}


def validate_all_documents():
    return [validate_document(path) for path in DOCUMENTS]


if __name__ == "__main__":
    print(json.dumps(validate_all_documents(), indent=2))
