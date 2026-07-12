from mypm.compiler.assembler import _generate_aliases, _generate_main


def test_generate_main_uses_region():
    result = _generate_main("us-central1")
    assert 'local region="us-central1"' in result


def test_generate_main_default_region():
    result = _generate_main("europe-west4")
    assert 'local region="europe-west4"' in result


def test_generate_main_type_based_routing():
    result = _generate_main("europe-west4")
    assert "get_project_type" in result
    assert "terraform)" in result
    assert "python)" in result


def test_generate_aliases_sources_projects():
    sources = "source ${SCRIPT_DIR}/mypm.sh\nsource ${SCRIPT_DIR}/myapp.sh"
    result = _generate_aliases(sources)
    assert "source ${SCRIPT_DIR}/mypm.sh" in result
    assert "source ${SCRIPT_DIR}/myapp.sh" in result


def test_generate_aliases_contains_static_aliases():
    result = _generate_aliases("")
    assert "alias py=" in result
    assert "alias docker=" in result
