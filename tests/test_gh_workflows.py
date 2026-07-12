import pytest

from mypm.compiler.extensions.gh_workflows import get_cases


@pytest.fixture
def config():
    return {
        "global": {"codebase_dir": "/home/user/code"},
        "projects": [
            {"key": "myapp", "dir": "myapp"},
            {"key": "other", "dir": "other"},
        ],
    }


@pytest.fixture
def gh_config():
    return {
        "gh_workflows": {
            "myapp": [
                {
                    "name": "deploy",
                    "workflow": "deploy.yml",
                    "repo": "org/myapp",
                    "inputs": {"environment": "production", "branch": "main"},
                }
            ]
        }
    }


def test_get_cases_returns_cases_for_configured_project(config, gh_config):
    result = get_cases(config, gh_config)
    assert "myapp" in result
    assert result["myapp"][0]["name"] == "deploy"


def test_get_cases_builds_gh_command(config, gh_config):
    result = get_cases(config, gh_config)
    command = result["myapp"][0]["command"]
    assert "gh workflow run deploy.yml --repo org/myapp" in command
    assert "-f environment=production" in command
    assert "-f branch=main" in command


def test_get_cases_skips_unconfigured_project(config, gh_config):
    result = get_cases(config, gh_config)
    assert "other" not in result


def test_get_cases_workflow_without_inputs(config):
    gh_config = {
        "gh_workflows": {
            "myapp": [{"name": "test", "workflow": "ci.yml", "repo": "org/myapp"}]
        }
    }
    result = get_cases(config, gh_config)
    assert result["myapp"][0]["command"] == "gh workflow run ci.yml --repo org/myapp"
