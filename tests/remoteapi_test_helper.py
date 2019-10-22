from ensenso_nxlib.item import NxLibItem
from ensenso_nxlib.constants import *

import ensenso_nxlib.api as nxlib
import sys

import time
import subprocess

global nxlib_started
nxlib_started = False

global tcp_port
tcp_port = 24000

global host_name
host_name = 'localhost'


def _start_normal_nxlib():
    global tcp_port
    nxlib.load_lib()
    nxlib.initialize()
    nxlib.open_tcp_port(tcp_port)


def _end_normal_nxlib():
    nxlib.close_tcp_port()
    nxlib.finalize()


def main():
    while True:
        global nxlib_started
        if not nxlib_started:
            try:
                _start_normal_nxlib()
            except:
                print("failed")
                break
            print("started")
            nxlib_started = True
        time.sleep(1)


if __name__ == "main":
    main()
