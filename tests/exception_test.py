import pytest
from nxlib import NxLibException


def test_message():
    error_message = None
    test_message = "This is a message"
    error_code = 42
    dummy_path = "/dummy_path"
    should_be_message = "This is a message at {} - error_code {}".format(dummy_path, error_code)
    try:
        raise NxLibException(test_message, dummy_path, error_code)
    except NxLibException as e:
        error_message = e.get_error_text()

    assert error_message == should_be_message
