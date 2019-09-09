# Nxlib Python Examples

This subfolder consists of several examples of how to use the Python interface.
The following list describe, what the individual executables will do.

## General usage of examples.

In order to run the examples, go into the examples folder and execute the *.py files with python3. Some of the examples require arguments though.

Executing without arguments:
```
python3 file_name.py
```

Executing with argument:
```
python3 file_name.py -s abc
```
where _-s_ is the argument specifier and _abc_ the corresponding value of the argument.

## Examples

1. **grab_point_cloud.py** - will open a stereo-camera with the serial as argument and will capture images with. It also recitifies the images, computes the dispariy map and the point cloud. The point cloud result will be shown with the open3d viewer. In Order to run this examples, you will have to have [open3D](http://www.open3d.org/) installed. If that is not the case, you can easily install it with pip.
2. **list_camera.py** - will get all cameras and prints their serials and their availability onto the standard output.

