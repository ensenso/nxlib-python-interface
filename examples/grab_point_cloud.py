from nxlib import NxLibCommand, NxLibException, NxLibItem
from nxlib.constants import *
import nxlib.api as api

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

    # Recieve the left and right raw image
    img_left = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_RAW][ITM_LEFT].get_binary_data()
    img_right = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_RAW][ITM_RIGHT].get_binary_data()

    # Rectify the the captures raw images
    recitfication = NxLibCommand(CMD_RECTIFY_IMAGES)
    recitfication.execute()

    img_left_rectified = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_RECTIFIED][ITM_LEFT].get_binary_data()
    img_right_rectified = NxLibItem(
    )[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_RECTIFIED][ITM_RIGHT].get_binary_data()

    # Compute the disparity map
    disparity_map = NxLibCommand(CMD_COMPUTE_DISPARITY_MAP)
    disparity_map.execute()
    disp_map = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_DISPARITY_MAP].get_binary_data()

    # Compute the point map from the disparitu map
    point_map = NxLibCommand(CMD_COMPUTE_POINT_MAP)
    point_map.execute()
    points = NxLibItem()[ITM_CAMERAS][camera_serial][ITM_IMAGES][ITM_POINT_MAP].get_binary_data()

    # Watch the captured point cloud with open3d-python or pcl-python
    point_cloud = _ensenso_to_open3d(points)
    o3d.visualization.draw_geometries([point_cloud])


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
