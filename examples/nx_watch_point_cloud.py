from ensenso_nxlib import NxLibCommand, NxLibException, NxLibItem
from ensenso_nxlib.constants import *
import ensenso_nxlib.api as api

import argparse
import open3d as o3d
import numpy


def _ensenso_to_open3d(ensenso_pc):
    point_cloud = o3d.geometry.PointCloud()

    # Reshape from (m x n x 3) to ( (m*n) x 3)
    vector_3d_vector = ensenso_pc.reshape(
        (ensenso_pc.shape[0] * ensenso_pc.shape[1]), ensenso_pc.shape[2])

    # Filter nans: if a row has nan's in it, delete it
    vector_3d_vector = vector_3d_vector[~numpy.isnan(
        vector_3d_vector).any(axis=1)]
    point_cloud.points = o3d.utility.Vector3dVector(vector_3d_vector)
    return point_cloud


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

        # Watch the captured point cloud with open3d-python
        point_cloud = _ensenso_to_open3d(points)
        o3d.visualization.draw_geometries([point_cloud])

        # Closes all open cameras
        NxLibCommand(CMD_CLOSE).execute()

    except NxLibException as e:
        print("An NxLibException occured: Error Text: {}".format(e.get_error_text()))
    except:
        print("Something bad happenend, that has been out of our control.")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
