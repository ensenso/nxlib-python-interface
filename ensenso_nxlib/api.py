# -*- coding: utf-8 -*-
from .exception import NxLibException, NxLibError

from ctypes import *

import ensenso_nxlib.helper as helper

__all__ = [
    "close_tcp_port",
    "connect",
    "disconnect",
    "erase",
    "finalize",
    "get_binary",
    "get_binary_info",
    "get_bool",
    "get_count",
    "get_debug_buffer",
    "get_debug_messages",
    "get_double",
    "get_int",
    "get_json",
    "get_json_meta",
    "get_name",
    "get_string",
    "get_type",
    "initialize",
    "is_current_lib_remote",
    "load_lib",
    "load_remote_lib",
    "make_unique_item",
    "open_tcp_port",
    "set_binary",
    "set_binary_formatted",
    "set_bool",
    "set_double",
    "set_int",
    "set_json",
    "set_null",
    "set_string",
    "translate_error_code",
    "wait_for_bool_value",
    "wait_for_change",
    "wait_for_double_value",
    "wait_for_int_value",
    "wait_for_string_value",
    "wait_for_type"
]

NXLIB_INTERNAL_ERROR = 7
NXLIB_OPERATION_SUCCEEDED = 0

NX_ERRORS = ["NxLibOperationSucceeded",
             "NxLibCannotCreateItem",
             "NxLibCouldNotInterpretJsonText",
             "NxLibItemInexistent",
             "",
             "NxLibNoDebugData",
             "NxLibCouldNotOpenPort",
             "NxLibInternalError",
             "NxLibTimeout",
             "NxLibNotConnected",
             "NxLibMethodInvalid",
             "NxLibBadRequest",
             "",
             "NxLibItemTypeNotCompatible",
             "NxLibInvalidBufferSize",
             "NxLibBufferTooSmall",
             "NxLibBufferNotDivisibleByElementSize",
             "NxLibExecutionFailed",
             "NxLibDebugMessageOverflow",
             "",
             "",
             "",
             "NxLibConnectionNotCompatible",
             "NxLibInitializationNotAllowed",
             "NxLibNestingLimitReached",
             "NxLibNoOpenProfileBlock"]


class _Nxlib():
    def __init__(self):
        self.is_remote = False
        self.lib_object = None

    def __del__(self):
        if self.is_remote:
            disconnect()
        else:
            finalize()
        if self.lib_object:
            del self.lib_object


# testing flag
__nx_testing__ = False

# global placeholder for the nxlib_instance
_nxlib = _Nxlib()


def _get_lib():
    # will default load the normal nxlib, if there has been no load_remote_lib beforehand!
    global _nxlib
    if _nxlib.lib_object is None:
        if _nxlib.is_remote:
            load_remote_lib()
        else:
            load_lib()
    return _nxlib.lib_object


def is_current_lib_remote():
    # For Testing and debug purpose
    global _nxlib
    return _nxlib.is_remote


def _lib_is_remote():
    global _nxlib
    return _nxlib.is_remote


def load_lib(path=None):
    global _nxlib
    if path is None:
        _nxlib.lib_object = CDLL(helper.get_lib_name())
    else:
        _nxlib.lib_object = CDLL(path)
    _nxlib.is_remote = False
    if _nxlib.lib_object is None:
        raise NxLibError("Could not load shared library")


def load_remote_lib(path=None):
    global _nxlib
    if path is None:
        _nxlib.lib_object = CDLL(helper.get_lib_name(True))
    else:
        _nxlib.lib_object = CDLL(path)
    _nxlib.is_remote = True
    if _nxlib.lib_object is None:
        raise NxLibError("Could not load shared remote library")


def check_return_code(error_code):
    if error_code != NXLIB_OPERATION_SUCCEEDED:
        raise NxLibException("", error_code)


def _set(f, path, value):
    path = helper.fix_string_encoding(path)
    error_code = c_int32(0)
    f(byref(error_code), path, value)
    return error_code.value


def set_null(path):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibSetNull
    f.argtypes = [POINTER(c_int32), c_char_p]
    error_code = c_int32(0)
    f(byref(error_code), path)
    return error_code.value


def set_int(path, value):
    f = _get_lib().nxLibSetInt
    f.argtypes = [POINTER(c_int32), c_char_p, c_int32]
    return _set(f, path, value)


def set_double(path, value):
    f = _get_lib().nxLibSetDouble
    f.argtypes = [POINTER(c_int32), c_char_p, c_double]
    return _set(f, path, value)


def set_bool(path, value):
    f = _get_lib().nxLibSetBool
    f.argtypes = [POINTER(c_int32), c_char_p, c_int32]
    return _set(f, path, value)


def set_string(path, value):
    value = helper.fix_string_encoding(value)
    f = _get_lib().nxLibSetString
    f.argtypes = [POINTER(c_int32), c_char_p, c_char_p]
    return _set(f, path, value)


def set_json(path, value, only_writeable_nodes=False):
    path = helper.fix_string_encoding(path)
    value = helper.fix_string_encoding(value)
    f = _get_lib().nxLibSetJson
    f.argtypes = [POINTER(c_int32), c_char_p, c_char_p, c_int32]
    error_code = c_int32(0)
    f(byref(error_code), path, value, only_writeable_nodes)
    return error_code.value


def set_binary(path, buffer, buffer_size):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibSetBinary
    f.argtypes = [POINTER(c_int32), c_char_p, POINTER(c_void_p), c_int32]
    buffer = cast(buffer, POINTER(c_void_p))
    error_code = c_int32(0)
    f(byref(error_code), path, buffer, buffer_size)
    return error_code.value


def set_binary_formatted(path, buffer, width, height, channel_count, bytes_per_element, is_float):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibSetBinaryFormatted
    f.argtypes = [POINTER(c_int32), c_char_p, POINTER(
        c_void_p), c_int32, c_int32, c_int32, c_int32, c_int32]
    buffer = cast(buffer, POINTER(c_void_p))
    error_code = c_int32(0)
    f(byref(error_code), path, buffer, width, height,
      channel_count, bytes_per_element, is_float)
    return error_code.value


def get_binary(path, destination_buffer, buffer_size):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibGetBinary
    f.argtypes = [POINTER(c_int32), c_char_p, POINTER(
        c_void_p), c_int32, POINTER(c_int32), POINTER(c_double)]
    error_code = c_int32(0)
    destination_buffer = cast(destination_buffer, POINTER(c_void_p))
    # destination_buffer = c_void_p(buffer_size) #(c_ubyte * buffer_size)()
    bytes_copied = c_int32(0)
    timestamp = c_double(0)

    f(byref(error_code), path, destination_buffer,
      buffer_size, byref(bytes_copied), byref(timestamp))

    return bytes_copied.value, timestamp.value, error_code.value


def get_binary_info(path):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibGetBinaryInfo
    f.argtypes = [POINTER(c_int32), c_char_p, POINTER(c_int32), POINTER(c_int32), POINTER(c_int32),
                  POINTER(c_int32), POINTER(c_int32), POINTER(c_double)]

    error_code = c_int32(0)
    width = c_int32(0)
    height = c_int32(0)
    channel_count = c_int32(0)
    bytes_per_element = c_int32(0)
    is_float = c_int32(0)
    timestamp = c_double(0)

    f(byref(error_code), path, byref(width), byref(height), byref(channel_count), byref(bytes_per_element),
      byref(is_float), byref(timestamp))

    return (width.value, height.value, channel_count.value, bytes_per_element.value,
            is_float.value == 1, timestamp.value, error_code.value)


def _get(f, path):
    path = helper.fix_string_encoding(path)
    error_code = c_int32(0)
    result = f(byref(error_code), path)
    return result, error_code.value


def get_type(path):
    f = _get_lib().nxLibGetType
    f.restype = c_int32
    f.argtypes = [POINTER(c_int32), c_char_p]
    return _get(f, path)


def get_int(path):
    f = _get_lib().nxLibGetInt
    f.restype = c_int32
    f.argtypes = [POINTER(c_int32), c_char_p]
    return _get(f, path)


def get_bool(path):
    f = _get_lib().nxLibGetBool
    f.restype = c_int32
    f.argtypes = [POINTER(c_int32), c_char_p]
    b, error_code = _get(f, path)
    return b == 1, error_code


def get_count(path):
    f = _get_lib().nxLibGetCount
    f.restype = c_int32
    f.argtypes = [POINTER(c_int32), c_char_p]
    return _get(f, path)


def get_double(path):
    f = _get_lib().nxLibGetDouble
    f.restype = c_double
    f.argtypes = [POINTER(c_int32), c_char_p]
    return _get(f, path)


def get_string(path):
    f = _get_lib().nxLibGetString
    f.restype = c_char_p
    f.argtypes = [POINTER(c_int32), c_char_p]
    s, error_code = _get(f, path)
    if s is not None:
        s = s.decode()
    return s, error_code


def get_name(path):
    f = _get_lib().nxLibGetName
    f.restype = c_char_p
    f.argtypes = [POINTER(c_int32), c_char_p]
    s, error_code = _get(f, path)
    if s is not None:
        s = s.decode()
    return s, error_code


def get_json(path, pretty_print, number_precision, scientific_number_format):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibGetJson
    f.restype = c_char_p
    f.argtypes = [POINTER(c_int32), c_char_p, c_int32, c_int32, c_int32]
    error_code = c_int32(0)
    result = f(byref(error_code), path, pretty_print,
               number_precision, scientific_number_format)
    if result is not None:
        result = result.decode()
    return result, error_code.value


def get_json_meta(path, num_levels, pretty_print, number_precision, scientific_number_format):
    path = helper.fix_string_encoding(path)

    f = _get_lib().nxLibGetJsonMeta
    f.restype = c_char_p
    f.argtypes = [POINTER(c_int32), c_char_p, c_int32,
                  c_int32, c_int32, c_int32]
    error_code = c_int32(0)
    result = f(byref(error_code), path, num_levels, pretty_print,
               number_precision, scientific_number_format)
    if result is not None:
        result = result.decode()
    return result, error_code.value


def erase(path):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibErase
    f.argtypes = [POINTER(c_int32), c_char_p]
    error_code = c_int32(0)
    f(byref(error_code), path)
    return error_code.value


def wait_for_change(path):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibWaitForChange
    f.argtypes = [POINTER(c_int32), c_char_p]
    error_code = c_int32(0)
    f(byref(error_code), path)
    return error_code.value


def wait_for_type(path, awaited_type, wait_for_equal):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibWaitForType
    f.argtypes = [POINTER(c_int32), c_char_p, c_int32, c_int32]
    error_code = c_int32(0)
    f(byref(error_code), path, awaited_type, wait_for_equal)
    return error_code.value


def wait_for_int_value(path, value, wait_for_equal):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibWaitForIntValue
    f.argtypes = [POINTER(c_int32), c_char_p, c_int32, c_int32]
    error_code = c_int32(0)
    f(byref(error_code), path, value, wait_for_equal)
    return error_code.value


def wait_for_string_value(path, value, wait_for_equal):
    path = helper.fix_string_encoding(path)
    value = helper.fix_string_encoding(value)
    f = _get_lib().nxLibWaitForStringValue
    f.argtypes = [POINTER(c_int32), c_char_p, c_char_p, c_int32]
    error_code = c_int32(0)
    f(byref(error_code), path, value, wait_for_equal)
    return error_code.value


def wait_for_double_value(path, value, wait_for_equal):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibWaitForDoubleValue
    f.argtypes = [POINTER(c_int32), c_char_p, c_double, c_int32]
    error_code = c_int32(0)
    f(byref(error_code), path, value, wait_for_equal)
    return error_code.value


def wait_for_bool_value(path, value, wait_for_equal):
    path = helper.fix_string_encoding(path)
    f = _get_lib().nxLibWaitForBoolValue
    f.argtypes = [POINTER(c_int32), c_char_p, c_int32, c_int32]
    error_code = c_int32(0)
    f(byref(error_code), path, value, wait_for_equal)
    return error_code.value


def make_unique_item(path, item_name):
    path = helper.fix_string_encoding(path)
    item_name = helper.fix_string_encoding(item_name)
    f = _get_lib().nxLibMakeUniqueItem
    f.restype = c_char_p
    f.argtypes = [POINTER(c_int32), c_char_p, c_char_p]
    error_code = c_int32(0)
    new_path = f(byref(error_code), path, item_name)
    if new_path is not None:
        new_path = new_path.decode()
    return new_path, error_code.value


def translate_error_code(return_code):
    if return_code < 0 or return_code > len(NX_ERRORS):
        return ''

    return NX_ERRORS[return_code]


def get_debug_messages():
    return_code = c_int32()
    f = _get_lib().nxLibGetDebugMessages
    f.restype = c_char_p
    f.argtypes = [POINTER(c_int32)]
    result = f(byref(return_code))
    check_return_code(return_code)
    return result.decode()


def get_debug_buffer():
    raise NotImplementedError()


def initialize(wait_for_initial_camera_refresh=True):
    if _lib_is_remote():
        raise NxLibError("Library is a remote nxlib. Only normal nxlib instances can use initialize.")
    f = _get_lib().nxLibInitialize
    return_code = c_int32()
    f.argtypes = [POINTER(c_int32), c_int32]
    f(byref(return_code), wait_for_initial_camera_refresh)
    check_return_code(return_code.value)


def finalize():
    if _lib_is_remote():
        raise NxLibError("Library is a remote nxlib. Only normal nxlib instances can use finalize.")
    f = _get_lib().nxLibFinalize
    return_code = c_int32()
    f.argtypes = [POINTER(c_int32)]
    f(byref(return_code))
    check_return_code(return_code.value)


def open_tcp_port(port_number=0, opened_port=0):
    if _lib_is_remote():
        raise NxLibError("Library is a remote nxlib. Only normal nxlib instances are allowed to open tcp ports.")
    f = _get_lib().nxLibOpenTcpPort
    return_code = c_int32()
    f.argtypes = [POINTER(c_int32), c_int32, c_int32]
    f(byref(return_code), port_number, opened_port)
    check_return_code(return_code.value)
    if __nx_testing__:
        print(port_number)


def close_tcp_port():
    if _lib_is_remote():
        raise NxLibError("Library is a remote NxLib. Only normal NxLib instances are allowed to close tcp ports.")
    f = _get_lib().nxLibCloseTcpPort
    return_code = c_int32()
    f.argtypes = [POINTER(c_int32)]
    f(byref(return_code))
    check_return_code(return_code.value)


def connect(hostname, port):
    if not _lib_is_remote():
        raise NxLibError("Cannot use connect function from a normal NxLib.")
    hostname = helper.fix_string_encoding(hostname)
    return_code = c_int32(0)
    f = _get_lib().nxLibConnect
    f.argtypes = [POINTER(c_int32), c_char_p, c_int32]
    f(byref(return_code), hostname, port)
    check_return_code(return_code.value)


def disconnect():
    if not _lib_is_remote():
        raise NxLibError("Cannot use disconnenct function from a normal NxLib.")
    f = _get_lib().nxLibDisconnect
    return_code = c_int32(0)
    f.argtypes = [POINTER(c_int32)]
    f(byref(return_code))
    check_return_code(return_code.value)
