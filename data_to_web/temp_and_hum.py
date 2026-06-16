import dht
from machine import Pin

def get_dht_readings():
    sensor = dht.DHT11(Pin(22)) 
    
    try:
        # Trigger the measurement
        sensor.measure()
        
        # Retrieve the values
        temp_c = sensor.temperature() # Temperature in Celsius
        hum = sensor.humidity()       # Humidity percentage
        
        return temp_c, hum
        
    except OSError as e:
        # DHT sensors can occasionally fail to read
        print("Failed to read from DHT sensor:", e)
        return None, None