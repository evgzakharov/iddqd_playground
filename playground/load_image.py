import cv2


def load_image(file: str):
    return cv2.imread(file, cv2.IMREAD_COLOR)