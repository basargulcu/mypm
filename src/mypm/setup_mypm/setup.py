from pathlib import Path

ZSHRC = Path.home() / ".zshrc"
_ZSHRC_MARKER = "# mypm"

_BIN_DIR = Path(__file__).parent.parent.parent.parent / "bin" / "latest"


def mypm_bin() -> Path:
    return _BIN_DIR


def zshrc_block(bin_path: Path) -> str:
    return f"""\
{_ZSHRC_MARKER}
export MYPM_BIN="{bin_path}"
if [ -f ${{MYPM_BIN}}/aliases.sh ]; then source ${{MYPM_BIN}}/aliases.sh; fi
"""
