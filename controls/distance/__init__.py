import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
__GPIO_TRIGGER = 18
__GPIO_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(__GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(__GPIO_ECHO, GPIO.IN)


def getDistance():
    # set Trigger to HIGH
    GPIO.output(__GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(__GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # save start_time
    while GPIO.input(__GPIO_ECHO) == 0:
        start_time = time.time()
    # save time of arrival
    while GPIO.input(__GPIO_ECHO) == 1:
        stop_time = time.time()
    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (time_elapsed * 34300) / 2
    return distance
