from mypm.compiler.custom_aliases import _aliases_snippet


def test_aliases_snippet_generates_alias_lines():
    aliases = {"py": "source .venv/bin/activate", "docker": "podman"}
    result = _aliases_snippet(aliases)
    assert 'alias py="source .venv/bin/activate"' in result
    assert 'alias docker="podman"' in result


def test_aliases_snippet_includes_custom_header():
    result = _aliases_snippet({"py": "source .venv/bin/activate"})
    assert "# Custom" in result


def test_aliases_snippet_empty_returns_empty_string():
    assert _aliases_snippet({}) == ""
