from mypm.compiler.assembler import (
    _generate_aliases,
    _generate_definitions,
    _generate_main,
)


def test_generate_definitions_includes_project_snippet():
    result = _generate_definitions("# Project DIRs\nexport CODEBASE=/home", "")
    assert "SCRIPT_DIR=" in result
    assert "export CODEBASE=/home" in result


def test_generate_definitions_includes_custom_snippet():
    result = _generate_definitions("", '# Custom\nexport MY_VAR="val"')
    assert 'export MY_VAR="val"' in result


def test_generate_main_type_based_routing():
    result = _generate_main()
    assert "get_project_types" in result
    assert "terraform)" in result
    assert "gcp)" in result
    assert "python)" in result


def test_generate_main_region_lookup_by_project_key():
    result = _generate_main()
    assert "gcp_regions[$input_project_key]" in result


def test_generate_aliases_sources_projects():
    sources = "source ${SCRIPT_DIR}/mypm.sh\nsource ${SCRIPT_DIR}/myapp.sh"
    result = _generate_aliases(sources, "")
    assert "source ${SCRIPT_DIR}/mypm.sh" in result
    assert "source ${SCRIPT_DIR}/myapp.sh" in result


def test_generate_aliases_contains_static_aliases():
    result = _generate_aliases("", "")
    assert "alias adc=" in result
    assert "alias tf_init=" in result


def test_generate_aliases_includes_custom_snippet():
    result = _generate_aliases("", '# Custom\nalias py="source .venv/bin/activate"')
    assert "alias py=" in result
