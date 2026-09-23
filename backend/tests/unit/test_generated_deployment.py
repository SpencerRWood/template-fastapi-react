"""Check the rendered full-stack workflow, not only its template source."""

import runpy
import shutil
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]


def test_generated_analytics_portal_deployment(tmp_path: Path) -> None:
    project = tmp_path / "analytics-portal"
    shutil.copytree(
        ROOT,
        project,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            "node_modules",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
        ),
    )
    runpy.run_path(str(project / "scripts/rename_project.py"))["main"](
        "analytics-portal"
    )

    metadata = tomllib.loads((project / "backend/pyproject.toml").read_text())
    assert metadata["project"]["name"] == "analytics-portal"
    assert (project / "backend/src/analytics_portal/main.py").is_file()
    assert (
        '"name": "analytics-portal"'
        in (project / "frontend/package-lock.json").read_text()
    )
    workflow = (project / ".github/workflows/release.yml").read_text()
    parsed = yaml.safe_load(workflow)
    jobs = parsed["jobs"]
    assert jobs["release"]["uses"].endswith("/release.yml@v1")
    assert jobs["container"]["uses"].endswith("/container-release.yml@v1")
    assert jobs["promotion"]["uses"].endswith("/promote-container-to-dev.yml@v2")
    assert jobs["container"]["with"]["image_name"] == "analytics-portal"
    assert jobs["promotion"]["with"]["image_name"] == "analytics-portal"
    assert jobs["promotion"]["with"]["image_key"] == "analytics_portal_image_ref"
    assert jobs["promotion"]["with"]["version_image_digest"] == (
        "${{ needs.container.outputs.version_image_digest }}"
    )
    assert (
        "INFRASTRUCTURE_PR_TOKEN"
        in jobs["promotion"]["secrets"]["infrastructure_token"]
    )
    assert yaml.safe_load((project / ".github/workflows/validate.yml").read_text())[
        "jobs"
    ]["validation"]["uses"].endswith("/validate.yml@v1")
    for forbidden in (
        "environment_file",
        "promotion_branch_prefix",
        "pr_title_template",
        "gh pr",
        ":latest",
    ):
        assert forbidden not in workflow
