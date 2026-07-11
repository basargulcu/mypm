import pytest

from mypm.compiler.extensions.gh_workflows import (
    apply_gh_workflows,
    generate_project_script_with_workflows,
)


@pytest.fixture
def project():
    return {"key": "myapp", "dir": "myapp"}


@pytest.fixture
def workflows():
    return [
        {
            "name": "deploy",
            "workflow": "deploy.yml",
            "repo": "org/myapp",
            "inputs": {"environment": "production", "branch": "main"},
        }
    ]


def test_generates_function_with_workflow_case(project, workflows):
    result = generate_project_script_with_workflows(project, workflows)
    assert "unalias myapp 2>/dev/null" in result
    assert "myapp()" in result
    assert "deploy)" in result
    assert "gh workflow run deploy.yml --repo org/myapp" in result
    assert "-f environment=production" in result
    assert "-f branch=main" in result


def test_generates_default_fallback(project, workflows):
    result = generate_project_script_with_workflows(project, workflows)
    assert "source ${SCRIPT_DIR}/main.sh myapp" in result
    assert '"$@"' in result


def test_workflow_without_inputs(project):
    workflows = [{"name": "test", "workflow": "ci.yml", "repo": "org/myapp"}]
    result = generate_project_script_with_workflows(project, workflows)
    assert "gh workflow run ci.yml --repo org/myapp" in result


def test_apply_gh_workflows_writes_enhanced_script(tmp_path):
    config = {
        "global": {"codebase_dir": "/home/user/code"},
        "projects": [
            {"key": "myapp", "dir": "myapp"},
            {"key": "other", "dir": "other"},
        ],
    }
    gh_config = {
        "gh_workflows": {
            "myapp": [{"name": "deploy", "workflow": "deploy.yml", "repo": "org/myapp"}]
        }
    }

    # Write base scripts first (as compile_version would)
    (tmp_path / "myapp.sh").write_text("base")
    (tmp_path / "other.sh").write_text("base")

    apply_gh_workflows(config, gh_config, tmp_path)

    myapp_script = (tmp_path / "myapp.sh").read_text()
    assert "deploy)" in myapp_script
    assert "gh workflow run" in myapp_script

    # other.sh should be untouched
    assert (tmp_path / "other.sh").read_text() == "base"
