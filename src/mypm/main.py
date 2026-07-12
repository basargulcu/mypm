import shutil

from mypm.compiler import assembler, project_switcher
from mypm.setup_mypm.setup import ZSHRC, _ZSHRC_MARKER, mypm_bin, zshrc_block
from mypm.settings import ROOT

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


def compile_version(version: str):
    output_dir = ROOT / "bin" / version
    latest_dir = ROOT / "bin" / "latest"

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    (output_dir / "definitions.sh").write_text(assembler.generate_definitions())

    main_sh = output_dir / "main.sh"
    main_sh.write_text(assembler.generate_main())
    main_sh.chmod(0o755)

    (output_dir / "aliases.sh").write_text(assembler.generate_aliases())

    for key, content in project_switcher.project_scripts():
        (output_dir / f"{key}.sh").write_text(content)

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
