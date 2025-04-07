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

adc1 = ADC(Pin(36))     #Pin potentiometre 1
adc1.atten(ADC.ATTN_11DB)
adc1.width(ADC.WIDTH_10BIT)

adc2 = ADC(Pin(35))     #Pin potentiometre 2
adc2.atten(ADC.ATTN_11DB)
adc2.width(ADC.WIDTH_10BIT)

print("OHAYO MASTER! WATASHI WA ESP32")
time.sleep(1)

try:
    while True:
        adc1_value = adc1.read()  # 0 - 1023
        angle = int((adc1_value / 1023) * 180)
        servo.myServoWriteDuty(angle)
        print(f"Potentiometre: {adc1_value} -> Angle: {angle}")
        time.sleep(0.1)
    
        adc2_value = adc2.read()
        #1023/3 = 341
        if adc2_value <= 341: 
            print("1/3")
        if adc2_value <= 682 and adc2_value >341:
            print("2/3")
        if adc2_value > 682:
            print("3/3")
        time.sleep(1)
        
except:
    servo.deinit()
    print("issue")
