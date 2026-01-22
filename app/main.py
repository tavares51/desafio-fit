from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import settings
from app.common.errors import AppError
from app.common.logging import configure_logging

# Routers (vão existir nesses arquivos)
from app.modules.auth.router import router as auth_router
from app.modules.books.router import router as books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Hook de startup/shutdown.
    - conecta/valida integrações
    - executa checagens
    - inicia recursos (se necessário)
    """
    # configure_logging()
    logging.getLogger(__name__).info("Starting API...")

    yield

    logging.getLogger(__name__).info("Shutting down API...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.exception_handler(AppError)
    async def app_error_handler(_, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"message": exc.message, "details": exc.details}},
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_, exc: Exception):
        logging.getLogger(__name__).exception("Unhandled error: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"error": {"message": "Erro interno.", "details": {}}},
        )

    app.include_router(auth_router)
    app.include_router(books_router, prefix="/books", tags=["Books"])

    return app


app = create_app()
