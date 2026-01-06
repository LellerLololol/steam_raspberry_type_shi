import ctypes
import time
import pathlib

lib = ctypes.CDLL(str(pathlib.Path("Y401.so").resolve()))

# call start
if lib.start_sensor() != 0:
    print("Failed to start sensor")
    exit(1)

print("Sensor running")

while True:
    dist = lib.get_last_distance()
    print("distance =", dist)
    time.sleep(0.1)
