import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)

settings_file = open("settings.txt", "w")

troyka_module_pin = 13
comparator_module_pin = 14
digital_to_analog_converter_pins = [8, 11, 7, 1, 0, 5, 12, 6]
led_indicator_pins = [2, 3, 4, 17, 27, 22, 10, 9]

GPIO.setup(digital_to_analog_converter_pins, GPIO.OUT)
GPIO.setup(led_indicator_pins, GPIO.OUT)

GPIO.setup(comparator_module_pin, GPIO.IN)
GPIO.setup(troyka_module_pin, GPIO.OUT, initial=0)

def convert_number_to_binary_list(number):
    return [int(bit) for bit in bin(number)[2:].zfill(8)]

BASE_VOLTAGE_LEVEL = 3.3
VOLTAGE_STABILIZATION_TIME = 0.003

def read_analog_voltage():
    binary_search_exponent = 128
    binary_search_number = 0
    while binary_search_exponent > 0:
        binary_search_number += binary_search_exponent

        GPIO.output(digital_to_analog_converter_pins, convert_number_to_binary_list(binary_search_number))
        
        time.sleep(VOLTAGE_STABILIZATION_TIME)

        # Используем логическое выражение для замены if
        binary_search_number -= binary_search_exponent * (GPIO.input(comparator_module_pin) == 1)

        binary_search_exponent //= 2

    return binary_search_number

def get_voltage_from_troyka():
    return read_analog_voltage() / 256 * BASE_VOLTAGE_LEVEL

def display_voltage_on_leds(voltage: float):
    voltage_integer_value = int(voltage * 256 / BASE_VOLTAGE_LEVEL)
    GPIO.output(led_indicator_pins, convert_number_to_binary_list(voltage_integer_value))

voltage_readings = []
time_readings = []

MAXIMUM_CAPACITOR_VOLTAGE = 2.6
CHARGED_CAPACITOR_VOLTAGE = 0.97 * MAXIMUM_CAPACITOR_VOLTAGE
DISCHARGED_CAPACITOR_VOLTAGE = 0.20 * MAXIMUM_CAPACITOR_VOLTAGE

try:
    print("Charging capacitor...")
    experiment_start_time = time.time()
    GPIO.output(troyka_module_pin, 1)
    
    current_voltage = get_voltage_from_troyka()

    while current_voltage < CHARGED_CAPACITOR_VOLTAGE:
        time_readings.append(time.time() - experiment_start_time)
        voltage_readings.append(current_voltage)
        display_voltage_on_leds(current_voltage)
        time.sleep(0.01)
        current_voltage = get_voltage_from_troyka()

    charge_phase_data_points = len(voltage_readings)
    print("Capacitor is charged. Discharging...")
    print(f'Current time: {time_readings[-1]}')
    print(f'T = {time_readings[-1] / charge_phase_data_points}, f = {charge_phase_data_points / time_readings[-1]}')
    settings_file.write(f'T = {time_readings[-1] / charge_phase_data_points:.2f}, f = {charge_phase_data_points / time_readings[-1]:.2f}\n')
    settings_file.write(f'Points on charge: {charge_phase_data_points}\n')
    print(f'Points on charge: {charge_phase_data_points}')

    GPIO.output(troyka_module_pin, 0)

    while current_voltage > DISCHARGED_CAPACITOR_VOLTAGE:
        time_readings.append(time.time() - experiment_start_time)
        voltage_readings.append(current_voltage)
        display_voltage_on_leds(current_voltage)
        time.sleep(0.2)
        current_voltage = get_voltage_from_troyka()
        GPIO.output(digital_to_analog_converter_pins, 0)

    print(f'Experiment ended. Total time: {time_readings[-1]:.2f}')
    discharge_phase_data_points = len(time_readings) - charge_phase_data_points
    settings_file.write(f'T = {time_readings[-1] / discharge_phase_data_points}, f = {discharge_phase_data_points / time_readings[-1]}\n')
    settings_file.write(f'Points on discharge: {discharge_phase_data_points}\n')
    print(f'T = {time_readings[-1] / discharge_phase_data_points}, f = {discharge_phase_data_points / time_readings[-1]}')
    print(f'Points on charge: {discharge_phase_data_points}')

finally:
    GPIO.output(led_indicator_pins, 0)
    GPIO.output(digital_to_analog_converter_pins, 0)
    GPIO.output(troyka_module_pin, 0)
    GPIO.cleanup()

total_data_points = len(voltage_readings)

settings_file.write(f"ADC precision: {BASE_VOLTAGE_LEVEL/256} V\n")

settings_file.close()

with open("data.txt", "w") as data_file:
    for i in range(total_data_points):
        data_file.write(f'{time_readings[i]} {voltage_readings[i]}\n')

plt.plot(time_readings, voltage_readings)
plt.show()