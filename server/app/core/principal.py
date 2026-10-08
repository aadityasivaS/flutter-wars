"""Shared authentication boundary; credential verification belongs to Module B."""

from app.contracts.principal import Principal
from app.core.errors import AppError


async def get_principal() -> Principal:
    """Dependency placeholder replaced/overridden by Module B after authentication.

    Module B may register its verified-principal dependency with FastAPI's
    dependency overrides or call sites can depend on its compatible provider.
    No token decoding is intentionally performed here.
    """
    raise AppError("AUTHENTICATION_REQUIRED", "Authentication is required.", 401)
