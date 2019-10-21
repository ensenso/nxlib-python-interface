from nxlib import NxLibCommand, NxLibException, NxLibItem
from nxlib.constants import *
import nxlib.api as api

import argparse
import numpy


def filter_nans(point_map):
    return point_map[~numpy.isnan(point_map).any(axis=1)]


def reshape_point_cloud(point_map):
    """
    Reshapes the point cloud array from (m x n x 3) to ((m*n) x 3)
    """
    return point_map.reshape(
        (point_map.shape[0] * point_map.shape[1]), point_map.shape[2])


def compute_average_z(point_map):
    z_count = 0
    z_average = 0.0

    point_map = reshape_point_cloud(point_map)
    point_map = filter_nans(point_map)

    for i in range(point_map.shape[0]):
        point = point_map[i]
        z_value = point[2]
        z_average = z_value
        z_count += 1

    if z_count != 0:
        z_average = z_average / z_count
    return z_average


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

        # Rectify the the captures raw images
        rectification = NxLibCommand(CMD_RECTIFY_IMAGES)
        rectification.execute()

        # Compute the disparity map
        disparity_map = NxLibCommand(CMD_COMPUTE_DISPARITY_MAP)
        disparity_map.execute()

        # Compute the point map from the disparitu map
        point_map = NxLibCommand(CMD_COMPUTE_POINT_MAP)
        point_map.execute()
        points = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_POINT_MAP].get_binary_data()

        average_z = compute_average_z(points)
        print("The z-Average of this point cloud is {}".format(average_z))

        # Closes all open cameras
        NxLibCommand(CMD_CLOSE).execute()

    except NxLibException as e:
        print("An NxLibException occured: Error Text: {}".format(e.get_error_text()))
    except:
        print("Something bad happenend, that has been out of our control.")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
