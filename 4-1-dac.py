import RPi.GPIO as GPIO

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

binary_output = [0 for i in range(8)]

def convert_to_binary(value):
    return [int(bit) for bit in format(value, 'b').zfill(8)]

current_value = 0
try:
    while True:
        user_input = input("Enter a number from 0 to 255: ")
        try:
            current_value = int(user_input)
            if 0 <= current_value < 256:
                GPIO.output(dac, convert_to_binary(current_value))
                output_voltage = float(current_value) / 255 * 3.3
                print(f"Expected voltage: {output_voltage: .4}V")
            else:
                if current_value < 0:
                    print("Entered number is below zero")
                elif current_value > 255:
                    print("Entered number exceeds the maximum value")
        except ValueError:
            try:
                current_value = float(user_input)
            except ValueError:
                if user_input == "q":
                    break
                else:
                    print("Invalid input: not a digit")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()