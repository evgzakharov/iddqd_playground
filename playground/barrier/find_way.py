self_size1 = 6
self_size2 = 8
backward_y_size = 2

part_size1 = round(self_size1 / 2)
part_size2 = round(self_size2 / 2)


def find_distances(result_grid):
    center = round(len(result_grid) / 2)

    left_distance = _find_free_distance(result_grid, center - 1, -1, part_size1)
    right_distance = _find_free_distance(result_grid, center, 1, part_size1)

    left_distance2 = _find_free_distance(result_grid, center - 1, -1, part_size2)
    right_distance2 = _find_free_distance(result_grid, center, 1, part_size2)

    return left_distance, right_distance, left_distance2, right_distance2


def _find_free_distance(result_grid, start_index, diff, part_size):
    free_distance = 0

    for y_index in range(0, len(result_grid[0])):
        for x_index in range(0, part_size):
            if result_grid[start_index + diff * x_index][y_index]:
                return free_distance
        free_distance = free_distance + 1

    return free_distance


