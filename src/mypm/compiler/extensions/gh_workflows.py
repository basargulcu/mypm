from pathlib import Path


def _workflow_cases(workflows: list) -> str:
    lines = []
    for w in workflows:
        inputs = " ".join(f"-f {k}={v}" for k, v in w.get("inputs", {}).items())
        gh_cmd = f"gh workflow run {w['workflow']} --repo {w['repo']}"
        if inputs:
            gh_cmd += f" {inputs}"
        lines.append(f"        {w['name']})")
        lines.append(f"            {gh_cmd}")
        lines.append("            ;;")
    return "\n".join(lines)


def generate_project_script_with_workflows(project: dict, workflows: list) -> str:
    key = project["key"]
    cases = _workflow_cases(workflows)
    return f"""\
unalias {key} 2>/dev/null
{key}() {{
    case "$1" in
{cases}
        *)
            source ${{SCRIPT_DIR}}/main.sh {key} "$@"
            ;;
    esac
}}
"""


def apply_gh_workflows(config: dict, gh_config: dict, output_dir: Path) -> None:
    workflows_by_project = gh_config.get("gh_workflows", {})
    for project in config["projects"]:
        key = project["key"]
        if key in workflows_by_project:
            script = generate_project_script_with_workflows(
                project, workflows_by_project[key]
            )
            (output_dir / f"{key}.sh").write_text(script)
