import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
p = GPIO.PWM(25, 261)


def play(freq, delay):
    p.start(freq)
    time.sleep(delay)
    p.stop()


def pause(delay):
    time.sleep(delay)


def cleanup():
    GPIO.cleanup()


def play_intro():
    i = 0
    while True:
        try:
            play(20, 0.05)
            pause(0.5 / (i + 1))
            play(40, 0.01)
            i = i + 1
            if i > 100:
                break
        except:
            pass
