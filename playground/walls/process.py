import cv2
import imutils
import numpy as np

hsv_min = np.array((0, 90, 80), np.uint8)
hsv_max = np.array((15, 238, 250), np.uint8)

hsv_min2 = np.array((169, 86, 110), np.uint8)
hsv_max2 = np.array((179, 172, 251), np.uint8)

color_yellow = (0, 255, 255)


def process(img, output_dir, file):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh1 = cv2.inRange(hsv, hsv_min, hsv_max)
    thresh2 = cv2.inRange(hsv, hsv_min2, hsv_max2)
    thresh = thresh1 + thresh2

    # mask = cv2.erode(thresh, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)

    cv2.imwrite(f"{output_dir}/{file}", np.hstack((gray, mask)))

    return img
