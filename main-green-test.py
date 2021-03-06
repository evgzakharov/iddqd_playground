import time
from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from IPython.display import clear_output
import numpy as np
import cv2

try:
    import controls.servo as servo
    # import controls.distance as distance
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.distance as distance
    import mock.motor as motor


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

    hsv_min = np.array((53, 102, 90), np.uint8)
    hsv_max = np.array((86, 255, 255), np.uint8)

    hsv_min2 = np.array((53, 125, 147), np.uint8)
    hsv_max2 = np.array((74, 255, 255), np.uint8)

    # color_yellow = (0, 255, 255)

    for _ in camera.capture_continuous(image, format='bgr', use_video_port=True):
        clear_output(wait=True)
        img = image

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        thresh1 = cv2.inRange(hsv, hsv_min, hsv_max)
        thresh2 = cv2.inRange(hsv, hsv_min2, hsv_max2)
        thresh = thresh1 + thresh2

        moments = cv2.moments(thresh, 1)
        # dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']
        if dArea > 100:
            x = int(dM10 / dArea)
            # y = int(dM01 / dArea)
            # cv2.circle(img, (x, y), 5, color_yellow, 2)
            # cv2.putText(img, "%d-%d" % (x, y), (x + 10, y - 10),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

            wheel_angle = 0
            if x > 160:
                wheel_angle = round(((x - 160) / 160) * 100) * 1.85
                servo.steer(wheel_angle)
            elif x < 160:
                wheel_angle = -round((160 - x) / 160 * 100) * 1.45
                servo.steer(wheel_angle)

            # print(f"wheel={wheel_angle} x={x}")

            motor.forward(30)
        else:
            motor.roll()


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
