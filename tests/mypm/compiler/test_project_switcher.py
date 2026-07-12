from mypm.compiler.project_switcher import (
    _aliases_sources_snippet,
    _definitions_snippet,
    _project_script,
    _shell_var_name,
)


def global_config():
    return {"codebase_dir": "/home/user/code", "gcp_default_region": "us-central1"}


def projects():
    return [
        {"key": "mypm", "dir": "mypm", "type": "python"},
        {
            "key": "myapp",
            "dir": "myapp",
            "type": "terraform",
            "gcp_project_id": "my-gcp-id",
        },
    ]


def test_shell_var_name_replaces_dash():
    assert _shell_var_name("my-project") == "MY_PROJECT"


def test_shell_var_name_uppercases():
    assert _shell_var_name("myapp") == "MYAPP"


def test_definitions_exports_codebase():
    result = _definitions_snippet(global_config(), projects())
    assert 'export CODEBASE="/home/user/code"' in result


def test_definitions_exports_project_dirs():
    result = _definitions_snippet(global_config(), projects())
    assert "export MYPM_DIR=" in result
    assert "export MYAPP_DIR=" in result


def test_definitions_project_types():
    result = _definitions_snippet(global_config(), projects())
    assert 'project_types[mypm]="python"' in result
    assert 'project_types[myapp]="terraform"' in result


def test_definitions_gcp_project_ids():
    result = _definitions_snippet(global_config(), projects())
    assert 'gcp_project_ids[myapp]="my-gcp-id"' in result


def test_definitions_excludes_non_gcp():
    result = _definitions_snippet(global_config(), projects())
    assert "gcp_project_ids[mypm]" not in result


def test_definitions_dash_in_key_produces_valid_shell_var():
    result = _definitions_snippet(
        {"codebase_dir": "/home/user/code"},
        [{"key": "my-project", "dir": "my-project"}],
    )
    assert "export MY-PROJECT_DIR=" not in result
    assert "export MY_PROJECT_DIR=" in result


def test_aliases_sources_snippet():
    result = _aliases_sources_snippet(projects())
    assert "source ${SCRIPT_DIR}/mypm.sh" in result
    assert "source ${SCRIPT_DIR}/myapp.sh" in result


def test_project_script():
    result = _project_script({"key": "mypm", "dir": "mypm"})
    assert "unalias mypm 2>/dev/null" in result
    assert "mypm()" in result
    assert 'source ${SCRIPT_DIR}/main.sh mypm "$@"' in result
