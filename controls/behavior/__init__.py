try:
    import controls.servo as servo
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.motor as motor
import time

def turnBack():
    motor.breakdown()
    time.sleep(1)
    servo.steer(-100)
    time.sleep(0.5)
    motor.backward(30)
    time.sleep(1)
    servo.steer(0)
    time.sleep(1)