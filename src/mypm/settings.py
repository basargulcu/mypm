from pathlib import Path

from environs import Env

env = Env()
env.read_env()

ROOT = Path(__file__).parent.parent.parent

CONFIG_PATH = env.path("MYPM_CONFIG", default=ROOT / "config" / "projects.yml")
