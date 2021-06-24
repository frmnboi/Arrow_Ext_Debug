To debug the creation of C++ extensions for Pyarrow

Repository is based off the one here:
https://github.com/vaexio/vaex-arrow-ext

Requires: 
- pip install pyarrow 
- pip install pybind11

To use this example, modify the last 3 lines of the cmake file to the corresponding library locations on your current device. You may need to change the python version or library name to match the one on your device. I think there might be a way to automatically locate these shared libraries, but I'm not familiar enough with Arrow and Cmake to know how to do this.

create and move the python extension using cmake:

- mkdir build; cd build
- cmake ..
- make
- cp helperfuncs* ../Database

Then run the database function with the test scenario at the bottom:

- python database.py

The expected result is for the code to segmentation fault if the c++ builder is called to append a value in helperfuncs.cpp. The library should be importable without error (and as part of the import process, calls the required arrow::py::import_pyarrow())
