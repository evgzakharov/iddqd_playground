import time
from concurrent.futures.thread import ThreadPoolExecutor
from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from IPython.display import clear_output
import numpy as np
import cv2

from playground.barrier.find_way import find_distances
from playground.grid.count_grid import calculate_grid, calculate_intersect_grid, display_grid

try:
    import controls.servo as servo
    # import controls.distance as distance
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.distance as distance
    import mock.motor as motor

from controls.behavior import turnAround, stepLeft, stepRight


def test_action():
    turnAround(360)


def start():
    try:
        print("start")
        test_action()
    except KeyboardInterrupt:
        print("Closed")
    finally:
        print("Finish. Reseting..")
        servo.reset()
        motor.breakdown()


start()
