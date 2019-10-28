# NxLib Python Interface

This package is the Python interface from the [Ensenso](https://www.ensenso.com/) GmbH, to access functionalities of the NxLib via Python. With the Interface you can access your installed version of the NxLib from the [EnsensoSDK](https://www.ensenso.com/support/sdk-download/?lang=en) and use it with Python. Beware this project is currently in beta phase and some functionalities do not work yet.

## Prerequisites

In Order to use this package you will need the following Prerequisites installed:
  * [EnsensoSDK](https://www.ensenso.com/support/sdk-download/?lang=en) - Official SDK of the [Ensenso](https://www.ensenso.com/) Group for developing software with stereo 3D cameras for industrial applications.
  * [Python](https://www.python.org/downloads/) - Version > 3.5. is required.
  * [Pip](https://pip.pypa.io/en/stable/installing/) - A Python package manager. Version > 9.0.1 is required.

The following packages should be installed default with python > 3.5., that are:
  * [Numpy](https://numpy.org/) - A package for scientific computing with Python (tested and developed with 1.17.2).
  * [Ctypes](https://docs.python.org/3.5/library/ctypes.html) - A foreign function library for Python, that allows calling functions in DLLs or shared libraries.


This package is only needed, if you want to run the tests in the ./tests folder:
  * [Pytest](https://docs.pytest.org/en/latest/) - A Python testing framework.

## Installing

There are two ways of installing the package. Either directly from source, or via pip repositories.

#### Installing with Pip Repository
If you do not need to do any modifications in the installed packet space and only want to use the package as is, we recommend you to install the package with pip. Pip will handle all dependencies of the package and will download the latest package version from here.

Global installation (does need privileged rights).
```
pip install ensenso_nxlib
```
Local installation.
```
pip install --user ensenso_nxlib
```

#### Installing from Source
If you like to install from source, e.g. to make local changes of the installed package on your system, you will first have to clone the repository
```
git clone https://github.com/ensenso/nxlib-python-interface.git
```
and install it from the root of the cloned repository (where the [setup.py](setup.py) - file is located).
```
cd nxlib-python-interface
pip install .
```

If you like to do changes to your local installation (development version), install it with
```
pip install -e .[dev]
```
You will need extra packages defined under [setup.py](setup.py) in the extra_require dictionary, which pip will install for you.


## Overview

The Python Interface ensenso_nxlib consists of modules which implement the NxLib classes (NxLibItem, NxLibCommand, NxLibException) and modules which wrap the global NxLib-Functions.

### Global Functions and Constants
  * **api** - The module for accessing global functions.
  * **constants** - A module, where all constants are defined. When this module is imported, it **updates itself** with the constants defined in the corresponding installed / loaded DLL (Windows) or shared library (Linux).
  * **helper** - Helper functions that are used within other modules of this package (can be ignored).

### Classes
  * **item** - The module for the NxLibItem class.
  * **command** - The module for the NxLibCommand class.
  * **exception** - The module for NxLibException class.

### How to import the modules
The constants or api module should be imported like this
```python
import ensenso_nxlib.api as api
from ensenso_nxlib.constants import *
```
Usually import * should be avoided. In this case however, it is unlikely that the constants defined here have the same name as other variables in your projects. Otherwise you will have to access them within a namespace like the following
```python
import ensenso_nxlib.constants as consts
```
and call the corresponding constants with the defined namespace
```python
consts.ITM_NXLIB_CONSTANT
```

Class modules can be easily imported like the following
```python
from ensenso_nxlib import NxLibItem, NxLibCommand, NxLibException
```

## Differences to other Language APIs from EnsensoSDK

The Python API differs in naming convention and access of global/static functions, which are described below.

### Naming
We try to make the Python API feel like the ones in C or C++, described in the EnsensoSDK [manual](https://www.ensenso.com/manual/index.html?nxlib_api.htm).
The main difference lies in between the naming convention. In Python we use the naming convention after [pep8](https://www.python.org/dev/peps/pep-0008/) and in C, C#, C++ we use the [camelCase](https://en.wikipedia.org/wiki/Camel_case)-convention.

The difference is shown in the following table.

| Type      | Python             | C/C++           |
| --------- | ------------------ | --------------- |
| Constants | ITM_CONSTANT | itmConstant |
| Variables | this_is_a_variable | thisIsAVariable |
| Functions | a_function() | aFunction() |

### Static/Global Function Access

If you would like to use C-Api-like functions (associated without any objects) within Python, you will have to call them with an object.
As an example the code in C++
```cpp
#include <nxLib.h>
nxLibInitialize();
```
will be the following in Python.
```python
import ensenso_nxlib.api as api
api.initialize()
```
We also stripped away the nxLib prefix of these static C++ or C functions, because the corresponding functions in Python are associated with an object.

Of course, you could also do the following:
```python
from ensenso_nxlib.api import *
initialize()
```
That enables you to call the function within the global namespace in Python. This, however, is not recommended. It could overwrite other functions that have the same name in your program (which is likely for the name e.g. initialize)


Other than that, you can use the Python API like the other APIs described in the [manual](https://www.ensenso.com/manual/). We also encourage you to do the examples (below) first.


## Examples

Some examples are provided in the [examples](./examples) subfolder of this project. 
If you like to execute them, clone this repository and execute the individual examples in that subfolder.
For further information see the [README.md](examples/README.md) within the examples subfolder of this project.

## Running Tests

If you would like to run tests, go to the root of the project folder (where the setup.py is located) and execute the following:
```
python3 setup.py test
```
This will run all tests, defined in the ./tests folder, with pytest. All functions that start with test_* or end with *_test ( * denotes a [wildcard](https://en.wikipedia.org/wiki/Wildcard_character)), will be executed.

If you want to execute a sole test, you will have to define it in its own *.py file and run it with
```
python3 sole_test.py
```

## Versioning

For released versions, see the [tags on this repository](https://github.com/ensenso/nxlib-python-interface/tags). We use Major.Minor version numbers.
Sometimes there are also post releases. Post released means that the source code has not been changed, but the documentation, for example, has been changed.

## Authors

* **[Yasin Guenduez](mailto:yasin.guenduez@ensenso.com)** - *Ensenso GmbH - Maintenance and further development*
* **[Paul Rogister](mailto:paul.rogister@isys-vision.de)** - *isys vision GmbH - Initial work*

## Licence

This project is licensed under the MIT Licence - see the [LICENSE.md](LICENSE.md) file for details

