import cv2
import imutils
import numpy as np

# [  2 250 103]

hsv_min = np.array((0, 90, 80), np.uint8)
hsv_max = np.array((15, 250, 250), np.uint8)

hsv_min2 = np.array((169, 86, 110), np.uint8)
hsv_max2 = np.array((179, 172, 251), np.uint8)

color_yellow = (0, 255, 255)

def find_contours(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    thresh1 = cv2.inRange(hsv, hsv_min, hsv_max)
    thresh2 = cv2.inRange(hsv, hsv_min2, hsv_max2)
    thresh = thresh1 + thresh2

    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return imutils.grab_contours(cnts)


def process(img, output_dir, file):
    cnts = find_contours2(img, output_dir, file)
    img_with_cntrs = img.copy()
    for contour in cnts:
        cv2.polylines(img_with_cntrs, [contour], True, (0, 255, 0))

    cv2.imwrite(f"{output_dir}/{file}", np.hstack((img, img_with_cntrs)))

    return img

def find_contours2(img, output_dir, file):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh1 = cv2.inRange(hsv, hsv_min, hsv_max)
    thresh2 = cv2.inRange(hsv, hsv_min2, hsv_max2)
    thresh = thresh1 + thresh2

    cv2.imwrite(f"{output_dir}/grey_{file}", np.hstack((gray, thresh)))

    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    cv2.imwrite(f"{output_dir}/gray_proc_{file}", np.hstack((gray, thresh)))

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return imutils.grab_contours(cnts)
