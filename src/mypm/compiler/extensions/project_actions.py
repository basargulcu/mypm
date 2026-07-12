def get_cases(config: dict, actions_config: dict) -> dict[str, list[dict]]:
    actions_by_project = actions_config.get("project_actions", {})
    result = {}
    for project in config["projects"]:
        key = project["key"]
        if key in actions_by_project:
            result[key] = [
                {"name": a["name"], "command": a["command"]}
                for a in actions_by_project[key]
            ]
    return result
