# Moucharabieh-SIN

Projet de fin d'année 1ère STI2D1 pour faire tourner un servomoteur selon la saison et la luminosité.

### Pré-requis [Matérielement]
Pour pouvoir utiliser ce projet, il vous faut :

  - **Un Raspberry Pi Pico OU un ESP32** *(préféré **l'ESP32** si vous voulez utiliser le serveur NTP)* 
  - **Un capteur de luminosité analogique**
  - **Un servomoteur analogique**

Pour exécuter le code, utilisez un IDE comme ***Visual Studio (Code)*** et installez l'extension ***MicroPython***.

## Comment fonctionne-t-il ?

Ce code va en premier lieu connecter la carte à un wifi *(à vous de mofifier la ligne de code comportant le SSID et le Mot de passe)*.
Ensuite, il se connectera à un serveur NTP permettant d'obtenir la date/heure/saison exacte actuel. Des exemples de serveurs NTP connus sont: 
> - pool.ntp.org
> - fr.pool.ntp.org
> - time.google.com


### Ce système a été mis en commentaire car plus fonctionnel dans le code pour un Raspberry Pi Pico W depuis une mise à jour de MicroPython. 
### Il peut être utilisé sur un ESP32 à la place.

Ensuite selon la luminosité acutelle (via le détecteur de luminosité ambiant), on change l'orientation des pales du moucharabieh. Notamment ici, si la luminosité est trop faible, on ferme l'ouverture.
Donc on règle le *SEUIL_FAIBLE* selon se que l'on considère comme "la nuit". Puis on tourne le servomoteur à la position 0°.
Cela s'applique pour la nuit, le jour (luminère ambiente), ou en canicule/trop forte lumière :
```
# Valeurs seuils pour la luminosité

SEUIL_FAIBLE = 1500        # Trop sombre
SEUIL_FORTE = 64500        # Trop lumineux
ANGLE_NUIT = 0
ANGLE_JOUR = 180
ANGLE_TROP_LUMINEUX = 90

[...]

# Déterminer l'angle voulu en fonction de la luminosité
        if light_sensor <= SEUIL_FAIBLE:
            angle_voulu = ANGLE_NUIT
        
        elif light_sensor >= SEUIL_FORTE:
            angle_voulu = ANGLE_TROP_LUMINEUX
        
        else:
            angle_voulu = ANGLE_JOUR
[...]
```

Le tout est géré par une transition plus lente dans la suite du code (optionnel aussi mais pour ne pas être brusque lorsque l'on tourne le servo moteur.

## Objectif principal du projet de fin d'année:

*En hiver, favoriser l'impact du rayonnement solaire sur les vitrages pour optimiser les apports gratuits lorsqu'il y a du soleil et limiter les déperditions quand il n'y a pas d'apport solaire.*
*En été, limiter l'impact du soleil sur les vitrages pour diminuer l'effet de serre et ainsi éviter les surchauffes.*
*En toutes saisons, favoriser l'éclairage naturel pour limiter les besoins d'éclairage artificiel qui consomment de l'énergie.*

