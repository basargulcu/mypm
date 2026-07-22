import yaml

from mypm.settings import CONFIG_PATH, GLOBAL_CONFIG_PATH


def _load_global() -> dict:
    with open(GLOBAL_CONFIG_PATH) as f:
        return yaml.safe_load(f) or {}


def _load_projects() -> list:
    with open(CONFIG_PATH) as f:
        return (yaml.safe_load(f) or {}).get("projects", [])


def _shell_var_name(key: str) -> str:
    return key.replace("-", "_").upper()


def _definitions_snippet(global_config: dict, projects: list) -> str:
    codebase_dir = global_config.get("codebase_dir", "")
    lines = ["# Project DIRs", f'export CODEBASE="{codebase_dir}"']

    for p in projects:
        key_upper = _shell_var_name(p["key"])
        lines.append(f'export {key_upper}_DIR="${{CODEBASE}}/{p["dir"]}"')

    lines.append("typeset -A project_dirs")
    for p in projects:
        key_upper = _shell_var_name(p["key"])
        lines.append(f"project_dirs[{p['key']}]=${{{key_upper}_DIR}}")

    lines.append("")
    lines.append("# Mappings")
    lines.append("typeset -A project_types")
    for p in projects:
        if "types" in p:
            lines.append(f'project_types[{p["key"]}]="{" ".join(p["types"])}"')

    lines.append("typeset -A gcp_project_ids")
    for p in projects:
        if "gcp_project_id" in p:
            lines.append(f'gcp_project_ids[{p["key"]}]="{p["gcp_project_id"]}"')

    lines.append("typeset -A gcp_regions")
    for p in projects:
        if "gcp_region" in p:
            lines.append(f'gcp_regions[{p["key"]}]="{p["gcp_region"]}"')

    return "\n".join(lines)


def definitions_snippet() -> str:
    return _definitions_snippet(_load_global(), _load_projects())


def _aliases_sources_snippet(projects: list) -> str:
    return "\n".join(f"source ${{SCRIPT_DIR}}/{p['key']}.sh" for p in projects)


def aliases_sources_snippet() -> str:
    return _aliases_sources_snippet(_load_projects())


def _project_script(project: dict) -> str:
    key = project["key"]
    commands = project.get("commands", [])
    cases = ""
    for cmd in commands:
        cases += f"        {cmd['name']})\n            {cmd['cmd']}\n            ;;\n"
    return f"""\
unalias {key} 2>/dev/null
{key}() {{
    case "$1" in
{cases}        *)
            source ${{SCRIPT_DIR}}/main.sh {key} "$@"
            ;;
    esac
}}
"""


def project_scripts() -> list[tuple[str, str]]:
    return [(_p["key"], _project_script(_p)) for _p in _load_projects()]
