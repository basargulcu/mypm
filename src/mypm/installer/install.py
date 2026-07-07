from pathlib import Path

ZSHRC = Path.home() / ".zshrc"
_ZSHRC_MARKER = "# mypm"


def mypm_bin(config: dict) -> Path:
    codebase_dir = Path(config["global"]["codebase_dir"])
    mypm_project = next(p for p in config["projects"] if p["key"] == "mypm")
    return codebase_dir / mypm_project["dir"] / "bin" / "latest"


def zshrc_block(bin_path: Path) -> str:
    return f"""\
# mypm
export MYPM_BIN="{bin_path}"
if [ -f ${{MYPM_BIN}}/aliases.sh ]; then source ${{MYPM_BIN}}/aliases.sh; fi
"""
