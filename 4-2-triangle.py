import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(bit) for bit in format(value, 'b').zfill(8)]

num = 0
flag = 1
period = 0
try:
    period = float(input("Enter the period of triangle signal: "))
    while True:
        GPIO.output(dac, decimal2binary(num))
        num += flag
        if num == 0:
            flag = 1
        if num == 256:
            num -= 1
            flag = -1
        time.sleep(period/512)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()