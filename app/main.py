"""CloudOps Deployment API - stateless application for CI/CD demonstration."""
from __future__ import annotations

import logging
import os
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

APP_NAME = "CloudOps Deployment API"
APP_VERSION = "1.0.0"
BUILD_SHA = os.getenv("BUILD_SHA", "local")
APP_ENV = os.getenv("APP_ENV", "development")

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("cloudops_api")

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "A stateless demonstration API used to validate a secure CI/CD workflow, "
        "container image publication and Cloud Run deployment."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

RESOURCES: list[dict[str, str]] = [
    {
        "id": "github",
        "name": "GitHub",
        "role": "Source control",
        "description": "Stores versioned application source code and workflow definitions.",
    },
    {
        "id": "actions",
        "name": "GitHub Actions",
        "role": "Pipeline automation",
        "description": "Runs linting, tests, security checks, image publication and deployment.",
    },
    {
        "id": "docker",
        "name": "Docker",
        "role": "Containerisation",
        "description": "Packages the application and runtime dependencies into an image.",
    },
    {
        "id": "artifact-registry",
        "name": "Artifact Registry",
        "role": "Image registry",
        "description": "Stores immutable, commit-tagged container images.",
    },
    {
        "id": "cloud-run",
        "name": "Cloud hosting",
        "role": "Cloud Run",
        "description": "Runs the container as a managed HTTPS service with autoscaling.",
    },
]


class EchoRequest(BaseModel):
    """Validated request body for the POST demonstration endpoint."""

    message: str = Field(min_length=1, max_length=200)
    correlation_id: str | None = Field(default=None, max_length=64)


@app.middleware("http")
async def add_security_headers_and_request_id(request: Request, call_next):
    """Add basic response hardening and a non-sensitive correlation identifier."""
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    logger.info(
        "http_request method=%s path=%s status_code=%s request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        request_id,
    )
    return response


@app.get("/", tags=["service"])
def root() -> dict[str, Any]:
    """Return service metadata and useful endpoint links."""
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "status": "operational",
        "links": {
            "health": "/healthz",
            "info": "/api/v1/info",
            "resources": "/api/v1/resources",
            "documentation": "/docs",
        },
    }


@app.get("/healthz", tags=["health"])
def health_check() -> dict[str, str]:
    """Lightweight liveness endpoint used by Cloud Run and smoke tests."""
    return {"status": "ok"}


@app.get("/api/v1/info", tags=["service"])
def service_info() -> dict[str, str]:
    """Expose non-secret build metadata for deployment verification."""
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "environment": APP_ENV,
        "build_sha": BUILD_SHA,
        "platform": "cloud-run" if os.getenv("K_SERVICE") else "local-or-container",
    }


@app.get("/api/v1/resources", tags=["resources"])
def list_resources() -> dict[str, Any]:
    """List the components represented by this CI/CD demonstration."""
    return {"count": len(RESOURCES), "items": RESOURCES}


@app.get("/api/v1/resources/{resource_id}", tags=["resources"])
def get_resource(resource_id: str) -> dict[str, str]:
    """Return one resource or a conventional 404 response."""
    for resource in RESOURCES:
        if resource["id"] == resource_id:
            return resource
    raise HTTPException(status_code=404, detail="Resource not found")


@app.post("/api/v1/echo", tags=["testing"])
def echo_payload(payload: EchoRequest) -> dict[str, Any]:
    """Validate and echo a request body to demonstrate POST and schema validation."""
    return {
        "received": True,
        "message": payload.message,
        "correlation_id": payload.correlation_id,
    }
