import urequests
import json
import network
import time

ssid = 'Bbox-FF4A3DBF'
password = 'Md7EyRQ69ZAZ3jHd3X'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print("\n INTERNET OK")
print("Adresse IP :", wifi.ifconfig()[0])

data = urequests.get("https://wttr.in/Paris?format=3")
print(data.text)
#data.close()

tempEXTstr = ""
for char in data.text:
    if char.isdigit():
        tempEXTstr += char
    elif tempEXTstr:
        break
print(tempEXTstr)
tempEXTint = int(tempEXTstr)

#je ferais le code du capteur soon
capteurTempINTint = 21

if capteurTempINTint > tempEXTint:
    print("il fait plus chaud dedans")
else:
    print("il fait plus chaud dehors")
