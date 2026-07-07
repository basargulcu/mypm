import pytest

from mypm.main import increment_version


@pytest.mark.parametrize(
    "version, expected",
    [
        ("v0.0.1", "v0.0.2"),
        ("v0.0.9", "v0.0.10"),
        ("v1.2.3", "v1.2.4"),
    ],
)
def test_increment_version(version, expected):
    assert increment_version(version) == expected
