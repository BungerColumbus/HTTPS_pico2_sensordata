import machine
from machine import Pin, reset, deepsleep, freq
from ultrasound import get_distance
from microphone import record_audio
from temp_and_hum import get_dht_readings
from utime import sleep_ms  # Added regular sleep
import network_connection
import sys

    # 3 seconds to press Ctrl+C before the script runs wild
print("Booting up... Press Ctrl+C now to stop.")
sleep_ms(3000) 

pin = Pin("LED", Pin.OUT)
trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

    # Sensor Power Gating
sensor_power = Pin(16, Pin.OUT)
sensor_power.value(0)

pin.toggle()
print("Pico ON")

def read_sensors():
    sensor_power.value(1)
        
    # Give the DHT11 and Ultrasonic sensors time to boot up and stabilize
    sleep_ms(2000) 
    
    distance = get_distance(echo=echo, trig=trig)
    temperature, humidity = get_dht_readings()
    
    sensor_power.value(0)
    return (temperature, humidity, distance)

while True:
    
    file_name = record_audio()

    try:
        
        if file_name: 
            print("Audio saved. Reconnecting to Wi-Fi...")
            network_connection.ensure_connection() 
            
            # Wait a brief moment to ensure the connection is stable
            sleep_ms(2000) 
            
            network_connection.send_wav(file_name)
    except KeyboardInterrupt:
        print("Detected Ctrl+C, exiting cleanly.")
        sys.exit()
    except Exception as e:
        print(f"Failed to process or send audio data: {e}")

    try:
        data = read_sensors()
        network_connection.send_data(data)
    except KeyboardInterrupt:
        print("Detected Ctrl+C, exiting cleanly.")
        sys.exit()
    except Exception as e:
        print(f"Failed to process or send stringdata: {e}")

    sleep_ms(3000)

    pin.value(0) 

    print("Going to sleep...")
    network_connection.powerDownWiFi()
    # Sleep for 10 seconds.
    sleep_ms(10000)
    # Here we are using just sleep. 
    # If this was working on battery I would simply switch from using sleep to using deepsleep.
    # It would also be possible to get rid of the infinite loop as main.py gets run each time
    # the pico awakes itself from deepsleep.