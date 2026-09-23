FROM node:24-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/index.html frontend/tsconfig.json frontend/vite.config.ts ./
COPY frontend/src ./src
RUN npm run build

FROM python:3.14-slim AS backend-build
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /app/backend
COPY backend/pyproject.toml backend/uv.lock backend/.python-version backend/README.md ./
COPY backend/src ./src
RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev --no-editable

FROM python:3.14-slim
ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=backend-build /opt/venv /opt/venv
COPY --from=frontend-build /app/frontend/dist /app/static
RUN useradd --create-home --uid 10001 app
USER app
EXPOSE 8000
CMD ["uvicorn", "template_fastapi_react.main:app", "--host", "0.0.0.0", "--port", "8000"]
