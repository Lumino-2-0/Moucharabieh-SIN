'''
Created by Sam ;)

https://github.com/Lumino-2-0
'''

from machine import Pin,PWM,ADC    #--|
import os                                   #  |--> Librairies nécessaires pour fonctionnement du code
import time                        #--|


#Pré-requi/Configuration du matériel
sg90 = PWM(Pin(21, mode=Pin.OUT))   # Configuration du moteur et ses PINs (ici Pin 21 pour la sortie de donnée)
sg90.freq(50)                      # Définition de la fréquence d'actualisation
adc0 = ADC(0)                     # Configuration du light_sensor (capteur de lumière) en analogique sur le Port A0



'''
En Python et sur la Pi, l’angle du moteur est calculé comme un pourcentage du cycle. Ce pourcentage se nomme « Duty Cycle ».

Un signal de 0.5ms correspond à 0° et un signal de 2.5ms à 180°. Sachant que notre cycle est de 50 Hz, soit 20ms, cela nous permet de calculer les Duty Cycle pour 0° et 180° comme ceci :

x = 0.5 / 20
y = 2.5 / 20
On trouve alors que le Duty Cycle correspondant à 0° est 0.025, soit 2.5% et que celui correspondant à 180° est 0.125, soit 12.5%.

DONC : 

    0.5ms/20ms = 0.025 = 2.5% duty cycle
    2.4ms/20ms = 0.12 = 12% duty cycle

    0.025*65535=1638
    0.12*65535=7864

'''
#Variable à initialiser 
Semi_ANA = 4369                                   #Valeur (moyenne) pour la nuit (àm modifier selon les calibrages)
Coucher_1 = 10000
Coucher_2 = 1638
Trop_lumineux = 64500

while True :
    print("adc0=",adc0.read_u16())                 # Afficer les valeurs analogiques dans la console

    ANA_Lum = adc0.read_u16()                     # Variable qui est la valeur analogique actuelle

    if ANA_Lum < Semi_ANA :                     # Si la lumière atuelle [ANA_Lum] est en dessous de la lumière sombre (nuit) [Semin_ANA]
        i = 0                             
        while i == 1638 :
            sg90.duty_u16(i)                     # Modifier la valeur du servo moteur (16bits) à 1638 ---|
            i = i + 1                        # On augmente la valeur de 1 (pour le mouvement) ----|    A modifier selo les groupes (voir calcul ci-dessus)
            time.sleep(0.01)                      # Attendre 0.01 seconde

    elif ANA_Lum < Coucher_1 and ANA_Lum > Coucher_2 : # Au  coucher du soleil
        i = 0
        while i == 4096 :
            sg90.duty_u16(i)  
            i = i + 1
            time.sleep(0.01)

    
    elif ANA_Lum > Trop_lumineux :                # Si la lumière atuelle [ANA_Lum] est au dessus de la lumière trop lumineuse [Trop_lumineux]
        i = 7864                            # On initialise la variable i à 7864 (180°) ----------------|
        while i == 65535 :                     # On tourne le moteur jusqu'à 65535 (360°) -----------|
            sg90.duty_u16(i)                     # Modifier la valeur du servo moteur (16bits) à 65535 --|
            i = i - 1                        # On diminue la valeur de 1 (pour le mouvement) ----|    A modifier selo les groupes (voir calcul ci-dessus)
            time.sleep(0.01)              # Attendre 0.01 seconde

    else :                                 # Sinon...                                               | -> On tourne à 180° si besoins selon la position actuelle et la meteo
        i = 0                           # On initialise la variable i à 1638 (0°) ----------------|
        while i == 7864 :                     # On tourne le moteur jusqu'à 7864 (180°) --------------|
            sg90.duty_u16(i)                     # Modifier la valeur du servo moteur (16bits) à 1638 --|
            i = i - 1                        # On diminue la valeur de 1 (pour le mouvement) ----|    A modifier selo les groupes (voir calcul ci-dessus)
            time.sleep(0.01)                      # Attendre 0.01 seconde
    print("Valeur du moteur actuel : ", sg90.duty_u16)
    time.sleep(0.1)                          # Attendre 0.1 seconde


'''
 .__                .__                                        
                   |  |  __ __  _____ |__| ____   ____                           
                   |  | |  |  \/     \|  |/    \ /  _ \                           # type: ignore
                   |  |_|  |  /  Y Y  \  |   |  (  <_> )                          # type: ignore
                   |____/____/|__|_|  /__|___|  /\____/                           # type: ignore
                                    \/        \/                                  # type: ignore
  _________                       ___.                  __                        # type: ignore
 /   _____/____    _____          \_ |__   ____________/  |______   __ _____  ___ # type: ignore
 \_____  \\__  \  /     \   ______ | __ \_/ __ \_  __ \   __\__  \ |  |  \  \/  / # type: ignore
 /        \/ __ \|  Y Y  \ /_____/ | \_\ \  ___/|  | \/|  |  / __ \|  |  />    <  # type: ignore
/_______  (____  /__|_|  /         |___  /\___  >__|   |__| (____  /____//__/\_ \ # type: ignore
        \/     \/      \/              \/     \/                 \/            \/ # type: ignore

        L 
'''