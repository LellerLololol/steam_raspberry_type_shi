#!/bin/bash

# Compile the C++ driver into a shared library (.so)
# Requires: pigpio library installed (usually default on Raspbian)

echo "Compiling ultra_driver.cpp..."

g++ -shared -o ultra_driver.so -fPIC ultra_driver.cpp -lpigpio -lrt

if [ $? -eq 0 ]; then
    echo "Compilation successful! Created ultra_driver.so"
else
    echo "Compilation failed."
    exit 1
fi
