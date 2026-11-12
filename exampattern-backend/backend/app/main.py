from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.core.logging import setup_logging
from app.core.rate_limit import limiter


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logging()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="AI-powered exam-pattern analysis and practice paper generation (practice tool only).",
        lifespan=lifespan,
    )
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/health", tags=["meta"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
