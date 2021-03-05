import time
import asyncio
from app.state import CarState
from app.state import CarStateDelegate
from controls.camera.follow_green import Delegate as GreenDelegate
# from controls.camera.follow_green import capture as GreenCapture
try:
    import controls.servo as servo
    import controls.distance as distance
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.distance as distance
    import mock.motor as motor

import controls.behavior as behavior

class App(CarStateDelegate, GreenDelegate):

    distance = 999

    def __init__(self):
        self._state = CarState()
        self._state.delegate = self
        # GreenCapture(self)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        print("setter of x called")
        self._state = value

    def run(self):
        try:
            while True:
                self.measure_distance()
                print(f"distance {self.distance}")
                if self.state.current_state == self.state.parking:
                    self.parking(self.state)
                if self.state.current_state == self.state.discover:
                    self.discover(self.state)
                if self.state.current_state == self.state.hunting:
                    self.hunting(self.state)

                time.sleep(0.2)
        finally:
            distance.cleanup()

    def measure_distance(self):
        self.distance = distance.getDistance()

    def on_exit_state(self, state):
        print(f"exit {state}")

    def on_enter_state(self, state):
        print(f"enter {state}")

    def green_did_captured(self, angle):
        if angle > 160:
            servo.steer(round((320 - angle) / 160 * 100))
        elif angle < 160:
            servo.steer(-round(angle / 160 * 100))

    def parking(self, state):
        motor.roll()
        servo.cam_v(0)
        if self.distance < 50:
            state.discoverArea()

    def discover(self, state):
        motor.forward(20)
        servo.cam_v(0)
        if self.distance < 20:
            state.goHunting()
        if self.distance > 50:
            state.stopMachine()

    def hunting(self, state):
        motor.forward(30)
        servo.cam_v(40)
        if self.distance > 20:
            state.discoverArea()
