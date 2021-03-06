import time
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from random import randrange
from enum import Enum
from picamera import PiCamera
from playground.barrier.find_way import find_distances
from playground.grid.count_grid import calculate_grid, calculate_intersect_grid
import numpy as np

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
    current_image = None

    def asString(self):
        return f"green = {self.green_angle}, grid = {self.grid_result}, dist = {self.distance}"


grid, result_grid = calculate_grid(True)


class App:
    mode: Mode
    state: State
    handlers: {}
    executor = PoolExecutor(max_workers=4)

    def __init__(self):
        self.state = State()
        self.mode = Mode.PARKING

        self.handlers = {}

    def run(self):
        self.start_input_measure()
        try:
            while True:
                self.mode = self.get_next_mode()
                print(f"{self.mode} {self.state.asString()}")
                time.sleep(1)
        except KeyboardInterrupt:
            print("main.Closed")
        finally:
            distance.cleanup()

    def start_input_measure(self):
        self.executor.submit(self.measure_distance)
        self.executor.submit(self.follow_green)
        self.executor.submit(self.grid_calculate)
        self.executor.submit(self.capture_camera)

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
        try:
            while True:
                try:
                    self.state.distance = distance.getDistance()
                except:
                    continue
        finally:
            distance.cleanup()

    def follow_green(self):
        while True:
            self.state.green_angle = randrange(-100, 100)

    def grid_calculate(self):
        while True:
            if self.state.current_image is not None:
                calculate_intersect_grid(self.state.current_image, grid, result_grid)
                self.state.grid_result = find_distances(result_grid)

    def capture_camera(self):
        try:
            camera
        except NameError:
            camera = PiCamera()
            camera.resolution = (320, 240)
            camera.framerate = 60
            camera.start_preview()
            time.sleep(2)
        image = np.empty((240 * 320 * 3,), dtype=np.uint8)
        image = image.reshape((240, 320, 3))
        index = 1
        for _ in camera.capture_continuous(image, format='bgr', use_video_port=True):
            self.state.current_image = image
