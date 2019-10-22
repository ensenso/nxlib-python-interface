import pytest

import ensenso_nxlib
from ensenso_nxlib import NxLibException


def test_exception_message():
    error_code = ensenso_nxlib.constants.NXLIB_ITEM_TYPE_NOT_COMPATIBLE
    error_text = ensenso_nxlib.api.translate_error_code(error_code)
    dummy_path = "/dummy_path"

    exception = None
    try:
        raise NxLibException(dummy_path, error_code)
    except NxLibException as e:
        exception = e

    assert exception.get_item_path() == dummy_path
    assert exception.get_error_code() == error_code
    assert exception.get_error_text() == error_text
    assert str(exception) == "NxLib error {} ({}) for item {}".format(error_code, error_text, dummy_path)
