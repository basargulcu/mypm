import yaml

from mypm.compiler import project_switcher
from mypm.settings import GLOBAL_CONFIG_PATH


def _load_global() -> dict:
    with open(GLOBAL_CONFIG_PATH) as f:
        return yaml.safe_load(f) or {}


def generate_definitions() -> str:
    snippet = project_switcher.definitions_snippet()
    return 'SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"\n\n' + snippet


def _generate_main(region: str) -> str:
    return f"""\
#!/bin/zsh

SUCCEED_MARKER=" \033[32m✅\033[0m"

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
    echo "$SUCCEED_MARKER"

    echo -n "# Checking ADC..."
    manage_adc
    echo "$SUCCEED_MARKER"

    export GCP_PROJECT_ID=$(get_gcp_project_id $project_key)
    echo "# GCP_PROJECT_ID=${{GCP_PROJECT_ID}}"

    echo -n "# Setting gcloud config project to $GCP_PROJECT_ID... "
    gcloud config set project $GCP_PROJECT_ID > /dev/null 2>${{SCRIPT_DIR}}/logs/main.log
    echo "$SUCCEED_MARKER"

    export GCP_REGION=$(get_gcp_region)
    echo "# GCP_REGION=${{GCP_REGION}}"

    echo -n "# Setting gcloud config region to $GCP_REGION... "
    gcloud config set ai/region $GCP_REGION > /dev/null 2>>${{SCRIPT_DIR}}/logs/main.log
    echo "$SUCCEED_MARKER"
}}

activate_python_project() {{
    local project_key="$1"
    echo -n "# Changing to $project_key directory"
    cd ${{project_dirs[$project_key]}}
    echo "$SUCCEED_MARKER"

    echo -n "# Activating python venv"
    source .venv/bin/activate > /dev/null 2>>${{SCRIPT_DIR}}/logs/main.log
    echo "$SUCCEED_MARKER"
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


def generate_main() -> str:
    global_config = _load_global()
    region = global_config.get("gcp_default_region", "europe-west4")
    return _generate_main(region)


def _generate_aliases(sources_snippet: str) -> str:
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
        "# Projects\n" + sources_snippet + "\n" + static
    )


def generate_aliases() -> str:
    return _generate_aliases(project_switcher.aliases_sources_snippet())
