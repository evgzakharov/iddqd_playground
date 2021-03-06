try:
    import controls.servo as servo
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.motor as motor
import time


def turn_around(angle=180):
    motor.breakdown()
    time.sleep(0.5)
    i = round(abs(angle) / 90)

    if angle > 0:
        mod = 1
    else:
        mod = -1

    for _ in range(i):
        servo.steer_right(100 * mod)
        motor.impluse(-30, 1)
        servo.steer_left(100 * mod)
        motor.impluse(30, 1)
        time.sleep(0.5)


def step_left():
    servo.steer(-100)
    time.sleep(0.5)
    servo.steer(-100)
    time.sleep(0.5)
    servo.steer(0)


def step_right():
    servo.steer(100)
    time.sleep(0.5)
    servo.steer(100)
    time.sleep(0.5)
    servo.steer(0)
