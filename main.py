'''
Created by Sam Bertaux 1STI2D-1

https://github.com/Lumino-2-0
'''

#-----------------------------------------------------------------|
                                                                 #|
import network                                                   #|
import socket                                                    #|
import machine                                                   #|
from servo import Servo                                          #| Modules nécessaires, ne pas toucher
import struct                                                    #|
import time                                                      #|
                                                                 #|
#-----------------------------------------------------------------|


'''Constante globale'''
#-----------------------------------------------------------------|
servo = Servo(pin=21, min=500, max=2500, max_angle=180)           # Définition du servomoteur sur le GPIO 21 avec une largeur d'impulsion de 500 μs pour 0 degré et 2500 μs pour 180 degrés 
adc0  = machine.ADC(0)                                            # Configuration du light_sensor (capteur de lumière) en analogique sur le Port A0
ssid = 'REDMAGIC 9S Pro Lumino'                                   # Nom du réseau Wi-Fi
password = '110908'                                               # Mot de passe du réseau Wi-Fi
NTP_DELTA = 2208988800 + 3600 * 2                                 # Décalage NTP pour UTC+2 (France, Parid GMT+2), donc +2h = +7200 secondes
host = "fr.pool.ntp.org"                                          # Serveur NTP à utiliser
#-----------------------------------------------------------------|



'''Connexion au Wi-Fi'''
#-----------------------------------------------------------------|
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Connection au Wifi...')
        time.sleep(1)
    print(wlan.ifconfig())
    print('Connecté au Wifi !')
#-----------------------------------------------------------------|

'''Récupération de l'heure NTP'''
#-----------------------------------------------------------------|

def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
#-----------------------------------------------------------------|



######################################################################################################################################
'''                                                   Debug dans cette section :                                                   '''

connect()                                                           # Connexion au Wi-Fi
set_time()                                                          # Récupération de l'heure via NTP
heure_actuelle = time.localtime()                                   # Obtenir l'heure actuelle

######################################################################################################################################

'''
Description :
    On fait une boucle infinie qui va lire la valeur analogique envoyée par le capteur de lumière (Light_Sensor) et donc, qui peut varier entre 0 et 65535 selon la luminosité captée.
    Ensuite on agit selon le taux de luminosité et la saison (hiver ou été) :
        - En hiver (mois 11, 12, 1, 2) : Si la luminosité est faible, on ouvre à fond.
        - En été (mois 5, 6, 7, 8) : Si la luminosité est trop forte, on réduit à moitié.
        - Sinon, on ajuste en fonction de la luminosité.
'''

try:
    while True:                                                               # Faire une boucle infinie
        light_sensor = adc0.read_u16()                                        # Lire la valeur du capteur de lumière actuelle
        mois = time.localtime()[1]                                            # Obtenir le mois actuel

        print("Luminosité Analogique : ", light_sensor)                       # Afficher la valeur du capteur de lumière

        if mois in [11, 12, 1, 2]:                                            # Si on est en hiver
            if light_sensor <= 1500:                                          # Si la luminosité est faible
                servo.move(180)                                               # Déplacer le servomoteur à 180 degrés (ouverture maximale)
                print("Hiver : Servo à 180 degrés (ouverture maximale)")
            else:
                servo.move(90)                                                # Sinon, ouverture partielle
                print("Hiver : Servo à 90 degrés (ouverture partielle)")
        elif mois in [5, 6, 7, 8]:                                            # Si on est en été
            if light_sensor >= 64500:                                         # Si la luminosité est trop forte
                servo.move(90)                                                # Réduire à moitié
                print("Été : Servo à 90 degrés (réduction à moitié)")
            else:
                servo.move(180)                                               # Sinon, ouverture maximale
                print("Été : Servo à 180 degrés (ouverture maximale)")
        else:                                                                 # Pour les autres saisons
            if light_sensor <= 1500:                                          # Si la luminosité est faible
                servo.move(0)                                                 # Fermer complètement
                print("Autre saison : Servo à 0 degré (fermé)")
            elif light_sensor >= 64500:                                       # Si la luminosité est trop forte
                servo.move(90)                                                # Réduire à moitié
                print("Autre saison : Servo à 90 degrés (réduction à moitié)")
            else:
                servo.move(180)                                               # Sinon, ouverture maximale
                print("Autre saison : Servo à 180 degrés (ouverture maximale)")

        time.sleep(0.5)                                                       # Attendre 0.5 seconde avant la prochaine lecture
except Exception as e:
    print("Erreur :", e)                                                      # Afficher l'erreur en cas de problème

'''
Crédit à Mr Frank Sauret pour la librairie Servo.py
Je sais qu'il y a plus de commentaire que de code mais bon, le projet n'a pas vraiment besoins d'un code complexe.
'''
