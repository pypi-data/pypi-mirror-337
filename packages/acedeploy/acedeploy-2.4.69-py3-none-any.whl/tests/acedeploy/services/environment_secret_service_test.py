import pytest
from acedeploy.services.secret_service import EnvironmentSecretService


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("logkey", "logkey-value")
    monkeypatch.setenv("mappedlogkey", "mappedlogkey-value")
    monkeypatch.setenv("mixedCaseKey", "mixed-value")
    monkeypatch.setenv("UPPERCASEKEY", "uppercase-value")
    monkeypatch.setenv("lowercasekey", "lowercase-value")


def test_get_secret_with_no_key_should_return_secret():
    # arrange
    sut = EnvironmentSecretService()
    test_key = "logkey"
    expected = "logkey-value"

    # act
    result = sut.get_secret(test_key)

    # assert
    assert result == expected


def test_get_secret_with_keymap_should_return_mapped_secret():
    # arrange
    key_map = {"logkey": "mappedlogkey"}
    sut = EnvironmentSecretService(key_map)
    test_key = "logkey"
    expected = "mappedlogkey-value"

    # act
    result = sut.get_secret(test_key)

    # assert
    assert result == expected


def test_get_secret_with_nokeymap_andlowerkey_should_return_lowercase_secret():
    # arrange
    sut = EnvironmentSecretService()
    test_key = "lowercasekey"  # mixed case key
    expected = "lowercase-value"

    # act
    result = sut.get_secret(test_key)

    # assert
    assert result == expected


def test_get_secret_with_nokeymap_upperkey_should_return_uppercase_secret():
    # arrange
    sut = EnvironmentSecretService()
    test_key = "UPPERCASEKEY"  # lowercase key
    expected = "uppercase-value"

    # act
    result = sut.get_secret(test_key)

    # assert
    assert result == expected


def test_get_secret_with_nokeympa_nosecret_should_return_none():
    # arrange
    sut = EnvironmentSecretService()
    test_key = "some-non-existant-key"

    # act - assert

    with pytest.raises(ValueError):
        _ = sut.get_secret(test_key)
