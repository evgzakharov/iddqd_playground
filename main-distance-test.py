import time
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


grid, result_grid = calculate_grid(True)

def test_action():
    try:
        camera
    except NameError:
        camera = PiCamera()
        camera.resolution = (320, 240)
        camera.framerate = 60
        camera.start_preview()
        time.sleep(2)

    image = np.empty((240 * 320 * 3,), dtype=np.uint8)
    image = image.reshape((240, 320, 3))
    index = 1

    for _ in camera.capture_continuous(image, format='bgr', use_video_port=True):
        clear_output(wait=True)

        calculate_intersect_grid(image, grid, result_grid)
        distances = find_distances(result_grid)
        print(f"{distances}: {index}")

        index = index + 1


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
