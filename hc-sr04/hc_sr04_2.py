from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import statistics
import math 

import time

PIN_TRIG = 22
PIN_ECHO = 27
point    = 10
tmp      = [num for num in range(point)]

factory = PiGPIOFactory()
sensor = DistanceSensor(PIN_ECHO, PIN_TRIG, pin_factory=factory)

for i in range(point):
    print('Distance to nearest object is', sensor.distance, 'm')
    tmp[i] = sensor.distance * 100
    time.sleep(0.5)

median = statistics.median(tmp)
print('Distance to nearest object is', '{:.2f}'.format(median), 'cm(median', point ,'point)')

