import network
import socket
from time import sleep_ms
import machine


ssid = 'Go Go Hotspot Gadget!!!'
password = 'parolamea:)'

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while (wlan.isconnected() == False):
        print('Attempting to connect...')
        sleep_ms(1000)
    print(wlan.ifconfig())

try:
    connect()
except KeyboardInterrupt:
    machine.reset()