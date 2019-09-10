from nxlib import NxLibItem
from nxlib.constants import *
import nxlib.api as api


def main():

    try:
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

    except NxLibException as e:
        print("An NxLibException occured: Error Text: {}".format(e.get_error_text()))
    except:
        print("Something bad happenend, that has been out of our control.")


if __name__ == "__main__":
    main()
