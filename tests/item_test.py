import pytest
from ensenso_nxlib.constants import *
from ensenso_nxlib import NxLibItem


def test_is_true():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW][ITM_SHOW_CAMERAS].is_bool() == True


def test_is_false():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_COMPUTE_DISPARITY_MAP][ITM_STATIC_BUFFERS].is_bool() == False


def test_is_not_bool():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW].is_bool() == False


def test_is_number():
    assert NxLibItem()[ITM_CALIBRATION][ITM_PATTERN][ITM_GRID_SPACING].is_number() == True


def test_is_not_number():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW][ITM_SHOW_CAMERAS].is_number() == False


def test_is_string():
    assert NxLibItem()[ITM_CALIBRATION][ITM_PATTERN][ITM_TYPE].is_string() == True


def test_is_not_string():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW].is_string() == False


def test_is_null():
    assert NxLibItem()[ITM_CALIBRATION][ITM_ASSEMBLY_CALIBRATION].is_null() == True


def test_is_not_null():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW].is_null() == False


def test_is_object():
    assert NxLibItem()[ITM_CALIBRATION][ITM_PATTERN].is_object() == True


def test_is_not_object():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW][ITM_SHOW_CAMERAS].is_object() == False


def test_is_array():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW][ITM_SIZE].is_array() == True


def test_is_not_array():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW].is_array() == False


def test_type():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW][ITM_SIZE].type() == 5


def test_exists():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS][ITM_RENDER_VIEW].exists() == True


def test_doesnt_exist():
    assert NxLibItem()[ITM_DEFAULT_PARAMETERS]["Blubb"].exists() == False


def test_as_json():
    NxLibItem().as_json()


def test_set_and_return():
    NxLibItem()["test"]["item"] = 42
    assert NxLibItem()["test"]["item"].is_number()

    value = NxLibItem()["test"]["item"].as_int()
    assert value == 42
