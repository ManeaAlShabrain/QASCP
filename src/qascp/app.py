"""Seedless tenant entry point; generic failures never serialize identity/DB exceptions."""

from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from .config import Settings, uuid_text
from .database import AccessDenied, Tenancy
from .identity import IdentityError, OIDC


def create_app():
    settings = Settings.load()
    identity = OIDC(settings.issuer, settings.audience, settings.oidc_ca)
    tenancy = Tenancy(settings.tenants)

    @asynccontextmanager
    async def lifespan(app):
        tenancy.open()
        try:
            yield
        finally:
            tenancy.close()

    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)

    @app.middleware("http")
    async def boundary(request, next_call):
        correlation = str(uuid4())
        request.state.correlation = correlation
        try:
            response = await next_call(request)
        except Exception:
            response = JSONResponse({"error": "service_unavailable", "correlation_id": correlation}, status_code=503)
        response.headers.update({"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff",
                                 "X-Correlation-ID": correlation, "Strict-Transport-Security": "max-age=31536000"})
        return response

    def error(request, status, code):
        headers = {"WWW-Authenticate": "Bearer"} if status == 401 else None
        return JSONResponse({"error": code, "correlation_id": request.state.correlation}, status_code=status, headers=headers)

    @app.exception_handler(404)
    async def missing(request, exc):
        return error(request, 404, "not_found")

    @app.exception_handler(405)
    async def method(request, exc):
        return error(request, 405, "method_not_allowed")

    @app.get("/live")
    async def live(request: Request):
        return {"status": "alive"}

    @app.get("/api/v2/tenancy/current")
    async def current(request: Request):
        auth = request.headers.getlist("authorization")
        if len(auth) != 1 or not auth[0].startswith("Bearer "):
            return error(request, 401, "unauthorized")
        try:
            subject = await run_in_threadpool(identity.verify, auth[0][7:])
        except IdentityError:
            return error(request, 401, "unauthorized")
        selectors = request.headers.getlist("x-tenant-id")
        try:
            if len(selectors) != 1:
                raise ValueError("Missing selector")
            tenant = uuid_text(selectors[0])
            if (request.url.query or request.headers.get("transfer-encoding")
                    or request.headers.get("content-length", "0") != "0"):
                raise ValueError("Unexpected request data")
        except ValueError:
            return error(request, 400, "invalid_request")
        try:
            return await run_in_threadpool(tenancy.current, tenant, subject, request.state.correlation)
        except AccessDenied:
            return error(request, 403, "forbidden")

    return app
