import RPi.GPIO as GPIO
import time

pin = 16


def breath():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    p = GPIO.PWM(pin, 50)
    p.start(0)
    try:
        while 1:
            for dc in range(0, 61, 3):
                p.ChangeDutyCycle(dc)
                time.sleep(0.1 - (dc - 30)/1000.0)
            for dc in range(60, -1, -3):
                p.ChangeDutyCycle(dc)
                time.sleep(0.1 - (dc - 30)/1000.0)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    p.stop()
    GPIO.cleanup()
