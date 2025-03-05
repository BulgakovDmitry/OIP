import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

troyka_pin     = 13
comparator_pin = 14
dac_pins       = [8, 11, 7, 1, 0, 5, 12, 6]
led_pins       = [2, 3, 4, 17, 27, 22, 10, 9]

GPIO.setup(dac_pins, GPIO.OUT)
GPIO.setup(led_pins, GPIO.OUT)
GPIO.setup(comparator_pin, GPIO.IN)
GPIO.setup(troyka_pin, GPIO.OUT, initial = 1)


def number_to_bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

def number_to_bar(num):
    fill = round(num / 256 * 8)
    return [1 if i < fill else 0 for i in range(8)]

BASE_VOLTAGE = 3.3
SLEEP_TIME   = 0.003
# reads analog signal and returns voltage in scale of 0..255
def adc():
    # binary search algorithm
    exponent = 128
    number = 0
    while (exponent > 0):
        # print(number, exponent)
        number += exponent

        GPIO.output(dac_pins, number_to_bin(number))
        
        #time to get stable voltage 
        time.sleep(SLEEP_TIME)

        # comparator returns 0 if Signal < DAC
        if GPIO.input(comparator_pin) == 1:
            number -= exponent

        exponent //= 2

    return number



try:
    while(1):
        volt_number = adc()
        voltage = volt_number / 256 * BASE_VOLTAGE
        print(f'Voltage on s = {voltage:.2f} V')
        GPIO.output(led_pins, number_to_bar(volt_number))



finally:
    GPIO.output(dac_pins, 0)
    GPIO.output(troyka_pin, 0)
    GPIO.cleanup()