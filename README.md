# template-fastapi-react

A thin full-stack template with a FastAPI backend, a React + TypeScript
frontend, `uv`, Vite, Ruff, mypy, pytest, ESLint, Prettier, Vitest,
pre-commit, GitHub Actions, Docker Compose, and semantic-release wired
together.

## Intended Use

Use this template for small full-stack applications that need a typed FastAPI
backend and a lightweight React frontend. The repository infrastructure is
ready for local development and release automation; application behavior is intentionally
minimal.

## Repository Layout

```text
backend/
  src/template_fastapi_react/
    api/routes/
    models/
    services/
    config.py
    exceptions.py
    main.py
  tests/
  pyproject.toml
  .python-version
frontend/
  src/
    api/
    components/
    hooks/
    pages/
    types/
    App.tsx
    main.tsx
  tests/
  package.json
  tsconfig.json
  vite.config.ts
.github/workflows/
docker-compose.yml
```

The backend follows the existing Python template family. The frontend keeps a
small Vite application shell and leaves API-specific behavior under
`frontend/src/api/`.

## Prerequisites

- Python 3.14
- `uv`
- Node.js 24
- npm
- Docker, if using Docker Compose

## Backend Setup

```sh
cd backend
uv sync --frozen --group dev
```

Run backend checks:

```sh
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv build
```

Run the backend locally:

```sh
uv run uvicorn template_fastapi_react.main:app --reload
```

## Frontend Setup

```sh
cd frontend
npm install
```

Run frontend checks:

```sh
npm run lint
npm run format
npm run typecheck
npm test -- --run
npm run build
```

Run the frontend locally:

```sh
npm run dev
```

## Docker Compose

From the repository root:

```sh
docker compose up --build
```

This starts:

- backend: `http://localhost:8000`
- frontend: `http://localhost:5173`

No database, cache, proxy, worker, or queue is included by default.

## Full Repository Validation

From the repository root:

```sh
cd backend && uv sync --frozen --group dev
cd ../frontend && npm install
cd ..
uv run --directory backend pre-commit run --all-files
docker compose config
```

## Pre-commit

Install hooks from the repository root after backend and frontend dependencies
are installed:

```sh
uv run --directory backend pre-commit install
```

Pre-commit runs the same file hygiene hooks as the Python templates, backend
Ruff lint/format, and frontend Prettier formatting.

## Release Validation

The release workflow validates the backend, frontend, and repository hooks
before semantic-release:

- Backend: `uv sync --frozen --group dev`, mypy, pytest, `uv build`
- Frontend: `npm ci`, ESLint, TypeScript, Vitest, Vite build
- Repository: pre-commit

Backend Ruff and frontend Prettier run through pre-commit.

## Versioning And Release

The repository uses one version, stored in `backend/pyproject.toml`.
semantic-release follows the Python template conventions:

- conventional commits
- tags like `v0.0.1`
- `fix:` and `perf:` create patch releases
- `feat:` creates minor releases while the template remains `0.x`
- release assets are built with `uv build`

The frontend package version starts at the same value for search-and-replace
clarity, but the default release workflow is repository-level rather than
separate frontend/backend release tracks.

## Automatic dev deployment

Pull requests use centralized validation. After a merge to `main`, the shared
workflow creates a semantic release, publishes an immutable GHCR image with
the built React frontend and FastAPI backend, and opens an infrastructure
promotion PR for its digest-qualified reference. Infrastructure validates and
automatically merges that PR, makes its patch release, and deploys to dev.
The application repository owns the image and promotion request;
infrastructure owns the dev image pin, Compose, Ansible, runtime secrets,
migrations, health checks, and deployment policy.

Before the first deployment, onboard the application in
`SpencerRWood/infrastructure`: add `<app>_image_ref` to `environments/dev.yml`,
the service and Compose definition, Ansible/runtime configuration and secrets,
plus migrations, health checks, and ingress where applicable. Set the initial
image pin to a valid digest-qualified image. This is a separate infrastructure
change; the template does not create it.

Add the generated repository secret `INFRASTRUCTURE_PR_TOKEN`: a fine-grained
token scoped only to `SpencerRWood/infrastructure` with Contents read/write,
Pull requests read/write, Commit statuses read, and Metadata read. Do not
commit the token. The promotion workflow consumes it through its standard
`infrastructure_token` mapping.

## Copy and rename

After creating a repository from this template, run
`python3 scripts/rename_project.py analytics-portal`, replacing
`analytics-portal` with your lowercase repository slug. The script reads the
existing `backend/pyproject.toml` project name and updates the Python package,
npm lockfile, production Dockerfile, workflow `image_name`, and snake-case
`image_key` together. Use the same slug for the GitHub repository. Then run
`uv lock` in `backend`, `npm install` in `frontend`, and the backend, frontend,
pre-commit, and Docker Compose checks.
