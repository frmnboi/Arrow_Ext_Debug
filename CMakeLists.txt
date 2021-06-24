cmake_minimum_required(VERSION 3.10)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(TARGET_SUPPORTS_SHARED_LIBS True)

find_package(PythonInterp REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
link_libraries(python3.8)


project(TestProject)

add_subdirectory(Dependencies/pybind11/)

pybind11_add_module(helperfuncs Database/helperfuncs.cpp  MODULE)

add_compile_options(-O2 -shared -fPIC)
find_package(Arrow REQUIRED)

 #note, that PYTHONPATH, and python version should be for the python version used
 target_include_directories(helperfuncs PUBLIC PYTHONPATH//site-packages/pyarrow/include)
 target_link_libraries(helperfuncs PRIVATE arrow_static) #arrow_shared
 #note, I use linux so I have a .so file.  I believe this is libarrow_python.400.so in windows?
 target_link_libraries(helperfuncs PRIVATE PYTHONPATH/site-packages/pyarrow/libarrow_python.so.400)


