import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


GPIO.setmode(GPIO.BCM)

dac    = [8, 11, 7, 1, 0, 5, 12, 6]
number = [0, 1, 0, 0, 0, 0, 0, 0]
zero   = [0, 0, 0, 0, 0, 0, 0, 0,]

GPIO.setup(dac, GPIO.OUT)
GPIO.output(dac, number)
time.sleep(10)

GPIO.output(dac, zero)

plt.plot([0, 5, 32, 64, 127, 255], [0.057, 0.137, 0.458, 0.866, 1.677, 3.255])
plt.show()

GPIO.cleanup()
