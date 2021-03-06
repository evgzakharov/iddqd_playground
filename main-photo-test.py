import sys
import time
from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from IPython.display import clear_output
import numpy as np
import cv2

from playground.grid.count_grid import calculate_grid, calculate_intersect_grid, display_grid

try:
    import controls.servo as servo
    # import controls.distance as distance
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.distance as distance
    import mock.motor as motor


grid, result_grid = calculate_grid()

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

    camera.capture(image, format='bgr', use_video_port=True)
    clear_output(wait=True)
    cv2.imwrite(f"walls_test/color_{sys.argv[1]}.jpg", image)
    print(1)


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
