import urequests
import json
import network
import time

ssid = 'Bbox-FF4A3DBF'
password = 'Md7EyRQ69ZAZ3jHd3X'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print("\n Connecté par WiFi!")
print("Adresse IP :", wifi.ifconfig()[0])


data = urequests.get("https://wttr.in/Saint-Nazaire?format=3")
print(data.text)  # Exemple : "Paris: 🌦 +12°C"
data.close()