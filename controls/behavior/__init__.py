try:
    import controls.servo as servo
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.motor as motor
import time

def turnBack():
    motor.breakdown()
    time.sleep(0.5)
    servo.steer_right(100)
    motor.impluse(-30, 1)
    servo.steer_left(100)
    motor.impluse(30, 1)
    servo.steer_right(100)
    motor.impluse(-30, 1)
    servo.steer_left(100)
    motor.impluse(30, 1.2)
