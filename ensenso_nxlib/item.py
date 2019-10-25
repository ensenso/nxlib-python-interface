import ensenso_nxlib.api as nxlib
from .exception import NxLibError, NxLibException

import numpy as np

__all__ = ["NxLibItem"]

NXLIB_ITEM_TYPE_INVALID = 0
NXLIB_ITEM_TYPE_NULL = 1
NXLIB_ITEM_TYPE_NUMBER = 2
NXLIB_ITEM_TYPE_STRING = 3
NXLIB_ITEM_TYPE_BOOL = 4
NXLIB_ITEM_TYPE_ARRAY = 5
NXLIB_ITEM_TYPE_OBJECT = 6

NXLIB_ITEM_INEXISTENT = 3
NXLIB_OPERATION_SUCCEEDED = 0
NXLIB_BAD_REQUEST = 11
NXLIB_ITEM_TYPE_NOT_COMPATIBLE = 13

NXLIB_ITEM_SEPARATOR = '/'
NXLIB_INDEX_ESCAPE_CHAR = '\\'


class NxLibItem:
    def __init__(self, path=None):
        if path is None:
            path = ""
        self.path = path
        pass

    def _check_return_code(self, error_code):
        if error_code != NXLIB_OPERATION_SUCCEEDED:
            raise NxLibException(self.path, error_code)

    def __getitem__(self, value):
        if type(value) is str:
            return NxLibItem(self.path + NXLIB_ITEM_SEPARATOR + value)
        elif type(value) is int:
            return NxLibItem(self.path + NXLIB_ITEM_SEPARATOR + NXLIB_INDEX_ESCAPE_CHAR + str(value))
        else:
            raise NxLibError("Value cannot be added to NxLib path")

    def __setitem__(self, path, value):
        self[path].set_t(value)

    def _compare(self, value):
        item_value = self.as_t()
        if type(item_value) == type(value):
            if item_value == value:
                return 0
            elif item_value < value:
                return -1
            else:
                return 1
        else:
            raise NxLibException(self.path, NXLIB_ITEM_TYPE_NOT_COMPATIBLE)

    def __lt__(self, value):
        return self._compare(value) < 0

    def __le__(self, value):
        return self._compare(value) <= 0

    def __eq__(self, value):
        return self._compare(value) == 0

    def __ne__(self, value):
        return self._compare(value) != 0

    def __gt__(self, value):
        return self._compare(value) > 0

    def __ge__(self, value):
        return self._compare(value) >= 0

    def __lshift__(self, other):
        if type(other) is str:
            self.set_json(str, True)
        elif isinstance(other, NxLibItem):
            self.set_json(other.as_json(), True)
        else:
            raise NxLibException(self.path, NXLIB_ITEM_TYPE_NOT_COMPATIBLE)

    def set_t(self, value):
        if value is None:
            self.set_null()
        elif type(value) is int:
            if (value > 2147483647 or value < -2147483648):
                raise NotImplementedError()
            else:
                self.set_int(value)
        elif type(value) is str:
            self.set_string(value)
        elif type(value) is bool:
            self.set_bool(value)
        elif type(value) is float:
            self.set_double(value)
        else:
            raise NxLibException(self.path, NXLIB_ITEM_TYPE_NOT_COMPATIBLE)

    def set_null(self):
        error_code = nxlib.set_null(self.path)
        self._check_return_code(error_code)

    def set_double(self, value):
        error_code = nxlib.set_double(self.path, value)
        self._check_return_code(error_code)

    def set_int(self, value):
        error_code = nxlib.set_int(self.path, value)
        self._check_return_code(error_code)

    def set_bool(self, value):
        error_code = nxlib.set_bool(self.path, value)
        self._check_return_code(error_code)

    def set_string(self, value):
        error_code = nxlib.set_string(self.path, value)
        self._check_return_code(error_code)

    def set_json(self, value, only_writable_nodes=False):
        error_code = nxlib.set_json(self.path, value, only_writable_nodes)
        self._check_return_code(error_code)

    def set_binary_data(self, buffer, buffer_size_or_width=0, height=0,
                        channel_count=0, bytes_per_element=0, is_float=0):
        if buffer_size_or_width == 0:
            self.set_binary_data_from_cv(buffer)
        else:

            if (channel_count > 0):
                width = buffer_size_or_width
                error_code = nxlib.set_binary_formatted(self.path, buffer, width, height,
                                                        channel_count, bytes_per_element,
                                                        is_float)
            else:  # not formatted
                buffer_size = buffer_size_or_width
                error_code = nxlib.set_binary(self.path, buffer, buffer_size)
            self._check_return_code(error_code)

    def set_binary_data_from_cv(self, mat):
        if type(mat).__name__ != 'ndarray':
            raise NxLibException(self.path, NXLIB_ITEM_TYPE_NOT_COMPATIBLE)

        channel_count = mat.shape[2]
        is_float = False
        if mat.dtype == 'uint8' or mat.dtype == 'int8':
            bpe = 1
        elif mat.dtype == 'uint16' or mat.dtype == 'int16':
            bpe = 2
        elif mat.dtype == 'int32':
            bpe = 4
        elif mat.dtype == 'float32':
            bpe = 4
            is_float = True
        elif mat.dtype == 'float64':
            bpe = 8
            is_float = True

        buffer = np.ctypeslib.as_ctypes(mat)
        error_code = nxlib.set_binary_formatted(
            self.path, buffer, mat.shape[1], mat.shape[0], channel_count, bpe, is_float)
        self._check_return_code(error_code)

    def get_binary_data(self):
        buffer = self._create_buffer()
        buffer_size = buffer.shape[0] * buffer.shape[1] * buffer.shape[2] * buffer.dtype.itemsize
        cbuffer = np.ctypeslib.as_ctypes(buffer)
        _, _, error_code = nxlib.get_binary(
            self.path, cbuffer, buffer_size)
        self._check_return_code(error_code)
        return buffer

    def _create_buffer(self):
        width, height, channel_count, bpe, is_float, _, _ = self.get_binary_data_info()
        nptype = np.uint8
        if is_float:
            if bpe == 4:
                nptype = np.float32
            elif bpe == 8:
                nptype = np.float64
        else:
            if bpe == 1:
                nptype = np.uint8
            elif bpe == 2:
                nptype = np.int16
            elif bpe == 4:
                nptype = np.int32

        image_buffer = np.zeros(
            (height, width, channel_count), nptype, order='C')

        return image_buffer

    def get_binary_data_info(self):
        width, height, channel_count, bpe, is_float, timestamp, error_code = nxlib.get_binary_info(
            self.path)
        self._check_return_code(error_code)
        return width, height, channel_count, bpe, is_float, timestamp, error_code

    def as_t(self):
        if self.is_null():
            return None
        elif self.is_number():
            return self.as_double()
        elif self.is_string():
            return self.as_string()
        elif self.is_bool():
            return self.as_bool()
        else:
            raise NxLibException(self.path, NXLIB_ITEM_TYPE_NOT_COMPATIBLE)

    def as_int(self):
        i, error_code = nxlib.get_int(self.path)
        self._check_return_code(error_code)
        return i

    def as_bool(self):
        b, error_code = nxlib.get_bool(self.path)
        self._check_return_code(error_code)
        return b

    def as_double(self):
        d, error_code = nxlib.get_double(self.path)
        self._check_return_code(error_code)
        return d

    def as_string(self):
        s, error_code = nxlib.get_string(self.path)
        self._check_return_code(error_code)
        return s

    def count(self):
        c, error_code = nxlib.get_count(self.path)
        self._check_return_code(error_code)
        return c

    def as_json(self, pretty_print=1, number_precision=2, scientific_number_format=0):
        json, error_code = nxlib.get_json(
            self.path, pretty_print, number_precision, scientific_number_format)
        self._check_return_code(error_code)
        return json

    def as_json_meta(self, num_levels=1, pretty_print=1, number_precision=2, scientific_number_format=0):
        json_meta, error_code = nxlib.get_json_meta(self.path, num_levels, pretty_print, number_precision,
                                                    scientific_number_format)
        self._check_return_code(error_code)
        return json_meta

    def is_null(self):
        t, error_code = nxlib.get_type(self.path)
        self._check_return_code(error_code)
        return t == NXLIB_ITEM_TYPE_NULL

    def is_string(self):
        t, error_code = nxlib.get_type(self.path)
        self._check_return_code(error_code)
        return t == NXLIB_ITEM_TYPE_STRING

    def is_number(self):
        t, error_code = nxlib.get_type(self.path)
        self._check_return_code(error_code)
        return t == NXLIB_ITEM_TYPE_NUMBER

    def is_bool(self):
        t, error_code = nxlib.get_type(self.path)
        self._check_return_code(error_code)
        return t == NXLIB_ITEM_TYPE_BOOL

    def is_array(self):
        t, error_code = nxlib.get_type(self.path)
        self._check_return_code(error_code)
        return t == NXLIB_ITEM_TYPE_ARRAY

    def is_object(self):
        t, error_code = nxlib.get_type(self.path)
        self._check_return_code(error_code)
        return t == NXLIB_ITEM_TYPE_OBJECT

    def type(self):  # overrides python type keyword ... !
        t, error_code = nxlib.get_type(self.path)
        self._check_return_code(error_code)
        return t

    def exists(self):
        t, error_code = nxlib.get_type(self.path)
        if error_code == NXLIB_ITEM_INEXISTENT:
            return False
        elif error_code == NXLIB_OPERATION_SUCCEEDED:
            return t != NXLIB_ITEM_TYPE_INVALID
        else:
            self._check_return_code(error_code)
            return False

    def name(self):
        item_name, error_code = nxlib.get_name(self.path)
        self._check_return_code(error_code)
        return item_name

    def erase(self):
        error_code = nxlib.erase(self.path)
        if error_code == NXLIB_ITEM_INEXISTENT:
            return
        self._check_return_code(error_code)

    def wait_for_change(self):
        error_code = nxlib.wait_for_change(self.path)
        self._check_return_code(error_code)

    def wait_for_type(self, awaited_type, wait_for_equal):
        error_code = nxlib.wait_for_type(self.path, awaited_type, wait_for_equal)
        self._check_return_code(error_code)

    def wait_for_value(self, value, wait_for_equal):
        if type(value) is int:
            error_code = nxlib.wait_for_int_value(self.path, value, wait_for_equal)
        elif type(value) is str:
            error_code = nxlib.wait_for_string_value(
                self.path, value, wait_for_equal)
        elif type(value) is bool:
            error_code = nxlib.wait_for_bool_value(self.path, value, wait_for_equal)
        elif type(value) is float:
            error_code = nxlib.wait_for_double_value(self.path, value, wait_for_equal)
        self._check_return_code(error_code)

    def make_unique_item(self, item_name=None):
        new_path, error_code = nxlib.make_unique_item(self.path, item_name)
        self._check_return_code(error_code)
        if new_path:
            return NxLibItem(new_path)
        return NxLibItem()
