from mypm.compiler import custom_aliases, custom_definitions, project_switcher


def _generate_definitions(project_snippet: str, custom_snippet: str) -> str:
    result = 'SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"\n\n' + project_snippet
    if custom_snippet:
        result += "\n\n" + custom_snippet + "\n"
    return result


def generate_definitions() -> str:
    return _generate_definitions(
        project_switcher.definitions_snippet(),
        custom_definitions.definitions_snippet(),
    )


def _generate_main() -> str:
    return """\
#!/bin/zsh

SUCCEED_MARKER=" \033[32m✅\033[0m"

get_gcp_project_id() {
    local input_project_key="${1}"
    echo "${gcp_project_ids[$input_project_key]}"
}

get_gcp_region() {
    local input_project_key="${1}"
    echo "${gcp_regions[$input_project_key]}"
}

manage_adc() {
    response=$(gcloud auth application-default print-access-token >/dev/null 2>&1 || echo "ADC not found")
    if [[ "$response" == "" ]]; then
        echo -n "ACD exists. "
    else
        echo "Require ADC - "
        gcloud auth login --update-adc
    fi
}

get_project_types() {
    local input_project_key="${1}"
    echo "${project_types[$input_project_key]}"
}

activate_terraform_project() {
    local project_key="$1"
}

activate_gcp_project() {
    local project_key="$1"

    echo -n "# Changing to $project_key directory..."
    cd ${project_dirs[$project_key]}
    echo "$SUCCEED_MARKER"

    echo -n "# Checking ADC..."
    manage_adc
    echo "$SUCCEED_MARKER"

    export GCP_PROJECT_ID=$(get_gcp_project_id $project_key)
    echo "# GCP_PROJECT_ID=${GCP_PROJECT_ID}"

    echo -n "# Setting gcloud config project to $GCP_PROJECT_ID... "
    gcloud config set project $GCP_PROJECT_ID > /dev/null 2>${SCRIPT_DIR}/logs/main.log
    echo "$SUCCEED_MARKER"

    export GCP_REGION=$(get_gcp_region $project_key)
    echo "# GCP_REGION=${GCP_REGION}"

    echo -n "# Setting gcloud config region to $GCP_REGION... "
    gcloud config set ai/region $GCP_REGION > /dev/null 2>>${SCRIPT_DIR}/logs/main.log
    echo "$SUCCEED_MARKER"
}

activate_python_project() {
    local project_key="$1"
    echo -n "# Changing to $project_key directory"
    cd ${project_dirs[$project_key]}
    echo "$SUCCEED_MARKER"

    echo -n "# Activating python venv"
    source .venv/bin/activate > /dev/null 2>>${SCRIPT_DIR}/logs/main.log
    echo "$SUCCEED_MARKER"
}

init() {
    mkdir -p ${SCRIPT_DIR}/logs
    touch ${SCRIPT_DIR}/logs/main.log
}

main() {
    init

    local types_str=$(get_project_types $1)
    for project_type in ${(s: :)types_str}; do
        case "$project_type" in
            terraform)
                activate_terraform_project $1
                ;;
            gcp)
                activate_gcp_project $1
                ;;
            python)
                activate_python_project $1
                ;;
            *)
                echo "Unknown project type: $project_type"
                ;;
        esac
    done
}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source ${SCRIPT_DIR}/definitions.sh
main $@
"""


def generate_main() -> str:
    return _generate_main()


def _generate_aliases(sources_snippet: str, custom_aliases_snippet: str) -> str:
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
"""
    result = (
        'SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"\n'
        "\n"
        "# Imports\n"
        "source ${SCRIPT_DIR}/definitions.sh\n"
        "\n"
        "# Projects\n" + sources_snippet + "\n" + static
    )
    if custom_aliases_snippet:
        result += "\n" + custom_aliases_snippet + "\n"
    return result


def generate_aliases() -> str:
    return _generate_aliases(
        project_switcher.aliases_sources_snippet(),
        custom_aliases.aliases_snippet(),
    )
