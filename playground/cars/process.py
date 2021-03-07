import cv2
import numpy as np

# Not green
# [76 52 74]
# [173  10  98]
# [84 47 82]
# [ 87  83 107]
# [ 86 101  63]

# [ 75 132  93] green
# [ 18 145 102]
hsv_min = np.array((18, 90, 70), np.uint8)
hsv_max = np.array((86, 255, 255), np.uint8)

hsv_min2 = np.array((53, 125, 147), np.uint8)
hsv_max2 = np.array((74, 255, 255), np.uint8)

red = (0, 0, 255)

area = 25


def process(img, output_dir, area, file):
    crop_img = img[60:240, 0:320]
    clear_img = crop_img.copy()
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # применяем цветовой фильтр
    thresh1 = cv2.inRange(hsv, hsv_min, hsv_max)
    thresh2 = cv2.inRange(hsv, hsv_min2, hsv_max2)
    thresh = thresh1 + thresh2

    cv2.imwrite(f"{output_dir}/{file}", np.hstack((gray, thresh)))

    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    if dArea > area:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(crop_img, (x, y), 5, red, 2)
        cv2.putText(crop_img, "%d-%d" % (x, y), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)

    cv2.imwrite(f"{output_dir}/thresh_{file}", np.hstack((clear_img, crop_img)))

    return crop_img


def process_one(img, output_dir, area):
    crop_img = img[60:240, 0:320]
    clear_img = crop_img.copy()
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
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
        cv2.circle(crop_img, (x, y), 5, red, 2)
        cv2.putText(crop_img, "%d-%d" % (x, y), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)

    cv2.imwrite(f"{output_dir}/thresh.jpg", np.hstack((clear_img, crop_img)))

    return crop_img


not_find_angle = -999

def green_angle_prod(img):
    crop_img = img[60:240, 0:320]
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    # применяем цветовой фильтр
    thresh1 = cv2.inRange(hsv, hsv_min, hsv_max)
    thresh2 = cv2.inRange(hsv, hsv_min2, hsv_max2)
    thresh = thresh1 + thresh2

    moments = cv2.moments(thresh, 1)
    dM10 = moments['m10']
    dArea = moments['m00']

    wheel_angle = not_find_angle

    if dArea > area:
        x = int(dM10 / dArea)
        if x > 160:
            wheel_angle = round(((x - 160) / 160) * 100) * 1.85
        elif x < 160:
            wheel_angle = -round((160 - x) / 160 * 100) * 1.45

        # print(f"wheel={wheel_angle} x={x}")

    return wheel_angle
