from Raspi_MotorHAT import Raspi_PWM_Servo_Driver
import time

pwm = Raspi_PWM_Servo_Driver.PWM(0x70)

# можно попробовать другую частоту
pwm.setPWMFreq(250)

# pwm1.setPWMFreq(60) - вообще по спецификации 60Гц. Но тогда и на ШИМ двигателя тоже пойдёт 60.
# Сделать разные частоты у меня не вышло

pwm.setPWM(14, 0, 0)
pwm.setPWM(0, 0, 0)
pwm.setPWM(1, 0, 0)

# допустимые диапазоны значений
__camera_v = [1200, 1800]
__camera_h = [650, 2150]
__steering = [2250, 2650]


def __cam_v_set(value):
    pwm.setPWM(0, 0, value)


def __cam_h_set(value):
    pwm.setPWM(1, 0, value)


def __steer_set(value):
    pwm.setPWM(14, 0, value)


def smooth():
    val = -90
    while val < 90:
        cam_h(val)
        val += 10
        time.sleep(0.2)


def cam_v(angle=0):
    angle = max(-100, angle)
    angle = min(100, angle)
    mid = sum(__camera_v) / len(__camera_v)
    value = mid + (mid - min(__camera_v)) * angle / 100
    __cam_v_set(int(value))


def cam_h(angle=0):
    angle = max(-100, angle)
    angle = min(100, angle)
    mid = sum(__camera_h) / len(__camera_h)
    value = mid + (mid - min(__camera_h)) * angle / 100
    __cam_h_set(int(value))


def steer(angle=0):
    angle = max(-100, angle)
    angle = min(100, angle)
    mid = sum(__steering) / len(__steering)
    value = mid + (mid - min(__steering)) * angle / 100
    __steer_set(int(value))


def reset():
    cam_v(0)
    cam_h(0)
    steer(0)


def check():
    for angle in [-100, 0, 100, 0]:
        cam_v(angle)
        time.sleep(0.3)
        cam_h(angle)
        time.sleep(0.3)
        steer(angle)
        time.sleep(0.5)
