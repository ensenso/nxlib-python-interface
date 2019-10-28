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

1. **nx_list_cams.py** - will get all cameras in the current nxlib and prints their serials and their availability onto the standard output.
2. **nx_simple.py** - will open a stereo-camera with the serial as argument, captures an image pair, rectifies them and computes the disparity map. Afterwards the point cloud is computed and the z-Average value of the point cloud is printed onto the standard output.
3. **nx_save_images.py** - will open a camera with the serial as argument, captures an image pair, rectifies them and saves them as *.png files into the directory, where the executable is located.
4. **nx_watch_point_cloud.py** - will open a stereo-camera with the serial as argument and will capture images with. It also rectifies the images, computes the disparity map and the point cloud. The point cloud result will be shown with the open3d viewer. In Order to run this examples, you will have to have [open3D](http://www.open3d.org/) installed. If that is not the case, you can easily install it with pip.

### Additional

**Install open3d with pip** - In Order to use the example **nx_watch_point_cloud.py**, you will have to install open3d with
```bash
pip install open3d-python
```
or (if no sufficient privileges)
```bash
pip install --user open3d-python
```

