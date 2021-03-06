import app

try:
    import controls.servo as servo
    import controls.distance as distance
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.distance as distance
    import mock.motor as motor


if __name__ == '__main__':
    try:
        application = app.App()
        application.run()
    except KeyboardInterrupt:
        print("Closed")
    finally:
        print("Finish. Reseting..")
        servo.reset()
        motor.breakdown()

