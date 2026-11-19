"""Authenticated Streamable HTTP MCP endpoint for the Bob Ross lab on Render."""
from __future__ import annotations

import hmac
import os

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from core import (
    compare_models,
    dataset_overview,
    reference_summary,
    storyboard,
    visualization_links,
)

HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
mcp = FastMCP(
    "DataCollectionMov - Bob Ross Lab",
    stateless_http=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=bool(HOST),
        allowed_hosts=[HOST] if HOST else [],
    ),
)


@mcp.tool()
def bob_ross_dataset() -> dict:
    """Describe the pinned FiveThirtyEight Bob Ross data, SHA, license and features."""
    return dataset_overview()


@mcp.tool()
def bob_ross_reference() -> dict:
    """Read the precomputed and verified classroom K-Means reference, not a new run."""
    return reference_summary()


@mcp.tool()
def bob_ross_compare_models(k: int = 4, exclude_guests: bool = True) -> dict:
    """Run K-Means, Ward and average-Hamming on identical Bob Ross data and compare fairly."""
    return compare_models(k=k, exclude_guests=exclude_guests)


@mcp.tool()
def bob_ross_visualizations() -> dict:
    """Get links to the reproducible profiles, diagnostics and classroom HTML."""
    return visualization_links()


@mcp.tool()
def bob_ross_storyboard() -> dict:
    """Build a six-scene video/storytelling outline grounded in the committed analysis."""
    return storyboard()


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request) -> Response:
    return JSONResponse({"status": "ok", "service": "datacollectionmov-bob-ross"})


class BearerAuthMiddleware:
    """Protect all MCP traffic; the only public route is /health."""

    def __init__(self, app: ASGIApp, token: str) -> None:
        self.app = app
        self.expected = "Bearer " + token

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http" or scope["path"] == "/health":
            await self.app(scope, receive, send)
            return
        headers = dict(scope.get("headers", []))
        supplied = headers.get(b"authorization", b"").decode("utf-8", errors="replace")
        if hmac.compare_digest(supplied, self.expected):
            await self.app(scope, receive, send)
            return
        response = JSONResponse(
            {"jsonrpc": "2.0", "error": {"code": -32001, "message": "Unauthorized"}, "id": None},
            status_code=401,
        )
        await response(scope, receive, send)


def create_app():
    token = os.getenv("MCP_API_TOKEN", "")
    if len(token) < 24:
        raise RuntimeError("MCP_API_TOKEN must be configured (at least 24 characters); refusing an unauthenticated public service.")
    app = mcp.streamable_http_app()
    app.add_middleware(BearerAuthMiddleware, token=token)
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
