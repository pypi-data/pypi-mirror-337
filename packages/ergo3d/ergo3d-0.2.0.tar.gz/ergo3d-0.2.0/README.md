# ergo3d
A Python package for calculating 3D geometric and ergonomic angles, designed for motion capture (Vicon) data and 3D human pose estimation results. 

# ergo3d

`ergo3d` is a Python package for handling and manipulating points, planes, coordinate systems, and joint angles in 3D space. This package is essential for geometric and ergonomic calculations.

## Modules

The package contains the following modules:

- `Point`: Provides classes and methods for handling and manipulating points in 3D space.

- `Plane`: Provides a class for defining 3D planes.

- `CoordinateSystem3D`: Provides a class for defining 3D coordinate systems.

- `JointAngles`: Provides a class easy ergonomic angle calculations.

## Installation

### install from PyPI
```bash
pip install ergo3d
```

### Use from source
```bash
git clone https://github.com/LeyangWen/ergo3d.git
```

### Steps to update the package on PyPI
* Update the version number in `setup.py`
* Build the package and upload to PyPI
```bash
python setup.py sdist bdist_wheel
```
```bash
twine upload dist/*
```
* API token from [Pypl](https://pypi.org/manage/account/token/)

