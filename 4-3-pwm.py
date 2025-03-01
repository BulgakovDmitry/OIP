import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

shim = GPIO.PWM(21, 1000)
shim.start(0)

try:
    while True:
        coef = int(input("Введите коэффициент заполнения: "))
        shim.ChangeDutyCycle(coef)
        voltage = 3.3*coef/100
        print(f"Assumed voltage: {voltage: .4}V")

finally:
    shim.stop()
    GPIO.output(21, 0)
    GPIO.cleanup()