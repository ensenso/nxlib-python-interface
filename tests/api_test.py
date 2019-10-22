import pytest
from ensenso_nxlib.item import NxLibItem
from ensenso_nxlib.constants import *

import ensenso_nxlib.api as nxlib


def test_load_nxlib():
    nxlib.load_lib()


def test_load_nxlib_with_wrong_path():
    with pytest.raises(Exception) as e_info:
        nxlib.load_lib("This should not work!")


def test_set_int():
    nxlib.set_int("/test", 15)
    a = nxlib.get_int("/test")
    value = a[0]
    error_code = a[1]
    assert (value is 15)
    assert (error_code is 0)


def test_set_int_with_float():
    with pytest.raises(Exception) as e_info:
        nxlib.set_int("/test", 15.5)
        assert (e_info == "wrong type")


def test_set_null():
    nxlib.set_null("/test")
    node_type = nxlib.get_type("/test")
    assert (node_type[0] == NXLIB_ITEM_TYPE_NULL)
    assert (node_type[1] == 0)


def test_set_double():
    nxlib.set_double("/test", 1.1)
    double_test = nxlib.get_double("/test")
    assert (double_test[0] == 1.1)
    assert (double_test[1] == 0)


def test_set_bool():
    nxlib.set_bool("/test", True)
    bool_test = nxlib.get_bool("/test")
    assert (bool_test[0] == True)
    assert (bool_test[1] == 0)
