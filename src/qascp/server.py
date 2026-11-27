"""Explicit TLS entry point, no request URL/access log or proxy-header trust."""

import os
from pathlib import Path
import ssl

import uvicorn


def main():
    try:
        cert, key = os.environ["QASCP_TLS_CERT"], os.environ["QASCP_TLS_KEY"]
        if not Path(cert).is_file() or not Path(key).is_file():
            raise ValueError("Missing TLS material")
        port = int(os.environ.get("QASCP_PORT", "8443"))
        if not 1024 <= port <= 65535:
            raise ValueError("Invalid port")
        from .app import create_app
        app = create_app()
    except Exception:
        raise SystemExit("QASCP startup configuration rejected") from None
    uvicorn.run(app, host="127.0.0.1", port=port, ssl_certfile=cert, ssl_keyfile=key,
                ssl_version=ssl.PROTOCOL_TLS_SERVER, access_log=False, log_config=None,
                proxy_headers=False, server_header=False, date_header=False,
                limit_concurrency=64, timeout_keep_alive=5, timeout_graceful_shutdown=5)
