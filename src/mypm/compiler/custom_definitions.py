import yaml

from mypm.settings import CUSTOM_DEFINITIONS_CONFIG_PATH


def _load_custom_definitions() -> dict:
    if not CUSTOM_DEFINITIONS_CONFIG_PATH.exists():
        return {}
    with open(CUSTOM_DEFINITIONS_CONFIG_PATH) as f:
        return (yaml.safe_load(f) or {}).get("custom_definitions", {})


def _definitions_snippet(definitions: dict) -> str:
    if not definitions:
        return ""
    lines = ["# Custom"]
    for name, value in definitions.items():
        lines.append(f'export {name}="{value}"')
    return "\n".join(lines)


def definitions_snippet() -> str:
    return _definitions_snippet(_load_custom_definitions())
