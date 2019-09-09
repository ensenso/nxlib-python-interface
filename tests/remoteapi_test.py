import pytest
import os
import sys
from subprocess import PIPE, Popen
from nxlib.item import NxLibItem
from nxlib.constants import *

from tests.remoteapi_test_helper import tcp_port, host_name

import time


import nxlib.api as nxlib_remote

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
global helper_file
helper_file = CURRENT_DIR + '/remoteapi_test_helper.py'


@pytest.fixture(scope="session")
def nxlib_pid():
    """
    Starts a normal nxlib in a subprocess and returns the process handle
    """
    nxlib_procc = Popen(['python3', '-u', helper_file], stdin=PIPE, stdout=PIPE,
                        universal_newlines=True, bufsize=1)

    # hack: pytest currently captures stdin and stdout pipe
    # so we just wait till the normal nxlib is getting started. (no stdin/stoud communication possible)
    time.sleep(10)  # wait for 10 secs, to make sure the lib is loaded successfully
    assert nxlib_procc is not None, "Could not start nxlib subprocess"
    return nxlib_procc


@pytest.fixture(scope="session")
def open_nxview():
    """
    Starts NxView in a subprocess as shell command and returns the process handle
    """
    nxview_procc = Popen(["nxView"])
    assert nxview_procc is not None, "Could not start nxlib subprocess"
    time.sleep(10)  # wait for nxview
    return nxview_procc


def test_remoteapi(open_nxview):
    assert open_nxview.pid is not None
    nxlib_remote.load_remote_lib()

    global tcp_port
    global host_name
    nxlib_remote.connect(host_name, tcp_port)
    _test_set_and_get_string()

    # Kill the subprocess
    time.sleep(1)
    open_nxview.kill()


def _test_set_and_get_string():
    assert nxlib_remote.is_current_lib_remote()
    NxLibItem()["test"] = "doofbacke"
    string = NxLibItem()["test"].as_string()
    assert "doofbacke" in string
