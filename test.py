import network
import socket
import machine
from servo import Servo
import time
import urequests
import struct
import ntptime

# Configuration du servo moteur et des capteurs
servo = Servo(pin=21, min=500, max=2500, max_angle=180)
sock = socket.socket()
adc0 = machine.ADC(0)  # Capteur de lumière sur le port A0
ssid = 'REDMAGIC 9S Pro Lumino'
password = 'Lumastor'
NTP_DELTA = 2208988800 + 3600 * 2  # UTC+2
host = "time.google.com"

'''
# Connexion au Wi-Fi
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    timeout = 10  # Temps maximum pour la connexion (en secondes)
    while not wlan.isconnected() and timeout > 0:
        print('Connexion au Wi-Fi...')
        time.sleep(1)
        timeout -= 1
    if wlan.isconnected():
        print('Connecte au Wi-Fi !', wlan.ifconfig())
    else:
        raise OSError("Impossible de se connecter au Wi-Fi. Verifiez vos parametres.")

def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    retries = 3  # Nombre de tentatives
    for attempt in range(retries):
        try:
            s.settimeout(5)  # Timeout de 5 secondes
            s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
            val = struct.unpack("!I", msg[40:44])[0]
            t = val - NTP_DELTA
            tm = time.gmtime(t)
            machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
            print("Heure mise à jour :", time.localtime())  # Affiche la date et l'heure locale
            return  # Sortir de la fonction si la mise à jour réussit
        except OSError as e:
            print(f"Tentative {attempt + 1} : Erreur lors de la récupération de l'heure NTP :", e)
            time.sleep(2)  # Attendre avant de réessayer
        finally:
            s.close()
    raise OSError("Impossible de récupérer l'heure NTP après plusieurs tentatives.")

# Déterminer la saison (hiver ou été)
def get_season():
    current_date = time.localtime()
    month = current_date[1]
    print(f"Date actuelle : {time.localtime()}")
    if month in [12,1,2,3,4,5]:  # Hiver + printemps
        return "winter"
    elif month in [6,7,8,9,10,11]:  # Été + automne
        return "summer"
    else:
        return "other"

# Programme principal
def main_old():
    connect()
    set_time()
    
    # Vérifiez si la date a été mise à jour
    current_date = time.localtime()
    if current_date[0] < 2023:  # Vérifie si l'année est correcte
        print("Erreur : la date n'a pas ete mise à jour correctement.")
        return
    
    try:
        while True:
            light_sensor = adc0.read_u16()  # Lire la valeur du capteur de lumière
            season = get_season()  # Déterminer la saison
            print(f"Luminosité : {light_sensor}, Saison : {season}")

            if season == "winter":
                if light_sensor <= 1500:  # Nuit ou faible luminosité
                    servo.move(180)  # Ouvrir complètement
                    print("Hiver : Servo a 180 degres (jour)")
                else:
                    servo.move(0)  # Fermer complètement
                    print("Hiver : Servo a 0 degres (nuit)")
            elif season == "summer":
                if light_sensor >= 64500:  # Trop lumineux
                    servo.move(90)  # Ouvrir à moitié
                    print("Été : Servo a 90 degrés (trop lumineux)")
                else:
                    servo.move(180)  # Ouvrir complètement
                    print("Été : Servo a 180 degres (jour)")
            else:
                servo.move(0)  # Par défaut, fermer
                print("Autre saison : Servo a 0 degres")

            time.sleep(0.5)  # Pause de 0.5 seconde
    except Exception as e:
        print("Erreur :", e)
'''


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    timeout = 10  # Temps maximum pour la connexion (en secondes)
    while not wlan.isconnected() and timeout > 0:
        print('Connexion au Wi-Fi...')
        time.sleep(1)
        timeout -= 1
    if wlan.isconnected():
        print('Connecte au Wi-Fi !', wlan.ifconfig())
        time.sleep(0.5)  # Attendre 5 secondes pour que la connexion Internet soit prête
    else:
        raise OSError("Impossible de se connecter au Wi-Fi. Vérifiez vos parametres.")


def test_network():
    try:
        response = urequests.get("http://time.google.com")  # Utilisez un serveur HTTP valide
        print("Connexion Internet reussie. (requete google)")
        response.close()
    except Exception as e:
        print("Erreur de connexion Internet :", e)

def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    retries = 3  # Nombre de tentatives
    for attempt in range(retries):
        try:
            addr = socket.getaddrinfo(host, 123)[0][-1]
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Crée un nouveau socket à chaque tentative
            s.settimeout(5)  # Timeout de 5 secondes
            s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
            val = struct.unpack("!I", msg[40:44])[0]
            t = val - NTP_DELTA
            tm = time.gmtime(t)
            machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
            print("Heure mise a jour :", time.localtime())  # Affiche la date et l'heure locale
            return  # Sortir de la fonction si la mise à jour réussit
        except OSError as e:
            print(f"Tentative {attempt + 1} : Erreur lors de la recuperation de l'heure NTP :", e)
            time.sleep(1)  # Attendre avant de réessayer
        finally:
            s.close()  # Fermer le socket après chaque tentative
    raise OSError("Impossible de recuperer l'heure NTP apres plusieurs tentatives.")

# Appel principal
def main():
    connect()
    
    test_network()
    #set_time()
    print("Programme termine.")
# Lancer le programme
main()