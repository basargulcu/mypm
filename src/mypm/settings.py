from pathlib import Path

from environs import Env

env = Env()
env.read_env()

ROOT = Path(__file__).parent.parent.parent

GLOBAL_CONFIG_PATH = env.path(
    "MYPM_GLOBAL_CONFIG", default=ROOT / "config" / "global.yml"
)
CONFIG_PATH = env.path("MYPM_CONFIG", default=ROOT / "config" / "projects.yml")
CUSTOM_ALIASES_CONFIG_PATH = env.path(
    "MYPM_CUSTOM_ALIASES_CONFIG", default=ROOT / "config" / "custom_aliases.yml"
)
