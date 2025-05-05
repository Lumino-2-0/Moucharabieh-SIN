'''
Created by Sam ;)

https://github.com/Lumino-2-0
'''

from machine import Pin,PWM,ADC    #--|
from servo import Servo
from time import sleep
from datetime import datetime, date, time, timedelta, timezone






servo=Servo(pin=21, min=500, max=2500, max_angle=180) # Définition du servomoteur sur le GPIO 21 avec une largeur d'impulsion de 500 μs pour 0 degré et 2500 μs pour 180 degrés 
adc0 = ADC(0)                                         # Configuration du light_sensor (capteur de lumière) en analogique sur le Port A0

'''
Servo(pin, min, max)
    pin: Le numéro du GPIO sur lequel est connecté le servomoteur.
    min (optionnel) : la largeur d'impulsion, en microsecondes, correspondant à l'angle minimum (0 degré) du servo (par défaut 500).
    max (optionnel) : la largeur d'impulsion, en microsecondes, correspondant à l'angle maximum (180 degrés) du servo (par défaut 2500).
    max_angle (optionnel) : Angle maximum du servomoteur (par défaut 180).

    On trouve ces informations sur la datasheet du servo c'est en μs.
    FT5330M : min = 500, max = 2 500, neutre = 1 500. 
    FS90 : min = 500, max = 2 500, neutre = 1 500. 

'''
mois =  datetime.now().date().month

print(mois)
while True:             #Faire de la boucle infinie

    light_sensor = adc0.read_u16()                  # Lire la valeur du capteur de lumière actuelle
    print("Luminosite Analogique : ", light_sensor) # Afficher la valeur du capteur de lumière

    if light_sensor <= 1500:                        # Si la valeur du capteur de lumière est inférieure ou égale à 1500 (Presque la nuit / C'est la nuit)
        servo.move(0)                               # Déplacer le servomoteur à 0 degré
        print("Servo a 0 degres")                   # Afficher que le servomoteur est à 0 degré
        sleep(0.50)                                 # Attendre 0.5 seconde
    elif light_sensor >= 64500:                     # Si la valeur du capteur de lumière est supérieure ou égale à 64500 (Trop lumineux)
        servo.move(180)                              # Déplacer le servomoteur à 90 degrés
        print("Servo a 180 degres")                  # Afficher que le servomoteur est à 90 degrés
        sleep(0.50)                                 # Attendre 0.5 seconde
    else :
        servo.move(90)                             # Déplacer le servomoteur à 180 degrés
        print("Servo a 90 degres")                 # Afficher que le servomoteur est à 180 degrés
        sleep(0.50)                                 # Attendre 0.5 seconde
    
        


'''
Crédit à Mr Frank Sauret pour la librairie Servo.py
'''
