# Repository Guidance

## Purpose and boundaries
- Keep this FastAPI and React template reusable after project rename.
- `backend/` owns the API and migrations; `frontend/` owns the typed UI.

## Development
- Preserve the documented rename path and the boundary between application code and deploy-time configuration.
- Use Alembic for schema changes introduced by a cloned application.

## Validation
- In `backend/`, run `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy`, and `uv run pytest`.
- In `frontend/`, run `npm run lint`, `npm run format`, `npm run typecheck`, `npm test -- --run`, and `npm run build`.
- From the root, run `uv run --directory backend pre-commit run --all-files` and `docker compose config` when applicable.

## Architecture constraints
- Keep frontend and backend contracts synchronized without baking runtime secrets into the image.
- Avoid adding deployment-target assumptions to template defaults.

## Safety
- Keep example environment values non-sensitive and portable after cloning.

## Branching strategy

- This repository uses **trunk-based development**. Create short-lived change branches from current `main` and target PRs to `main`.
- Follow the [canonical branching and delivery policy](https://github.com/SpencerRWood/codex-config/blob/main/docs/branching-policy.md), available through the installed codex-config source path. Verify the strategy, release association, fetched base and PR target before implementation and record them in Story evidence. Story completion does not authorize publication or deployment; retain existing review, CI, security and rollback requirements.
- This classification applies to maintenance of the template repository. Replace it with the new repository's classification during project creation; applications must use release-branch integration before Story development begins.
