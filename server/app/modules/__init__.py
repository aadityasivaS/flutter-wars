"""Explicit module-router registration."""

from fastapi import FastAPI

from app.modules.foundation.router import router as foundation_router


def register_modules(app: FastAPI) -> None:
    """Register Foundation routes; future modules add one explicit router here."""
    app.include_router(foundation_router)
