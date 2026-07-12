def shell_var_name(key: str) -> str:
    return key.replace("-", "_").upper()


def generate_project_script(project: dict) -> str:
    key = project["key"]
    return f"""\
unalias {key} 2>/dev/null
{key}() {{
    source ${{SCRIPT_DIR}}/main.sh {key} "$@"
}}
"""


def generate_definitions(config):
    g = config["global"]
    projects = config["projects"]

    lines = ['SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"', ""]
    lines.append("# Project DIRs")
    lines.append(f'export CODEBASE="{g["codebase_dir"]}"')

    for p in projects:
        key_upper = shell_var_name(p["key"])
        lines.append(f'export {key_upper}_DIR="${{CODEBASE}}/{p["dir"]}"')

    lines.append("typeset -A project_dirs")
    for p in projects:
        key_upper = shell_var_name(p["key"])
        lines.append(f"project_dirs[{p['key']}]=${{{key_upper}_DIR}}")

    lines.append("")
    lines.append("# Mappings")
    lines.append("typeset -A project_types")
    for p in projects:
        if "type" in p:
            lines.append(f'project_types[{p["key"]}]="{p["type"]}"')

    lines.append("typeset -A gcp_project_ids")
    for p in projects:
        if "gcp_project_id" in p:
            lines.append(f'gcp_project_ids[{p["key"]}]="{p["gcp_project_id"]}"')

    lines.append("# Misc")
    lines.append("")

    return "\n".join(lines)


def generate_main(config):
    region = config["global"].get("gcp_default_region", "europe-west4")

    return f"""\
#!/bin/zsh

get_gcp_project_id() {{
    local input_project_key="${{1}}"
    echo "${{gcp_project_ids[$input_project_key]}}"
}}

get_gcp_region() {{
    local region="{region}"
    echo "${{region}}"
}}

manage_adc() {{
    response=$(gcloud auth application-default print-access-token >/dev/null 2>&1 || echo "ADC not found")
    if [[ "$response" == "" ]]; then
        echo -n "ACD exists. "
    else
        echo "Require ADC - "
        gcloud auth login --update-adc
    fi
}}

get_project_type() {{
    local input_project_key="${{1}}"
    echo "${{project_types[$input_project_key]}}"
}}

activate_gcp_project() {{
    local project_key="$1"

    echo -n "# Changing to $project_key directory..."
    cd ${{project_dirs[$project_key]}}
    echo "DONE!"

    echo -n "# Checking ADC..."
    manage_adc
    echo "DONE!"

    export GCP_PROJECT_ID=$(get_gcp_project_id $project_key)
    echo "# GCP_PROJECT_ID=${{GCP_PROJECT_ID}}"

    echo -n "# Setting gcloud config project to $GCP_PROJECT_ID... "
    gcloud config set project $GCP_PROJECT_ID > /dev/null 2>${{SCRIPT_DIR}}/logs/main.log
    echo "DONE!"

    export GCP_REGION=$(get_gcp_region)
    echo "# GCP_REGION=${{GCP_REGION}}"

    echo -n "# Setting gcloud config region to $GCP_REGION... "
    gcloud config set ai/region $GCP_REGION > /dev/null 2>>${{SCRIPT_DIR}}/logs/main.log
    echo "DONE!"
}}

activate_python_project() {{
    local project_key="$1"
    echo -n "# Changing to $project_key directory..."
    cd ${{project_dirs[$project_key]}}
    echo "DONE!"

    echo -n "# Activating python venv..."
    py > /dev/null 2>>${{SCRIPT_DIR}}/logs/main.log
    echo "DONE!"
}}

init() {{
    mkdir -p ${{SCRIPT_DIR}}/logs
    touch ${{SCRIPT_DIR}}/logs/main.log
}}

main() {{
    init

    local project_type=$(get_project_type $1)
    case "$project_type" in
        terraform)
            activate_gcp_project $1
            ;;
        python)
            activate_python_project $1
            ;;
        *)
            echo "Unknown project type: $project_type"
            ;;
    esac
}}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source ${{SCRIPT_DIR}}/definitions.sh
main $@
"""


def generate_aliases(config):
    projects = config["projects"]
    source_lines = "\n".join(f"source ${{SCRIPT_DIR}}/{p['key']}.sh" for p in projects)

    static = r"""
# GCP
alias _adc="gcloud auth application-default login"
alias _gl="gcloud auth login"
alias _gp="gcloud config set project ${1}"
alias adc="gcloud auth login --update-adc"
alias gcp="gcloud storage cp -r"
alias gsync="gcloud storage rsync -r"
alias gls="gcloud storage ls"
alias gdu="gcloud storage du"
alias grm="gcloud storage rm -r"
alias g="cat ${SCRIPT_DIR}/alias.sh | grep gcloud"

# Terraform
alias tf="cat ${SCRIPT_DIR}/alias.sh | grep tf_"
alias tf_cd="cd ${BARTOS_DIR}/infra"
alias tf_init="terraform init"
alias tf_plan="tf_init; terraform plan"

# Custom
alias help="cat $SCRIPT_DIR/aliases.sh"
alias def="cat $SCRIPT_DIR/definitions.sh | grep DEFAULT"
alias my="echo '# source ~/.zshrc'; source ~/.zshrc"
alias py="echo '# source .venv/bin/activate'; source .venv/bin/activate"
alias cl="ollama launch claude"
alias docker="podman"
alias coffee="echo '# caffeinate -di'; caffeinate -di"
"""

    return (
        'SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"\n'
        "\n"
        "# Projects\n" + source_lines + "\n" + static
    )
