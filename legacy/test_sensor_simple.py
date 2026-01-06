from gpiozero import DistanceSensor
from time import sleep

# Use the exact same pins as the C++ driver
# BCM 23 = Physical 16
# BCM 24 = Physical 18
TRIGGER_PIN = 23
ECHO_PIN = 24

print(f"Testing sensor on BCM Pins: Trig={TRIGGER_PIN}, Echo={ECHO_PIN}")
print(f"Please double check your wiring!")
print(f"Physical Pin 16 -> Trig")
print(f"Physical Pin 18 -> Echo")

try:
    sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIGGER_PIN, max_distance=4)
    print("Sensor initialized. Reading...")

    while True:
        dist_cm = sensor.distance * 100
        print(f"Distance: {dist_cm:.1f} cm")
        sleep(0.5)

except Exception as e:
    print(f"Error: {e}")
