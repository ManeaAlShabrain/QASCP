"""Shared static OpenAPI acceptance policy; no runtime authentication claim."""

import re


def resolve_parameter(parameter, components):
    """Support local parameter aliases without permitting cycles or external reads."""
    seen = set()
    while isinstance(parameter, dict) and "$ref" in parameter:
        ref = parameter["$ref"]
        prefix = "#/components/parameters/"
        if not isinstance(ref, str) or not ref.startswith(prefix) or ref in seen:
            raise ValueError("Invalid or cyclic parameter reference")
        seen.add(ref)
        key = ref[len(prefix):]
        if "/" in key or "~" in key.replace("~0", "").replace("~1", ""):
            raise ValueError("Invalid parameter reference token")
        key = key.replace("~1", "/").replace("~0", "~")
        if key not in components:
            raise ValueError("Missing parameter reference")
        parameter = components[key]
    if not isinstance(parameter, dict):
        raise ValueError("Invalid parameter object")
    return parameter


def check_openapi_policy(spec):
    """Enforce the same tenant/authentication contract for both API proposals."""
    if (spec.get("openapi") != "3.1.0"
            or spec.get("security") != [{"oidcBearer": []}]):
        raise ValueError("Invalid API version or bearer security")
    components = spec.get("components", {})
    if spec.get("webhooks") or components.get("callbacks"):
        raise ValueError("Unreviewed webhook or callback surface")
    bearer = components.get("securitySchemes", {}).get("oidcBearer", {})
    if (bearer.get("type") != "http" or bearer.get("scheme", "").lower() != "bearer"
            or bearer.get("bearerFormat") != "JWT"):
        raise ValueError("Bearer security scheme was weakened")
    parameter_components = components.get("parameters", {})
    tenant = parameter_components.get("TenantSelector", {})
    if (tenant.get("name") != "X-Tenant-ID" or tenant.get("in") != "header"
            or tenant.get("required") is not True
            or tenant.get("schema", {}).get("type") != "string"
            or tenant.get("schema", {}).get("format") != "uuid"):
        raise ValueError("Tenant selector definition was weakened")
    operations = set()
    for path, path_item in spec["paths"].items():
        if "$ref" in path_item:
            raise ValueError("Unreviewed referenced path surface")
        if path_item.get("parameters") != [{"$ref": "#/components/parameters/TenantSelector"}]:
            raise ValueError("Missing trusted tenant selector")
        for method in ("get", "post", "put", "patch", "delete", "head", "options", "trace"):
            if method not in path_item:
                continue
            operation = path_item[method]
            if operation.get("callbacks"):
                raise ValueError("Unreviewed callback surface")
            if "security" in operation or operation.get("operationId") in operations:
                raise ValueError("Security override or duplicate operation ID")
            if not operation.get("operationId"):
                raise ValueError("Missing operation ID")
            operations.add(operation["operationId"])
            parameters = [resolve_parameter(p, parameter_components)
                          for p in operation.get("parameters", [])]
            if any(p.get("in") == "header" and p.get("name", "").lower() == "x-tenant-id"
                   for p in parameters):
                raise ValueError("Operation overrides the inherited tenant selector")
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
    return {"operations": len(operations)}
