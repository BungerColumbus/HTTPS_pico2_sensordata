from machine import Pin, time_pulse_us, reset
from ultrasound import get_distance
from utime import sleep
import time
import network_connection

pin = Pin("LED", Pin.OUT)
trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

sleep(1) # sleep 1sec
pin.toggle()
print("Pico ON")

try:
    network_connection.connect()
except KeyboardInterrupt:
    reset()

#Sensor data
distance = 0
counter = 0

def read_sensors():
    distance = get_distance(echo = echo, trig = trig)
    print(distance)
    return(51 + counter, 24 + counter, 31 + counter, distance)

while True:
    network_connection.send_data(read_sensors())
    time.sleep_ms(10000)
