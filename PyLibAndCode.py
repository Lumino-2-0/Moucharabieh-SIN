from machine import Pin, PWM, ADC
import time

class myServo(object):  #lib my servo
    def __init__(self, pin: int = 15, hz: int = 50):
        self._servo = PWM(Pin(pin), freq=hz) 
    
    def myServoWriteDuty(self, duty):
        duty = max(26, min(128, duty))
        self._servo.duty(duty)
        
    def myServoWriteAngle(self, pos):
        pos = max(0, min(180, pos))
        pos_buffer = (pos / 180) * (128 - 26)
        self._servo.duty(int(pos_buffer) + 26)

    def myServoWriteTime(self, us):
        us = max(500, min(2500, us))
        pos_buffer = (1024 * us) / 20000
        self._servo.duty(int(pos_buffer))
        
    def deinit(self):
        self._servo.deinit()

servo = myServo(15)  # Servo Pin
servo.myServoWriteAngle(90)  # 180/2 = 90

adc = ADC(Pin(36))     #Pin potentiometre
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_10BIT)

print("OHAYO MASTER! WATASHI WA ESP32")
time.sleep(1)

try:
    while True:
        adc_value = adc.read()  # 0 - 1023
        duty = int((adc_value / 1023) * (128 - 26)) + 26
        servo.myServoWriteDuty(duty)
        print(f"Potentiometre: {adc_value} -> Angle: {duty}")
        time.sleep(0.1)
except:
    servo.deinit()

