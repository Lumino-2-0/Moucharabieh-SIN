import urequests
import json
import network
import time

# Configuration du Wi-Fi
SSID = "REDMAGIC 9S Pro Lumino"
PASSWORD = "Lumastor"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

try:
    wifi.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wifi.isconnected():
        time.sleep(1)
    print("\n INTERNET OK")
    print("Adresse IP :", wifi.ifconfig()[0])

    # Vérifiez la stabilité de la connexion Wi-Fi
    try:
        # Essayez de faire un ping vers un serveur connu
        response = urequests.get("http://www.example.com")
        response.close()
        print("Ping successful")
    except Exception as e:
        print("Ping failed:", e)

    try:
        # Utilisez un serveur de test différent
        data = urequests.get("http://www.example.com")
        print(data.text)

        tempEXTstr = ""
        for char in data.text:
            if char.isdigit():
                tempEXTstr += char
            elif tempEXTstr:
                break
        print(tempEXTstr)

        data.close()  # Assurez-vous de fermer la connexion
    except Exception as e:
        print("Erreur lors de la requête HTTP :", e)
except Exception as e:
    print("Erreur lors de la connexion Wi-Fi :", e)
