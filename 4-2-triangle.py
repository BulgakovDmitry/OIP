import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def convert_to_binary(decimal_value):
    return [int(bit) for bit in format(decimal_value, 'b').zfill(8)]

current_value = 0
direction = 1
signal_period = 0

try:
    signal_period = float(input("Enter the period of triangle signal: "))
    
    while True:
        GPIO.output(dac, convert_to_binary(current_value))
        current_value += direction
        
        if current_value == 0:
            direction = 1
        if current_value == 256:
            current_value -= 1
            direction = -1
        
        time.sleep(signal_period / 512)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()