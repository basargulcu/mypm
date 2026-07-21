from mypm.compiler.custom_definitions import _definitions_snippet


def test_definitions_snippet_generates_export_lines():
    definitions = {"MY_VAR": "some_value", "ANOTHER_VAR": "another_value"}
    result = _definitions_snippet(definitions)
    assert 'export MY_VAR="some_value"' in result
    assert 'export ANOTHER_VAR="another_value"' in result


def test_definitions_snippet_includes_custom_header():
    result = _definitions_snippet({"MY_VAR": "val"})
    assert "# Custom" in result


def test_definitions_snippet_empty_returns_empty_string():
    assert _definitions_snippet({}) == ""
