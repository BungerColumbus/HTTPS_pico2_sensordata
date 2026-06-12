import network
import urequests
import socket
from time import sleep_ms
import machine
import json


ssid = 'Go Go Hotspot Gadget!!!'
password = 'parolamea:)'
website = "http://188.166.105.198/api/data"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    attempts = 0
    while (wlan.isconnected() == False):
        print('Attempting to connect...')
        attempts += 1
        if attempts >= 20:
            wlan.active(False)
            # Raise a standard Python exception with a custom message
            raise OSError("Wi-Fi connection failed: Max attempts reached.")
        sleep_ms(1000)
    print(wlan.ifconfig())


def send_data(status_message):
    # Read all data points
    temperature, humidity, voltage, distance = status_message
    
    # Prepare the JSON payload
    payload = {
        "t1": temperature,
        "h1": humidity,
        "v": voltage,
        "d": distance
    }

    headers = {"Content-Type": "application/json"}
    
    try:
        print(f"Sending data: {status_message}")
        # Making the POST request
        response = urequests.post(website, data=json.dumps(payload), headers=headers)
        
        print("Server Response Code:", response.status_code)
        print("Server Response:", response.text)
        
        response.close() # Closing the connection to free memory
    except Exception as e:
        print("Failed to send data:", e)