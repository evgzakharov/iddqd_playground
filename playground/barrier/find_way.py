self_size = 6
free_y_size = 5
backward_y_size = 2

part_size = round(self_size / 2)


def find_distances(result_grid):
    center = round(len(result_grid) / 2)

    left_distance = _find_free_distance(result_grid, center - 1, -1)
    right_distance = _find_free_distance(result_grid, center, 1)

    return left_distance, right_distance


def _find_free_distance(result_grid, start_index, diff):
    free_distance = 0

    for y_index in range(0, free_y_size - 1):
        for x_index in range(0, part_size - 1):
            if result_grid[start_index + diff * x_index][y_index]:
                return free_distance
        free_distance = free_distance + 1

    return free_distance


