# Moucharabieh-SIN

Projet de fin d'année 1ère STI2D1 pour faire tourner un servomoteur selon la saison et la luminosité.

### Pré-requis [Matérielement]
Pour pouvoir utiliser ce projet, il vous faut :

  - **Un Raspberry Pi Pico W (W pour la connexion Wifi)**
  - **Un capteur de luminosité analogique**
  - **Un servomoteur analogique**

Pour exécuter le code, utilisez un IDE comme ***Visual Studio (Code)*** et installez l'extension ***MicroPython***.

## Comment fonctionne-t-il ?

Ce code va en premier lieu connecter la carte à un wifi *(à vous de mofifier la ligne de code comportant le SSDI et le Mot de passe)*.
Ensuite, il se connectera à un serveur NTP permettant d'obtenir la date/heure/saison exacte actuel. Un exemple de serveur NTP connu est 
> pool.ntp.org

Par la suite, il choisira plus précisemment l'angle de pivot a donner pour le servo moteur. De plus qu'il utilisera le capteur de luminosité pour régler l'ouverture du Moucharabieh.
