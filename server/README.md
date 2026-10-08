# GDG Flutter Workshop Backend

Module A provides the intentionally thin FastAPI foundation shared by all backend modules. It does not own business entities or authentication logic.

## Prerequisites and installation

Use Python 3.11+ and [uv](https://docs.astral.sh/uv/) (or install the dependencies from `pyproject.toml` with your preferred Python environment manager).

```powershell
uv sync --all-groups
Copy-Item .env.example .env
```

Set `DATABASE_URL` in `.env`. For local development this can be a direct PostgreSQL/Neon SQLAlchemy URL. In deployment it should be the provider-supplied Cloudflare Hyperdrive route to Neon; no provider-specific adapter is hard-coded here.

## Run and test

```powershell
uv run uvicorn app.main:app --reload
uv run pytest
uv run ruff check .
```

`GET /health` returns `{"status":"ok"}` for process liveness. `GET /ready` verifies the configured database path and returns `{"status":"ready"}` or a safe `503` error.

## Structure

- `app/core`: settings, database lifecycle, error mapping, logging hooks, principal boundary.
- `app/contracts`: stable public shared contracts.
- `app/modules/foundation`: health/readiness router only.
- `tests`: Foundation contract tests.

Future modules expose an `APIRouter` and add it explicitly in `app/modules/__init__.py`. For example:

```python
router = APIRouter(prefix="/example")


@router.get("/")
def example():
    return {"status": "ok"}
```

See [docs/module-a.md](docs/module-a.md) for integration boundaries.
