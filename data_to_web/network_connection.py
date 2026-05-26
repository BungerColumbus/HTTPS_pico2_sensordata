import network
import urequests
import socket
from time import sleep_ms
import machine
import json


ssid = 'WiFi 3.1'
password = 'c6etrApEcR'
website = "http://http://188.166.105.198/api/data"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while (wlan.isconnected() == False):
        print('Attempting to connect...')
        sleep_ms(1000)
    print(wlan.ifconfig())

def send_data(status_message):
    # Prepare the JSON payload
    payload = {"status": status_message}
    headers = {"Content-Type": "application/json"}
    
    try:
        print(f"Sending data: {status_message}")
        # Make the POST request
        response = urequests.post(website, data=json.dumps(payload), headers=headers)
        
        print("Server Response Code:", response.status_code)
        print("Server Response:", response.text)
        
        response.close() # Always close the connection to free memory
    except Exception as e:
        print("Failed to send data:", e)


counter = 0

try:
    connect()
except KeyboardInterrupt:
    machine.reset()

while True:
    counter += 1
    status = f"Hello from Pico 2W! Update #{counter}"
    send_data(status)
    sleep_ms(10000)