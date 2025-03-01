import RPi.GPIO as GPIO

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

number = [0 for i in range(8)]

def decimal2binary(value):
    return [int(bit) for bit in format(value, 'b').zfill(8)]

num = 0
try:
    while True:
        num = input("number 0 to 255: ")
        try:
            num = int(num)
            if 0 <= int(num) < 256:
                GPIO.output(dac, decimal2binary(num))
                voltage = float(num)/255*3.3
                print(f"Assumed voltage: {voltage: .4}V")
            else:
                if int(num) < 0:
                    print("entered number below zero")
                elif int(num) > 255:
                    print("entered number over max value")
        except Exception:
            try:
                num = float(num)
            except: ValueError
            print("Not a digit")
            if num == "q": break
            else:
                print("You typed in not decimal")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()