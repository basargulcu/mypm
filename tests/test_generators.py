import pytest

from mypm.compiler.generators import (
    generate_aliases,
    generate_definitions,
    generate_main,
)


@pytest.fixture
def config():
    return {
        "global": {
            "codebase_dir": "/home/user/code",
            "gcp_default_region": "us-central1",
        },
        "projects": [
            {"key": "mypm", "dir": "mypm"},
            {"key": "myapp", "dir": "myapp", "gcp_project_id": "my-gcp-id"},
        ],
    }


def test_generate_definitions_exports_codebase(config):
    result = generate_definitions(config)
    assert 'export CODEBASE="/home/user/code"' in result


def test_generate_definitions_exports_project_dirs(config):
    result = generate_definitions(config)
    assert "export MYPM_DIR=" in result
    assert "export MYAPP_DIR=" in result


def test_generate_definitions_gcp_project_ids(config):
    result = generate_definitions(config)
    assert 'gcp_project_ids[myapp]="my-gcp-id"' in result


def test_generate_definitions_excludes_non_gcp(config):
    result = generate_definitions(config)
    assert "gcp_project_ids[mypm]" not in result


def test_generate_main_uses_region(config):
    result = generate_main(config)
    assert 'local region="us-central1"' in result


def test_generate_main_default_region():
    config = {"global": {}, "projects": []}
    result = generate_main(config)
    assert 'local region="europe-west4"' in result


def test_generate_aliases_includes_project_aliases(config):
    result = generate_aliases(config)
    assert "alias mypm=" in result
    assert "alias myapp=" in result


def test_generate_definitions_dash_in_key_produces_valid_shell_var():
    config = {
        "global": {"codebase_dir": "/home/user/code"},
        "projects": [{"key": "my-project", "dir": "my-project"}],
    }
    result = generate_definitions(config)
    # Shell variable names cannot contain dashes — MY-PROJECT_DIR is invalid.
    # The export line must use an underscore: MY_PROJECT_DIR.
    assert "export MY-PROJECT_DIR=" not in result
    assert "export MY_PROJECT_DIR=" in result
