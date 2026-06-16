import network
import urequests
import socket
from time import sleep_ms
import machine
import json
import os

ssid = 'WiFi 3.1'
password = 'c6etrApEcR'
data_website = "http://188.166.105.198/api/data"
audio_website = "http://188.166.105.198/api/upload-audio"

def ensure_connection():
    """Checks if connected to Wi-Fi, and reconnects if dropped."""
    wlan = network.WLAN(network.STA_IF)
    
    if wlan.isconnected():
        return True
        
    print('Wi-Fi disconnected. Attempting to connect...')
    wlan.active(True)
    wlan.connect(ssid, password)
    
    attempts = 0
    while not wlan.isconnected() and attempts < 30:
        print('Attempting to connect...')
        attempts += 1
        sleep_ms(1000)
        
    if wlan.isconnected():
        print('Connected! Network config:', wlan.ifconfig())
        return True
    else:
        print('Error: Could not connect to Wi-Fi.')
        return False

def send_data(status_message):
    if not ensure_connection():
        print("Skipping send_data: No network connection.")
        return

    temperature, humidity, distance = status_message
    payload = {
        "t1": temperature,
        "h1": humidity,
        "d": distance,
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        print(f"Sending data: {status_message}")
        # Add a timeout so it doesn't hang forever if the network drops mid-request
        response = urequests.post(data_website, data=json.dumps(payload), headers=headers, timeout=10)
        
        print("Server Response Code:", response.status_code)
        print("Server Response:", response.text)
        response.close() 
        
    except OSError as e:
        print(f"Network error in send_data: {e}")
    except Exception as e:
        print(f"Failed to send data: {e}")

def send_wav(file_path):
    if not ensure_connection():
        print("Skipping send_wav: No network connection.")
        return

    try:
        os.stat(file_path)
    except OSError:
        print(f"Error: The file {file_path} does not exist.")
        return

    headers = {"Content-Type": "audio/wav"}
    
    try:
        print(f"Reading and sending {file_path}...")
        
        with open(file_path, "rb") as f:
            audio_data = f.read() 
            
        # Add a timeout here as well
        response = urequests.post(audio_website, data=audio_data, headers=headers, timeout=15)
        
        print("Server Response Code:", response.status_code)
        print("Server Response:", response.text)
        response.close() 
        
    except MemoryError:
        print("MemoryError: The WAV file is too large to load into Pico's RAM.")
    except OSError as e:
        print(f"Network error in send_wav: {e}")
    except Exception as e:
        print(f"Failed to send WAV file: {e}")