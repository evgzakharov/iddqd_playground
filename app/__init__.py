import time
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from random import randrange
from enum import Enum

try:
    import controls.servo as servo
    import controls.distance as distance
    import controls.motor as motor
except ImportError:
    import mock.servo as servo
    import mock.distance as distance
    import mock.motor as motor


class Mode(Enum):
    DISCOVER = 0
    HUNTING = 1
    PARKING = 2


class State:
    green_angle: int
    grid_result: [int]
    distance: float

    def asString(self):
        return f"green = {self.green_angle}, grid = {self.grid_result}, dist = {self.distance}"


class App:
    mode: Mode
    state: State
    handlers: {}

    def __init__(self):
        self.state = State()
        self.mode = Mode.PARKING

        self.handlers = {}

    def run(self):
        try:
            while True:
                self.state = self.get_next_state()
                self.mode = self.get_next_mode()
                print(f"{self.mode} {self.state.asString()}")
        except KeyboardInterrupt:
            print("main.Closed")
        finally:
            distance.cleanup()

    def get_next_state(self):
        state = State()
        with PoolExecutor(max_workers=3) as executor:
            distance = executor.submit(self.measure_distance)
            green_angle = executor.submit(self.follow_green)
            grid_result = executor.submit(self.grid_calculate)
            state.distance = distance.result()
            state.green_angle = green_angle.result()
            state.grid_result = grid_result.result()
        return state

    def get_next_mode(self):
        handlers = {
            Mode.PARKING: self.processParking,
            Mode.DISCOVER: self.processDiscover,
            Mode.HUNTING: self.processHunting
        }
        return handlers[self.mode]()

    def processParking(self):
        # do some logic and return next state
        return Mode.DISCOVER

    def processDiscover(self):
        # do some logic and return next state
        return Mode.HUNTING

    def processHunting(self):
        # do some logic and return next state
        return Mode.PARKING

    def measure_distance(self):
        return distance.getDistance()

    def follow_green(self):
        # do green point angle calculation here
        return randrange(-100, 100)

    def grid_calculate(self):
        # do grid result calculation here
        time.sleep(1)
        return [randrange(-100, 100), randrange(-100, 100)]
