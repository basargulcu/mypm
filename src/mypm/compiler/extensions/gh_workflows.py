def get_cases(config: dict, gh_config: dict) -> dict[str, list[dict]]:
    workflows_by_project = gh_config.get("gh_workflows", {})
    result = {}
    for project in config["projects"]:
        key = project["key"]
        if key in workflows_by_project:
            result[key] = [_to_case(w) for w in workflows_by_project[key]]
    return result


def _to_case(workflow: dict) -> dict:
    inputs = " ".join(f"-f {k}={v}" for k, v in workflow.get("inputs", {}).items())
    command = f"gh workflow run {workflow['workflow']} --repo {workflow['repo']}"
    if inputs:
        command += f" {inputs}"
    return {"name": workflow["name"], "command": command}
