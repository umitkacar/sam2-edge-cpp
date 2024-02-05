#!/bin/bash

# If the "build" directory exists, delete it
if [ -d "build" ]; then
  rm -rf build
fi

# Create a new "build" directory
mkdir build

# Change to the build directory
cd build

# Configure the project with CMake
cmake ..

# Compile the project
make

