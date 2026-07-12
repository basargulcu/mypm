import yaml

from mypm.settings import CUSTOM_ALIASES_CONFIG_PATH


def _load_custom_aliases() -> dict:
    if not CUSTOM_ALIASES_CONFIG_PATH.exists():
        return {}
    with open(CUSTOM_ALIASES_CONFIG_PATH) as f:
        return (yaml.safe_load(f) or {}).get("custom_aliases", {})


def _aliases_snippet(aliases: dict) -> str:
    if not aliases:
        return ""
    lines = ["# Custom"]
    for name, cmd in aliases.items():
        lines.append(f'alias {name}="{cmd}"')
    return "\n".join(lines)


def aliases_snippet() -> str:
    return _aliases_snippet(_load_custom_aliases())
