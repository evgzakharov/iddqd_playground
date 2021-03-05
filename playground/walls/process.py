import cv2
import numpy as np

hsv_min = np.array((53, 00, 00), np.uint8)
hsv_max = np.array((83, 160, 255), np.uint8)

color_yellow = (0, 255, 255)


def process(img, output_dir):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.inRange(hsv, hsv_min, hsv_max)

    cv2.imwrite(f"{output_dir}/thresh.jpg", np.hstack((gray, thresh)))

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
