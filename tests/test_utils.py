from unittest.mock import patch
from utils.utils import valid_name, get_user_input


def test_valid_name():
    assert valid_name("Jo") == False
    assert valid_name("Joe") == True

    assert valid_name("Joe_") == False
    assert valid_name("_Joe") == False

    assert valid_name("Joe-Smith") == False
    assert valid_name("Joe_Smith") == True
    assert valid_name("Joe_Smith0") == True

    assert valid_name("Joe__Smith") == False


def test_get_user_input():
    with patch("builtins.input", side_effect=["Test Input"]):
        prompt = "Enter something: "
        result = get_user_input(prompt)
        assert result == "Test Input"

    with patch("builtins.input", side_effect=["", "Test Input"]):
        prompt = "Enter something: "
        result = get_user_input(prompt)
        assert result == "Test Input"
