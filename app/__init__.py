import time
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from random import randrange
from enum import Enum

from numpy.random import rand
from picamera import PiCamera

from controls.behavior import turn_around
from playground.barrier.find_way import find_distances
from playground.cars.process import green_angle_prod, not_find_angle
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

try:
    camera
except NameError:
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 60
    camera.start_preview()
    camera.exposure_mode = 'sports'
    time.sleep(2)

image = np.empty((240 * 320 * 3,), dtype=np.uint8)
image = image.reshape((240, 320, 3))
index = 1
stuck_list = [0] * 50

class Mode(Enum):
    DISCOVER = 0
    HUNTING = 1
    PARKING = 2


class State:
    green_angle = not_find_angle
    grid_result = [7, 7, 7, 7]
    distance = 999
    current_image = None

    green_angle_changed = 0
    grid_result_changed = 0
    distance_changed = 0
    stuck_index = 0

    def asString(self):
        return f"green = {self.green_angle}, grid = {self.grid_result}, dist = {self.distance}, " \
               f"green_angle_changed = {self.green_angle_changed}, " \
               f"grid_result_changed = {self.grid_result_changed}, " \
               f"distance_changed = {self.distance_changed}"


def add_distance_to_stuck_list_and_check(self, dist, eps=0.1):
    stuck_list[self.state.stuck_index] = dist
    self.state.stuck_index += 1
    if self.state.stuck_index == 50:
        avg = sum(stuck_list) / self.state.stuck_index
        self.state.stuck_index = 0
        if abs(avg - stuck_list[0]) < eps:
            turn_around(90)

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
                time.sleep(0.1)
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
        if self.state.distance < 10:
            return Mode.DISCOVER

        if self.state.green_angle != not_find_angle:
            return Mode.HUNTING

        return Mode.PARKING

    def processDiscover(self):
        motor.forward(25)
        add_distance_to_stuck_list_and_check(self, self.state.distance)
        # motor.impluse(50, 0.1)

        # [left_close, right_close, left_outer, right_outer ]
        distances = self.state.grid_result
        if distances[0] <= 2 or distances[1] <= 2:
            if distances[0] < distances[1]:
                turn_around(90) # left
            else:
                turn_around(-90) # right
            # if randrange(0, 1, 1) > 0:
            #     turn_around(90)
            # else:
            #     turn_around(-90)

            return Mode.DISCOVER

        if distances[2] < distances[3]:
            min_outer = distances[2]
            left = True
        else:
            min_outer = distances[3]
            left = False

        if min_outer <= 6:
            # if left:
            #     servo.steer(100)
            # else:
            #     servo.steer(-100)
            if left:
                servo.steer(100 / (1 + max(min_outer, 1)))
            else:
                servo.steer(-100 / (1 + max(min_outer, 1)))
        else:
            servo.steer(0)
            if self.state.green_angle != not_find_angle:
                return Mode.HUNTING

        return Mode.DISCOVER

    def processHunting(self):
        distances = self.state.grid_result
        if distances[0] < distances[1]:
            min = distances[0]
        else:
            min = distances[1]

        if min < 4:
            return Mode.DISCOVER

        if self.state.green_angle == not_find_angle:
            return Mode.DISCOVER

        motor.forward(30)
        servo.steer(self.state.green_angle)

        return Mode.HUNTING

    def measure_distance(self):
        try:
            while True:
                try:
                    self.state.distance = distance.getDistance()
                    self.state.distance_changed = self.state.distance_changed + 1
                    time.sleep(0.1)
                except:
                    continue
        finally:
            distance.cleanup()

    def follow_green(self):
        while True:
            try:
                local_image = self.state.current_image
                if local_image is not None:
                    local_image = local_image.copy()
                    self.state.green_angle = green_angle_prod(local_image)
                    self.state.green_angle_changed = self.state.green_angle_changed + 1
            except Exception as e:
                continue

    def grid_calculate(self):
        while True:
            try:
                local_image = self.state.current_image
                if local_image is not None:
                    local_image = self.state.current_image.copy()
                    grid, result_grid = calculate_grid(True)
                    calculate_intersect_grid(local_image, grid, result_grid)
                    self.state.grid_result = find_distances(result_grid)
                    self.state.grid_result_changed = self.state.grid_result_changed + 1
            except Exception:
                continue

    def capture_camera(self):
        for _ in camera.capture_continuous(image, format='bgr', use_video_port=True):
            self.state.current_image = image.copy()
