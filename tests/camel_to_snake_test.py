import pytest
from ensenso_nxlib.helper import convert_camel_to_lower_snake, convert_camel_to_upper_snake, fix_nxlib_prefix


def test_camel_to_lower_snake():
    nxlib_constant = "itmNxLibConstant"
    converted_string = convert_camel_to_lower_snake(nxlib_constant)
    assert converted_string == "itm_nx_lib_constant"

    nxlib_constant = "another42CamelCase"
    converted_string = convert_camel_to_lower_snake(nxlib_constant)
    assert converted_string == "another42_camel_case"

    nxlib_constant = "UpperCamelCase"
    converted_string = convert_camel_to_lower_snake(nxlib_constant)
    assert converted_string == "upper_camel_case"


def test_camel_to_upper_snake():
    nxlib_constant = "lowerCamelCase"
    converted_string = convert_camel_to_upper_snake(nxlib_constant)
    assert converted_string == "LOWER_CAMEL_CASE"

    nxlib_constant = "UpperCamelCase"
    converted_string = convert_camel_to_upper_snake(nxlib_constant)
    assert converted_string == "UPPER_CAMEL_CASE"


def test_nxlib_prefix():
    constant = 'NX_LIB_ANYTHING'
    expected = 'NXLIB_ANYTHING'

    result = fix_nxlib_prefix(constant)
    assert expected == result
