try:
    import controls.servo as servo
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.motor as motor
import time


def turnAround(angle=180):
    motor.breakdown()
    time.sleep(0.5)
    i = round(angle / 90)
    for _ in range(i):
        servo.steer_right(100)
        motor.impluse(-30, 1)
        servo.steer_left(100)
        motor.impluse(30, 1)
        time.sleep(0.5)


def stepLeft():
    servo.steer(-100)
    time.sleep(0.5)
    servo.steer(-100)
    time.sleep(0.5)
    servo.steer(0)


def stepRight():
    servo.steer(100)
    time.sleep(0.5)
    servo.steer(100)
    time.sleep(0.5)
    servo.steer(0)
