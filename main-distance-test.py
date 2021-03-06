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


grid, result_grid = calculate_grid(True)

executor = ThreadPoolExecutor(max_workers=4)

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

        executor.submit(lambda: calculate_intersect_grid(image, grid, result_grid))

        distances = find_distances(result_grid)
        print(distances)

        if distances[0] <= 1 and distances[1] <= 1:
            # motor.backward(30)
            servo.steer(0)
            continue

        # motor.forward(30)

        if distances[0] < distances[1]:
            min = distances[0]
            left = True
        else:
            min = distances[1]
            left = False

        if min < 3:
            if left:
                servo.steer(80)
            else:
                servo.steer(-80)
        else:
            servo.steer(0)

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
