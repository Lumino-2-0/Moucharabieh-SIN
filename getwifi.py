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

data = urequests.get("https://wttr.in/Paris?format=3")
print(data.text) 
#data.close()

resultat = ""

for char in data.text:
    if char.isdigit():
        resultat += char
    elif resultat:
        break

print(resultat)
