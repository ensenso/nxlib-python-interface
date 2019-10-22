from ensenso_nxlib import NxLibCommand, NxLibException, NxLibItem
from ensenso_nxlib.constants import *
import ensenso_nxlib.api as api

import argparse


def get_camera_node(serial):
    root = NxLibItem()  # References the root
    cameras = root[ITM_CAMERAS][ITM_BY_SERIAL_NO]  # References the cameras subnode
    for i in range(cameras.count()):
        found = cameras[i].name() == serial
        if found:
            return cameras[i]


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial", type=str, required=True,
                        help="The serial of the stereo camera, you want to open")
    args = parser.parse_args(args)

    camera_serial = args.serial
    try:
        # Waits for the cameras to be initialized
        api.initialize()

        # Opens the camera with the serial stored in camera_serial variable
        cmd = NxLibCommand(CMD_OPEN)
        cmd.parameters()[ITM_CAMERAS] = camera_serial
        cmd.execute()

        # Captures with the previous openend camera
        capture = NxLibCommand(CMD_CAPTURE)
        capture.parameters()[ITM_CAMERAS] = camera_serial
        capture.execute()

        # Rectifies the images
        rectify = NxLibCommand(CMD_RECTIFY_IMAGES).execute()

        # Get the item node of the openend camera
        camera = get_camera_node(camera_serial)

        # Save images
        save_image_cmd = NxLibCommand(CMD_SAVE_IMAGE)

        save_image_cmd.parameters()[ITM_NODE] = camera[ITM_IMAGES][ITM_RAW][ITM_LEFT].path
        save_image_cmd.parameters()[ITM_FILENAME] = "raw_left.png"
        save_image_cmd.execute()

        save_image_cmd.parameters()[ITM_NODE] = camera[ITM_IMAGES][ITM_RAW][ITM_RIGHT].path
        save_image_cmd.parameters()[ITM_FILENAME] = "raw_right.png"
        save_image_cmd.execute()

        save_image_cmd.parameters()[ITM_NODE] = camera[ITM_IMAGES][ITM_RECTIFIED][ITM_LEFT].path
        save_image_cmd.parameters()[ITM_FILENAME] = "rectified_left.png"
        save_image_cmd.execute()

        save_image_cmd.parameters()[ITM_NODE] = camera[ITM_IMAGES][ITM_RECTIFIED][ITM_RIGHT].path
        save_image_cmd.parameters()[ITM_FILENAME] = "rectified_right.png"
        save_image_cmd.execute()

        # Closes all open cameras
        NxLibCommand(CMD_CLOSE).execute()

    except NxLibException as e:
        print("An NxLibException occured: Error Text: {}".format(e.get_error_text()))
    except:
        print("Something bad happenend, that has been out of our control.")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
