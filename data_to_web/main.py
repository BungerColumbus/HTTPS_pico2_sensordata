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

counter = 0

while True:
    distance = get_distance(echo = echo, trig = trig)
    print(distance)
    counter += 1
    status = f"Hello from Pico 2W!\nUpdate #{counter}\nDistance: {distance} cm"
    network_connection.send_data(status)
    time.sleep_ms(10000)
