import dht
from machine import Pin

def get_dht_readings():
    # Initialize the DHT11 sensor on the provided pin
    sensor = dht.DHT11(22)
    
    try:
        # Trigger the measurement
        sensor.measure()
        
        # Retrieve the values
        temp_c = sensor.temperature() # Temperature in Celsius
        hum = sensor.humidity()       # Humidity percentage
        
        return temp_c, hum
        
    except OSError as e:
        # DHT sensors can occasionally fail to read, which throws an OSError
        print("Failed to read from DHT sensor:", e)
        return None, None