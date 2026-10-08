# GDG Flutter Workshop Backend

Module A provides the intentionally thin FastAPI foundation shared by all backend modules. It does not own business entities or authentication logic.

## Prerequisites and installation

Use Python 3.11+ and [uv](https://docs.astral.sh/uv/) (or install the dependencies from `pyproject.toml` with your preferred Python environment manager).

```powershell
uv sync --all-groups
Copy-Item .env.example .env
```

Set `DATABASE_URL` in `.env`. For local development, start PostgreSQL in Docker:

```powershell
docker run --name flutter-wars-postgres `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=flutter_wars `
  -p 5432:5432 `
  -d postgres:18
```

The `.env.example` URL points to this container. Stop and restart it with:

```powershell
docker stop flutter-wars-postgres
docker start flutter-wars-postgres
```

For deployment, set `DATABASE_URL` to the provider-supplied Cloudflare Hyperdrive route to Neon; no provider-specific adapter is hard-coded here.

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

## Module C IDE synchronization

Module C adds organizer-managed team API keys and `GET /ide/state`. The IDE must send `X-Team-API-Key`; this is a separate credential from participant JWTs. See [docs/module-c.md](docs/module-c.md) for endpoint details, integration boundaries, and the local fake-inventory test setup. Run its coverage with `uv run pytest tests/test_ide_sync.py`.
