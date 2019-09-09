import pytest
import os
from nxlib import NxLibItem, NxLibCommand
import nxlib.api as api
from nxlib.constants import *
import numpy

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
test_camera = CURRENT_DIR + "/test_files/N35_test.zip"


def test_capture_pipeline():
    api.initialize()

    camera_serial = "test_cam"

    cmd = NxLibCommand(CMD_CREATE_CAMERA)
    cmd.parameters()[ITM_SERIAL_NUMBER] = camera_serial
    cmd.parameters()[ITM_FOLDER_PATH] = test_camera
    cmd.execute()

    cmd = NxLibCommand(CMD_OPEN)
    cmd.parameters()[ITM_CAMERAS] = camera_serial
    cmd.execute()

    capture = NxLibCommand(CMD_CAPTURE)
    capture.parameters()[ITM_CAMERAS] = camera_serial
    capture.execute()

    img_left = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_RAW][ITM_LEFT].get_binary_data()
    _test_binary_data(img_left, 1024, 1280, 1, numpy.uint8)

    img_right = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_RAW][ITM_RIGHT].get_binary_data()
    _test_binary_data(img_right, 1024, 1280, 1, numpy.uint8)

    recitfication = NxLibCommand(CMD_RECTIFY_IMAGES)
    recitfication.execute()

    img_left_rectified = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_RECTIFIED][ITM_LEFT].get_binary_data()
    _test_binary_data(img_left_rectified, 1024, 1280, 1, numpy.uint8)

    img_right_rectified = NxLibItem(
    )[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_RECTIFIED][ITM_RIGHT].get_binary_data()
    _test_binary_data(img_right_rectified, 1024, 1280, 1, numpy.uint8)

    disparity_map = NxLibCommand(CMD_COMPUTE_DISPARITY_MAP)
    disparity_map.execute()
    disp_map = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_DISPARITY_MAP].get_binary_data()
    _test_binary_data(disp_map, 1024, 1280, 1, numpy.int16)

    point_map = NxLibCommand(CMD_COMPUTE_POINT_MAP)
    point_map.execute()
    points = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_POINT_MAP].get_binary_data()
    _test_binary_data(points, 1024, 1280, 3, numpy.float32)


def _test_binary_data(img_to_test, height, width, channel, dtype):
    assert img_to_test is not None  # check if not referenced at all
    assert img_to_test.shape == (height, width, channel)  # height, width, channel
    assert img_to_test.dtype.type == dtype  # check the type of the numpy array (uint8, int16, int32, float32, float64)
    assert img_to_test.nbytes == height * width * channel * img_to_test.dtype.itemsize  # check space in memory
