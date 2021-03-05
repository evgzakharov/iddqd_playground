import math

import cv2
import numpy as np

from playground.walls.process import find_contours

line_thickness = 1
x_size = 320
y_size = 240
min_y_size = 80
color = (0, 255, 0)

start_y_diff = 20
start_x_diff = 23


def count_grid(img, output_dir, file):
    img_grid = img.copy()
    line_thickness = 1

    cnts = find_contours(img)

    y_lines = calculate_y_grids()
    x_lines = calculate_x_grids(-1) + calculate_x_grids(1)

    # calculate_x_grids(img_grid, line_thickness, cnts, -1)
    # calculate_x_grids(img_grid, line_thickness, cnts, 1)

    # cv2.imwrite(f"{output_dir}/{file}", np.hstack((img, img_grid)))


def calculate_y_grids():
    lines = []

    current_y = y_size
    y_diff = start_y_diff
    round_y_diff = max(round(y_diff), 1)

    while current_y + round_y_diff > min_y_size:
        lines.append(((0, current_y), (x_size, current_y)))
        current_y = current_y - round_y_diff
        y_diff = y_diff * 0.9
        round_y_diff = round(y_diff)

    return lines


def calculate_x_grids(diff):
    lines = []

    current_x = round(x_size / 2)
    center_x = current_x

    current_x_top_diff = 0
    current_x_down_diff = 0
    iteration = 1

    addition = round(x_size / 3)
    while -addition < current_x < x_size + addition:
        lines.append(((center_x - round(current_x_top_diff) * diff, min_y_size), (current_x - current_x_down_diff * diff, y_size)))
        current_x = current_x - start_x_diff * diff

        current_x_top_diff = current_x_top_diff + start_x_diff * 0.22
        current_x_down_diff = current_x_down_diff + start_x_diff
        iteration = iteration + 1

    return lines
