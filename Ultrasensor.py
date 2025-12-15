import sys
from gpiozero import DistanceSensor
from time import sleep
import numpy as np
import argparse
import time
import datetime
import ctypes
import pathlib
import asyncio

async def sensor():
    #print("I GET LOADED")
    #Ctype shi
    c_lib = ctypes.CDLL(pathlib.Path().absolute() / "Y401.so")
    return_value = c_lib.main()
 
    """
    #Pins and sensors
    trigger_pin = 23
    echo_pin = 24
    sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)
    """

    while True:
        #Sensor
        print("sensor is working")
        print(return_value)
        #distance_cm = sensor.distance * 100
        #print (f"distance = {distance_cm:.1f} cm")
        #sleep(0.1)


if __name__ == "__main__":
	asyncio.run(sensor())
