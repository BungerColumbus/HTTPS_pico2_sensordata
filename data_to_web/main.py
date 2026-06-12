import machine
from machine import Pin, reset, deepsleep, freq
from ultrasound import get_distance
from microphone import sample_microphone
from utime import sleep_ms
import network_connection

# Underclock the CPU
freq(50000000) 

pin = Pin("LED", Pin.OUT)
trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

# Sensor Power Gating
sensor_power = Pin(16, Pin.OUT)
sensor_power.value(0)

pin.toggle()
print("Pico ON")

try:
    network_connection.connect()
except KeyboardInterrupt:
    reset()


def read_sensors():
    sensor_power.value(1)
    
    sleep_ms(50) 
    
    distance = get_distance(echo=echo, trig=trig)
    mic = sample_microphone(50)
    
    sensor_power.value(0)
    
    print(distance)
    print(mic)
    return (51, 24, mic, distance)

# Gather and send data
try:
    data = read_sensors()
    network_connection.send_data(data)
except Exception as e:
    print(f"Failed to process or send data: {e}")

pin.value(0) 

print("Going to deep sleep...")

# Sleep for 10 seconds (10,000 ms). The Pico will reset and run this script again upon waking.
deepsleep(10000)