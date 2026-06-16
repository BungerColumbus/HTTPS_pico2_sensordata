import network
import urequests
import socket
from time import sleep_ms
import machine
import json
import os


ssid = 'Go Go Hotspot Gadget!!!'
password = 'parolamea:)'
website = "http://188.166.105.198/api/data"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    attempts = 0
    while (wlan.isconnected() == False and attempts < 15):
        print('Attempting to connect...')
        attempts+=1
        sleep_ms(1000)
    print(wlan.ifconfig())


def send_data(status_message):
    # Read all data points
    temperature, humidity, distance = status_message
    
    # Prepare the JSON payload
    payload = {
        "t1": temperature,
        "h1": humidity,
        "d": distance,
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

def send_wav(file_path):
    """
    Reads a .wav file from the Pico's filesystem and POSTs it as raw binary data.
    """
    # 1. Verify the file exists before trying to send
    try:
        os.stat(file_path)
    except OSError:
        print(f"Error: The file {file_path} does not exist.")
        return

    # 2. Set the content type to audio/wav
    headers = {"Content-Type": "audio/wav"}
    
    try:
        print(f"Reading and sending {file_path}...")
        
        # 3. Open the file in binary read mode ('rb')
        with open(file_path, "rb") as f:
            audio_data = f.read() 
            
        # 4. Make the POST request
        response = urequests.post(website, data=audio_data, headers=headers)
        
        print("Server Response Code:", response.status_code)
        print("Server Response:", response.text)
        
        response.close() # Always close to free up memory
        
    except MemoryError:
        print("MemoryError: The WAV file is too large to load into Pico's RAM.")
    except Exception as e:
        print("Failed to send WAV file:", e)
