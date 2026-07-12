import shutil
from pathlib import Path

import yaml

from mypm.compiler.generators import (
    generate_aliases,
    generate_definitions,
    generate_main,
    generate_project_script,
)
from mypm.setup_mypm.setup import ZSHRC, _ZSHRC_MARKER, mypm_bin, zshrc_block
from mypm.settings import CONFIG_PATH, ROOT

_VERSION_FILE = ROOT / "bin" / "latest" / ".version"


def get_latest_version() -> str | None:
    if _VERSION_FILE.exists():
        return _VERSION_FILE.read_text().strip()
    return None


def increment_version(version: str) -> str:
    prefix, *parts = version.lstrip("v").split(".")
    parts = [prefix] + parts
    parts[-1] = str(int(parts[-1]) + 1)
    return "v" + ".".join(parts)


def compile_version(version: str, config_path: Path = CONFIG_PATH):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    output_dir = ROOT / "bin" / version
    latest_dir = ROOT / "bin" / "latest"

    output_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "definitions.sh": generate_definitions(config),
        "main.sh": generate_main(config),
        "aliases.sh": generate_aliases(config),
    }

    for name, content in files.items():
        path = output_dir / name
        path.write_text(content)
        if name == "main.sh":
            path.chmod(0o755)

    for project in config["projects"]:
        key = project["key"]
        (output_dir / f"{key}.sh").write_text(generate_project_script(project))

    (output_dir / ".version").write_text(version)

    if latest_dir.exists():
        shutil.rmtree(latest_dir)
    shutil.copytree(output_dir, latest_dir)


def setup_mypm() -> bool:
    bin_path = mypm_bin()
    block = zshrc_block(bin_path)

    existing = ZSHRC.read_text() if ZSHRC.exists() else ""
    if _ZSHRC_MARKER in existing:
        return False

    with open(ZSHRC, "a") as f:
        f.write(f"\n{block}")
    return True
