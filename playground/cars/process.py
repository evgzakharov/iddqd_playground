import cv2
import numpy as np

# [76 52 74] bottom

# [ 75 132  93] green
# [ 70  70 138]
hsv_min = np.array((53, 80, 62), np.uint8)
hsv_max = np.array((75, 255, 255), np.uint8)

hsv_min2 = np.array((53, 125, 147), np.uint8)
hsv_max2 = np.array((74, 255, 255), np.uint8)

red = (0, 0, 255)


def process(img, output_dir, area):
    clear_img = img.copy()
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # применяем цветовой фильтр
    thresh1 = cv2.inRange(hsv, hsv_min, hsv_max)
    thresh2 = cv2.inRange(hsv, hsv_min2, hsv_max2)
    thresh = thresh1 + thresh2

    cv2.imwrite(f"{output_dir}/thresh_gray.jpg", np.hstack((gray, thresh)))

    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    if dArea > area:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x, y), 5, red, 2)
        cv2.putText(img, "%d-%d" % (x, y), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)

    cv2.imwrite(f"{output_dir}/thresh.jpg", np.hstack((clear_img, img)))

    return img