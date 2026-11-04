# backend/src/backend/telemetry.py
import logging
import sys
import uuid
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from pythonjsonlogger import jsonlogger
from prometheus_fastapi_instrumentator import Instrumentator

def setup_logging():
    """Configures structured JSON logging for production observability."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers:
        logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Silence overly verbose third-party loggers
    for log_name in ("uvicorn.access", "httpcore", "httpx", "chromadb"):
        logging.getLogger(log_name).setLevel(logging.WARNING)

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Injects a unique request ID for distributed tracing and context logging."""
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        # Bind context to log record factory or pass downstream headers
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

def init_telemetry(app: FastAPI):
    """Initializes logging middleware and Prometheus metrics instrumentation."""
    setup_logging()
    app.add_middleware(RequestIDMiddleware)
    
    # Expose /metrics endpoint for Prometheus scrapers
    Instrumentator().instrument(app).expose(app, tags=["Monitoring"])