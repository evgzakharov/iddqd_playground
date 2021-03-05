import cv2 as cv
import numpy as np


def process(img, output_dir):
    clear_img = img.copy()
    pts = np.array([[37, 193], [102, 137], [220, 137], [296, 193]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv.polylines(img, [pts], True, (0, 0, 255))

    cv.imwrite(f"{output_dir}/thresh.jpg", np.hstack((clear_img, img)))


    return img