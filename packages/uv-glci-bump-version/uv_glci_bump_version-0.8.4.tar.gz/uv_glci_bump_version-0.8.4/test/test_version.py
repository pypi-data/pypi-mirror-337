import pytest

from uv_glci_bump_version import version


def test_load():
    with pytest.raises(RuntimeError, match='no value'):
        version.Version.load('')

    with pytest.raises(RuntimeError, match='3 parts'):
        version.Version.load('1.2.3.4')

    with pytest.raises(RuntimeError, match='3 parts'):
        version.Version.load('1.2')

    with pytest.raises(RuntimeError, match='integer'):
        version.Version.load('1.2.a')

    assert version.Version.load('1.2.3') == version.Version(1, 2, 3)


def test_dump():
    assert version.Version.load('1.2.3').dump() == '1.2.3'


def test_major() -> None:
    major = version.IncrementKind.MAJOR
    assert version.Version(1, 0, 0).incremented(major) == version.Version(2, 0, 0)
    assert version.Version(2, 57, 2).incremented(major) == version.Version(3, 0, 0)
    assert version.Version(0, 0, 0).incremented(major) == version.Version(1, 0, 0)
    assert version.Version(0, 0, 17).incremented(major) == version.Version(1, 0, 0)


def test_minor() -> None:
    minor = version.IncrementKind.MINOR
    assert version.Version(1, 0, 0).incremented(minor) == version.Version(1, 1, 0)
    assert version.Version(1, 12, 0).incremented(minor) == version.Version(1, 13, 0)
    assert version.Version(3, 0, 5).incremented(minor) == version.Version(3, 1, 0)
    assert version.Version(0, 3, 0).incremented(minor) == version.Version(0, 4, 0)
    assert version.Version(0, 0, 2).incremented(minor) == version.Version(0, 1, 0)


def test_patch() -> None:
    patch = version.IncrementKind.PATCH
    assert version.Version(1, 0, 0).incremented(patch) == version.Version(1, 0, 1)
    assert version.Version(5, 37, 0).incremented(patch) == version.Version(5, 37, 1)
    assert version.Version(0, 0, 0).incremented(patch) == version.Version(0, 0, 1)
    assert version.Version(0, 0, 99).incremented(patch) == version.Version(0, 0, 100)
