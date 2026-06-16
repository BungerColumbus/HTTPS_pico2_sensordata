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

    # Wrapping connection in try/except
try:
    network_connection.ensure_connection()
except KeyboardInterrupt:
    print("Detected Ctrl+C, exiting cleanly.")
    sys.exit()  # Exit to REPL instead of resetting the whole board
except Exception as e:
    print(f"Connection failed: {e}")

while True:

    def read_sensors():
        sensor_power.value(1)
        
        # Give the DHT11 and Ultrasonic sensors time to boot up and stabilize
        sleep_ms(2000) 
    
        distance = get_distance(echo=echo, trig=trig)
        temperature, humidity = get_dht_readings()
    
        sensor_power.value(0)
        return (temperature, humidity, distance)

    # Gather and send data
    try:
        data = read_sensors()
        network_connection.send_data(data)
    except KeyboardInterrupt:
        print("Detected Ctrl+C, exiting cleanly.")
        sys.exit()
    except Exception as e:
        print(f"Failed to process or send data: {e}")

    sleep_ms(3000)

    try:

        file_name = record_audio()
        
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

    pin.value(0) 

    print("Going to sleep...")
    # Sleep for 10 seconds.
    sleep_ms(10000)
