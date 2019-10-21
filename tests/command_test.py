import pytest
import os

from nxlib import NxLibCommand, NxLibException
from nxlib.constants import *

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
test_camera = CURRENT_DIR + "/test_files/N35_test.zip"
TEST_FILES = os.path.join(CURRENT_DIR + "/" + "test_files/N35_test.zip")


def test_open_a_non_existing_serial():
    with pytest.raises(NxLibException):
        broken_serial = "Blubb"
        cmd = NxLibCommand(CMD_OPEN)
        cmd.parameters()[ITM_CAMERAS] = broken_serial
        cmd.execute()


def test_command_does_not_exist():
    with pytest.raises(NxLibException):
        cmd = NxLibCommand("DestroyPc")
        cmd.execute()


def test_create_file_camera():
    cmd = NxLibCommand(CMD_CREATE_CAMERA)
    cmd.parameters()[ITM_FOLDER_PATH] = test_camera
    cmd.parameters()[ITM_SERIAL_NUMBER] = "test_cam"
    cmd.execute()


def test_open_created_file_camera():
    cmd = NxLibCommand(CMD_OPEN)
    cmd.parameters()[ITM_CAMERAS] = "test_cam"
    cmd.execute


def test_no_wait_fail():
    import time
    cmd = NxLibCommand(CMD_CREATE_CAMERA)
    cmd.parameters()[ITM_FOLDER_PATH] = "this folder does not exist!"
    cmd.execute(None, False)
    while not cmd.finished():
        time.sleep(1)
    assert not cmd.successful()


def test_command_run():
    cmd = NxLibCommand(CMD_GET_CONSTANTS)
    cmd.execute()
    assert cmd.successful()
