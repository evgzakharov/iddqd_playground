import time
from picamera import PiCamera
from IPython.display import clear_output
import numpy as np
import cv2
import controls.servo as servo

try:
    camera
except NameError:
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 60
    camera.start_preview()
    time.sleep(2)

class Delegate:
    def green_did_captured(self, angle):
        print("not implemented")

def capture(delegate: Delegate):
    global camera
    image = np.empty((240 * 320 * 3,), dtype=np.uint8)
    image = image.reshape((240, 320, 3))
    hsv_min = np.array((53, 55, 147), np.uint8)
    hsv_max = np.array((83, 255, 255), np.uint8)
    color_yellow = (0, 255, 255)

    for _ in camera.capture_continuous(image, format='rgb', use_video_port=True):
        clear_output(wait=True)
        img = image # cv2.flip(image, 1)  # отражение кадра вдоль оси Y

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)

        moments = cv2.moments(thresh, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']
        if dArea > 10:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            cv2.circle(img, (x, y), 5, color_yellow, 2)
            cv2.putText(img, "%d-%d" % (x, y), (x + 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

            delegate.green_did_captured(x)
