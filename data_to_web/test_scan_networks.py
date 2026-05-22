import network
import ubinascii

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

net = wlan.scan()

for i in range(len(net)):

    ssid = net[i][0].decode('utf-8')
    bssid = ubinascii.hexlify(net[i][1], ':').decode('utf-8')
    channel = net[i][2]
    rssi = net[i][3]

    print(f"SSID: {ssid} | BSSID: {bssid} | Channel: {channel} | RSSI: {rssi}dBm")



