#include <arrow/python/pyarrow.h>
#include <pybind11/pybind11.h>
#include<Python.h>

#include "arrow_conversions.hh"


#include <arrow/array/builder_primitive.h>

#include<iostream>


std::shared_ptr<arrow::DoubleArray> vol_adj_close(std::shared_ptr<arrow::DoubleArray>& close,std::shared_ptr<arrow::Int64Array>& volume)
{
    std::cout<<"arrow function called"<<std::endl;
    if (close->length()!=volume->length())
        throw std::length_error("Arrays are not of equal length");
    std::cout<<"length check passed"<<std::endl;
    arrow::DoubleBuilder builder;
    arrow::Status status = builder.Resize(volume->length()*sizeof(double));
    if (!status.ok()) {
        throw std::bad_alloc();
    }
    std::cout<<"status"<<status.ok()<<std::endl;
    std::cout<<"resize called"<<std::endl;
    for(int i = 0; i < volume->length(); i++) {
        // std::cout<<"for loop called"<<std::endl;
        // std::cout<<close->Value(i) / volume->Value(i)<<std::endl;

        // builder.AppendEmptyValue();

        //UnsafeAppend fails
        auto temp=static_cast<double>(close->Value(i) / volume->Value(i));
        builder.UnsafeAppend(temp);
    }
    std::cout<<"appended data (via unsafe call)"<<std::endl;
    std::shared_ptr<arrow::DoubleArray> array;
    arrow::Status st = builder.Finish(&array);
    if (!status.ok()) {
        throw std::bad_alloc();
    }
    std::cout<<"returning array"<<std::endl;
    return array;
}

int import_pyarrow()
{
    return arrow::py::import_pyarrow();
}


PYBIND11_MODULE(helperfuncs, m) {
    arrow::py::import_pyarrow();
    m.doc() = "Pyarrow Extensions";
    m.def("vol_adj_close", &vol_adj_close, pybind11::call_guard<pybind11::gil_scoped_release>());
    m.def("import_pyarrow",&import_pyarrow);
    m.def("import_pyarrow2",&arrow::py::import_pyarrow);
}
