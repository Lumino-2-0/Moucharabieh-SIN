'''
Created by Sam Bertaux 1STI2D-1

https://github.com/Lumino-2-0
'''

#-----------------------------------------------------------------|
                                                                 #|
import machine                                                   #|
from servo import Servo                                          #| Modules nécessaires, ne pas toucher
import time                                                      #|
#import ntptime                                                  #|
                                                                 #|
#-----------------------------------------------------------------|


'''Constante globale'''
#-----------------------------------------------------------------|
servo = Servo(pin=21, min=500, max=2500, max_angle=180)           # Définition du servomoteur sur le GPIO 21 avec une largeur d'impulsion de 500 μs pour 0 degré et 2500 μs pour 180 degrés 
adc0  = machine.ADC(0)                                            # Configuration du light_sensor (capteur de lumière) en analogique sur le Port A0
ssid = 'Lumastor'                                                 # Nom du réseau Wi-Fi (Inutile actuellement)
password = '11092008'                                             # Mot de passe du réseau Wi-Fi (Inutile actuellement)
NTP_DELTA = 2208988800 + 3600 * 2                                 # Décalage NTP pour UTC+2 (France, Parid GMT+2), donc +2h = +7200 secondes (inutile actuellement)
host = "fr.pool.ntp.org"                                          # Serveur NTP à utiliser (inutile actuellement)
#-----------------------------------------------------------------|


#Décommenter cette section ainsi que toutes les parties necessaires à la connexion au serveur NTP si vous voulez tester (Normalment fonctionnel sur ESP32)
'''Connexion au Wi-Fi
#-----------------------------------------------------------------|
def connect():                                                    

    wlan = network.WLAN(network.STA_IF)                           
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Connexion au Wifi...')
        time.sleep(1)
    print(wlan.ifconfig())
    print('Connecte au Wifi !')
#-----------------------------------------------------------------|

Récupération de l'heure NTP

#-----------------------------------------------------------------|
def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    try:
        addr = socket.getaddrinfo("ntp.unice.fr", 123)[0][-1]
        print(f"Adresse IP résolue pour ntp.unice.fr : {addr}")
    except Exception as e:
        print(f"Erreur de résolution DNS pour ntp.unice.fr : {e}")
        raise

    for attempt in range(5):  # Réessayez jusqu'à 5 fois
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(10)  # Augmentez le délai d'attente
            print(f"Tentative {attempt + 1} de connexion au serveur NTP...")
            s.sendto(NTP_QUERY, addr)
            print(f"Requête envoyée au serveur {addr}. En attente de réponse...")
            msg = s.recv(48)
            val = struct.unpack("!I", msg[40:44])[0]
            t = val - NTP_DELTA    
            tm = time.gmtime(t)
            machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
            print("Heure mise à jour avec succès.")
            return
        except OSError as e:
            print(f"Tentative {attempt + 1} échouée : {e}")
        finally:
            s.close()
    raise Exception("Impossible de récupérer l'heure NTP après plusieurs tentatives.")

#-----------------------------------------------------------------|

'''
#Décommenter cette section ainsi que toutes les parties necessaires à la connexion au serveur NTP si vous voulez tester (Normalment fonctionnel sur ESP32)


######################################################################################################################################
'''                                                   Debug dans cette section :                                                   
connect()                                                        # Connexion au Wi-Fi
print("Date actuelle theorique avant synchro %s" %str(time.localtime()))
try :
    ntptime.settime()
except OverflowError:
            # it is not going to work
            print("overflow error; settime is borked \n Retentative dans 5 secondes...")
            time.sleep(5000)

except OSError:
            print(f"ntptime.settime() failure \n Retentative dans 5 secondes...")
            # Not expecting more than 1 failure, maybe waiting will help?
            time.sleep(5000)
print("Date actuelle apres synchro %s" %str(time.localtime()))

'''
#Décommenter cette section ainsi que toutes les parties necessaires à la connexion au serveur NTP si vous voulez tester (Normalment fonctionnel sur ESP32)


######################################################################################################################################
'''
Description :
    On fait une boucle infinie qui va lire la valeur analogique envoyée par le capteur de lumière (Light_Sensor) et donc, qui peut varier entre 0 et 65535 selon la luminosité captée.
    Ensuite on agit selon le taux de luminosité et la saison (hiver ou été) :
        - En hiver (mois 11, 12, 1, 2) : Si la luminosité est faible, on ouvre à fond.
        - En été (mois 5, 6, 7, 8) : Si la luminosité est trop forte, on réduit à moitié.
        - Sinon, on ajuste en fonction de la luminosité.


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

# Valeurs seuils pour la luminosité
SEUIL_FAIBLE = 1500        # Trop sombre
SEUIL_FORTE = 63000        # Trop lumineux
ANGLE_NUIT = 0
ANGLE_JOUR = 180
ANGLE_TROP_LUMINEUX = 90

# Angle actuel suivi manuellement
angle_actuel = 180 # Démarre en position jour

while True:
    try:
        # Lecture de la luminosité
        light_sensor = adc0.read_u16()
        print("Luminosite : ", light_sensor)
        print("Angle actuel du servo :", angle_actuel)

        # Déterminer l'angle voulu en fonction de la luminosité
        if light_sensor <= SEUIL_FAIBLE:
            angle_voulu = ANGLE_NUIT
        
        elif light_sensor >= SEUIL_FORTE:
            angle_voulu = ANGLE_TROP_LUMINEUX
        
        else:
            angle_voulu = ANGLE_JOUR

        # Définir si le mouvement est autorisé selon les règles
        transition_valide = False
        if (angle_actuel == ANGLE_JOUR and angle_voulu in [ANGLE_NUIT, ANGLE_TROP_LUMINEUX]) or \n           (angle_actuel == ANGLE_NUIT and angle_voulu == ANGLE_JOUR) or \n           (angle_actuel == ANGLE_TROP_LUMINEUX and angle_voulu == ANGLE_JOUR):
            transition_valide = True
        elif angle_actuel == angle_voulu:
            transition_valide = False  # Pas de mouvement nécessaire
        else:
            transition_valide = False  # Interdit : trop lumineux ↔ nuit

        if transition_valide:
            # Bouge le servo doucement, degré par degré
            step = 1 if angle_voulu > angle_actuel else -1  # Détermine la direction
            for angle in range(angle_actuel, angle_voulu + step, step):
                servo.move(angle)           # Déplacement du servo à l'angle actuel
                print(f"Deplacement vers {angle}°")
                time.sleep(0.05)            # Délai pour ralentir le mouvement
            angle_actuel = angle_voulu      # Met à jour l’angle actuel

        else:
            print("Transition ignoree (non autorisee ou deja à la bonne position)")

        time.sleep(0.2)  # Petite pause avant la prochaine lecture

    except Exception as e:
        print("Erreur :", e)



'''
Crédit à Mr Frank Sauret pour la librairie Servo.py
Je sais qu'il y a plus de commentaires que de code mais bon, le projet n'a pas vraiment besoins d'un code complexe.
'''
