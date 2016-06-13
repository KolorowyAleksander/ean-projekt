cmake_minimum_required(VERSION 3.5)
project(ean_projekt)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -m64 -static")

set(SOURCE_FILES
        c++/src/main.cpp
        c++/lib/interval.h)

add_executable(ean_projekt ${SOURCE_FILES})