import pytest

from mypm.compiler.extensions.project_actions import get_cases


@pytest.fixture
def config():
    return {
        "global": {"codebase_dir": "/home/user/code"},
        "projects": [
            {"key": "mypm", "dir": "mypm"},
            {"key": "other", "dir": "other"},
        ],
    }


@pytest.fixture
def actions_config():
    return {
        "project_actions": {
            "mypm": [
                {"name": "compile", "command": "_mypm compile"},
                {"name": "test", "command": "uv run pytest tests/"},
            ]
        }
    }


def test_get_cases_returns_cases_for_configured_project(config, actions_config):
    result = get_cases(config, actions_config)
    assert "mypm" in result
    assert len(result["mypm"]) == 2


def test_get_cases_maps_name_and_command(config, actions_config):
    result = get_cases(config, actions_config)
    compile_case = result["mypm"][0]
    assert compile_case["name"] == "compile"
    assert compile_case["command"] == "_mypm compile"


def test_get_cases_skips_unconfigured_project(config, actions_config):
    result = get_cases(config, actions_config)
    assert "other" not in result
