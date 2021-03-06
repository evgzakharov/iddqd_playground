import cv2
import numpy as np
from shapely.errors import TopologicalError
from shapely.geometry import Polygon

from playground.walls.process import find_contours

line_thickness = 1
x_size = 320
y_size = 240
min_y_size = 80
color = (0, 255, 0)

start_y_diff = 20
start_x_diff = 23


def calculate_grid():
    grid = []
    y_lines = _calculate_y_grids()
    x_lines = []
    left_x = _calculate_x_grids(1)
    left_x.reverse()
    x_lines.extend(left_x)
    x_lines.extend(_calculate_x_grids(-1))

    result_grid = []

    for x_index in range(len(x_lines) - 2):
        line_grid = []
        result_line = []
        for y_index in range(len(y_lines) - 2):
            left_x = x_lines[x_index]
            right_x = x_lines[x_index + 1]

            top_y = y_lines[y_index]
            bottom_y = y_lines[y_index + 1]

            points = [
                _cross(left_x, top_y),
                _cross(right_x, top_y),
                _cross(right_x, bottom_y),
                _cross(left_x, bottom_y),
            ]

            line_grid.append(points)
            result_line.append(False)

        grid.append(line_grid)
        result_grid.append(result_line)

    return grid, result_grid


def calculate_intersect_grid(img, grid, result_grid):
    cnts = find_contours(img)

    for x_index in range(len(grid) - 2):
        line_grid = grid[x_index]
        result_line = result_grid[x_index]

        for y_index in range(len(line_grid) - 2):
            points = line_grid[y_index]
            if _intersect(cnts, points):
                result_line[y_index] = True
            else:
                result_line[y_index] = False

    return result_grid


def display_grid(img, output_dir, file, grid, result_grid):
    img_grid = img.copy()
    cnts = find_contours(img)

    for x_index in range(len(grid) - 2):
        line_grid = grid[x_index]
        for y_index in range(len(line_grid) - 2):
            points = line_grid[y_index]
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img_grid, [pts], True, (0, 0, 255))

            if _intersect(cnts, points):
                cv2.polylines(img_grid, [pts], True, (0, 0, 255))
            else:
                cv2.polylines(img_grid, [pts], True, (0, 255, 0))

    cv2.imwrite(f"{output_dir}/{file}", np.hstack((img, img_grid)))


def _intersect(cnts, points):
    for cnt in cnts:
        prepared = np.squeeze(cnt)
        if len(prepared.shape) < 2 or prepared.shape[0] < 3:
            continue
        try:
            if Polygon(points).intersects(Polygon(np.squeeze(cnt))):
                return True
        except TopologicalError:
            continue

    return False


def _cross(line1, line2):
    x1 = line1[0][0]
    y1 = line1[0][1]
    x2 = line1[1][0]
    y2 = line1[1][1]

    x3 = line2[0][0]
    y3 = line2[0][1]
    x4 = line2[1][0]
    y4 = line2[1][1]

    if y2 - y1 != 0:
        q = (x2 - x1) / (y1 - y2)
        sn = (x3 - x4) + (y3 - y4) * q
        fn = (x3 - x1) + (y3 - y1) * q
        n = fn / sn
    else:
        n = (y3 - y1) / (y3 - y4)

    x_cross = x3 + (x4 - x3) * n
    y_cross = y3 + (y4 - y3) * n
    return [x_cross, y_cross]


def _calculate_y_grids():
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


def _calculate_x_grids(diff):
    lines = []

    current_x = round(x_size / 2)
    center_x = current_x

    current_x_top_diff = 0
    current_x_down_diff = 0
    iteration = 1

    addition = round(x_size / 3)
    while -addition < current_x < x_size + addition:
        lines.append(((center_x - round(current_x_top_diff) * diff, min_y_size),
                      (current_x - current_x_down_diff * diff, y_size)))
        current_x = current_x - start_x_diff * diff

        current_x_top_diff = current_x_top_diff + start_x_diff * 0.22
        current_x_down_diff = current_x_down_diff + start_x_diff
        iteration = iteration + 1

    return lines
