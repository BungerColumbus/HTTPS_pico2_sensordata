from machine import Pin, time_pulse_us
from ultrasound import get_distance
from utime import sleep
import time

pin = Pin("LED", Pin.OUT)
trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

sleep(1) # sleep 1sec
pin.toggle()
print("Pico ON")



while True:
    distance = get_distance(echo = echo, trig = trig)
    print(distance)
    time.sleep_ms(100)
    print("waited 0.1 sec")



      
print("Finished.")
pin.off()
