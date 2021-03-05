import cv2
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

    cv2.imwrite(f"{output_dir}/{file}", np.hstack((gray, thresh)))

    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    if dArea > 100:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x, y), 5, color_yellow, 2)
        cv2.putText(img, "%d-%d" % (x, y), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

    return img
