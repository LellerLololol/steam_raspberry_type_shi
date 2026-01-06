import sys
from gpiozero import DistanceSensor
from time import sleep
import numpy as np
import cv2
import argparse
import time
import datetime
import ctypes
import pathlib
import asyncio

async def sensor():
    #Camera setup
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    sleep(5)
    
    #Ctype shi
    C_lib = ctypes.CDLL(pathlib.Path().absolute() / "Y401.so")
 
    #Pins and sensors
    trigger_pin = 23
    echo_pin = 24
    sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)

    
    
    while True:
        print("sensor is working")
        #Camera
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #Sensor
        distance_cm = sensor.distance * 100
        print (f"distance = {distance_cm:.1f} cm")
        sleep(0.1)

    
    #Camera cleanup
    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()



