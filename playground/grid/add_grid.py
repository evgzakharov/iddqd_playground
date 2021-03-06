import math

import cv2
import numpy as np

line_thickness = 1
x_size = 320
y_size = 240
min_y_size = 80
color = (0, 255, 0)

start_y_diff = 20
start_x_diff = 23
x_angle = 0.22

def add_grid(img, output_dir, file):
    img_grid = img.copy()
    line_thickness = 1

    add_y_grids(img_grid, line_thickness)
    add_x_grids(img_grid, line_thickness, -1)
    add_x_grids(img_grid, line_thickness, 1)

    cv2.imwrite(f"{output_dir}/{file}", np.hstack((img, img_grid)))


def add_y_grids(img_grid, line_thickness):
    current_y = y_size
    y_diff = start_y_diff
    round_y_diff = max(round(y_diff), 1)

    while current_y + round_y_diff > min_y_size:
        cv2.line(img_grid, (0, current_y), (x_size, current_y), color, thickness=line_thickness)
        current_y = current_y - round_y_diff
        y_diff = y_diff * 0.9
        round_y_diff = round(y_diff)


def add_x_grids(img_grid, line_thickness, diff):
    current_x = round(x_size / 2)
    center_x = current_x

    current_x_top_diff = 0
    current_x_down_diff = 0
    iteration = 1

    addition = round(x_size / 3)
    while -addition < current_x < x_size + addition:
        cv2.line(img_grid, (center_x - round(current_x_top_diff) * diff, min_y_size), (current_x - current_x_down_diff * diff, y_size), color, thickness=line_thickness)
        current_x = current_x - start_x_diff * diff

        current_x_top_diff = current_x_top_diff + start_x_diff * x_angle
        current_x_down_diff = current_x_down_diff + start_x_diff
        iteration = iteration + 1
