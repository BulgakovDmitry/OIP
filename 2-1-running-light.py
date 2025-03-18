import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

leds = [2, 3, 4, 17, 27, 22, 10, 9]

for i in range(0,len(leds)):
    GPIO.setup(leds[i], GPIO.OUT)

for i in range(0,3):
    for j in range (0, len(leds)):
        GPIO.output(leds[j], 1)
        time.sleep(0.2)
        GPIO.output(leds[j], 0)
        time.sleep(0.2)

for i in range(0,len(leds)):
    GPIO.output(leds[j], 0)