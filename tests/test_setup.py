from pathlib import Path

from mypm.setup.setup import _BIN_DIR, mypm_bin, zshrc_block


def test_mypm_bin_returns_package_bin_dir():
    result = mypm_bin()
    assert result == _BIN_DIR
    assert result.parts[-2:] == ("bin", "latest")


def test_zshrc_block_contains_bin_path():
    bin_path = Path("/home/user/code/mypm/bin/latest")
    result = zshrc_block(bin_path)
    assert 'export MYPM_BIN="/home/user/code/mypm/bin/latest"' in result
    assert "aliases.sh" in result
