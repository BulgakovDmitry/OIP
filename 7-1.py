import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)

# Определение пинов
dac_pins = [8, 11, 7, 1, 0, 5, 12, 6]
led_pins = [2, 3, 4, 17, 27, 22, 10, 9]

# Настройка пинов
GPIO.setup(led_pins, GPIO.OUT)
GPIO.setup(dac_pins, GPIO.OUT)

comp_pin = 14
troyka_pin = 13
GPIO.setup(troyka_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp_pin, GPIO.IN)

def decimal_to_binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def binary_to_decimal(binary_list):
    return sum(bit * (2 ** (7 - i)) for i, bit in enumerate(binary_list))

def read_voltage():
    return GPIO.input(comp_pin) * 3.3 / 256

def adc_simple():
    binary_output = [0] * 8
    for i in range(8):
        binary_output[i] = 1
        GPIO.output(dac_pins, binary_output)
        time.sleep(0.001)  
        if GPIO.input(comp_pin) == 1:
            binary_output[i] = 0
    GPIO.output(dac_pins, binary_output)
    return binary_to_decimal(binary_output) * (3.3 / 256)

def update_leds(voltage):
    GPIO.output(led_pins, decimal_to_binary(int(voltage * 255 / 3.3)))

try:
    voltage_data = []
    start_time = time.time()
    GPIO.output(troyka_pin, GPIO.HIGH)

    # Зарядка конденсатора
    while adc_simple() <= 0.8 * 3.3:
        voltage = adc_simple()
        voltage_data.append(voltage)
        update_leds(voltage)
        time.sleep(0.005)  

    GPIO.output(troyka_pin, GPIO.LOW)

    # Разрядка конденсатора
    while adc_simple() > 0.65 * 3.3:
        voltage = adc_simple()
        voltage_data.append(voltage)
        update_leds(voltage)
        time.sleep(0.005) 

    end_time = time.time()
    total_time = end_time - start_time

    # Сохранение данных
    voltage_str = [str(int(v * 255 / 3.3)) for v in voltage_data]
    with open('data.txt', 'w') as file:
        file.write('\n'.join(voltage_str))

    # Сохранение настроек
    quantization_step = 3.3 / 256
    sampling_rate = len(voltage_data) / total_time
    settings = [str(quantization_step), str(sampling_rate)]
    with open('settings.txt', 'w') as file:
        file.write('\n'.join(settings))

    # Вывод результатов
    print('Общая продолжительность эксперимента:', total_time)
    print('Период:', total_time / len(voltage_data))
    print('Частота дискретизации:', sampling_rate)
    print('Шаг квантования:', quantization_step)

    # Построение графика
    plt.plot(voltage_data)
    plt.show()

except KeyboardInterrupt:
    print('Программа была остановлена с клавиатуры')

finally:
    GPIO.output(dac_pins, 0)
    GPIO.cleanup()