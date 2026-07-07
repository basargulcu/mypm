from pathlib import Path

from mypm.installer.install import mypm_bin, zshrc_block


def test_mypm_bin_resolves_path():
    config = {
        "global": {"codebase_dir": "/home/user/code"},
        "projects": [{"key": "mypm", "dir": "mypm"}],
    }
    result = mypm_bin(config)
    assert result == Path("/home/user/code/mypm/bin/latest")


def test_mypm_bin_missing_project_raises():
    config = {
        "global": {"codebase_dir": "/home/user/code"},
        "projects": [],
    }
    try:
        mypm_bin(config)
        assert False, "Expected StopIteration"
    except StopIteration:
        pass


def test_zshrc_block_contains_bin_path():
    bin_path = Path("/home/user/code/mypm/bin/latest")
    result = zshrc_block(bin_path)
    assert 'export MYPM_BIN="/home/user/code/mypm/bin/latest"' in result
    assert "aliases.sh" in result
