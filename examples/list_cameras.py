from nxlib import NxLibItem
from nxlib.constants import *
import nxlib.api as api


def main():
    # Waits for the cameras to be initialized
    api.initialize()

    # References to the root of the nxLib tree
    root = NxLibItem()

    # Reference to the serials subnode of all cameras
    cameras = root[ITM_CAMERAS][ITM_BY_SERIAL_NO]

    # Loop over the array
    for i in range(cameras.count()):
        if cameras[i][ITM_STATUS][ITM_OPEN].exists():
            is_available = cameras[i][ITM_STATUS][ITM_AVAILABLE].as_bool()
            serial = cameras[i].name()
            print("Camera with serial {} is currently {}".format(serial, "available" if is_available else "closed"))


if __name__ == "__main__":
    main()
