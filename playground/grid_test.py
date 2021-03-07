import os
import time
from os import listdir

from shapely.errors import TopologicalError

from playground.barrier.find_way import find_distances
from playground.grid.count_grid import display_grid, calculate_intersect_grid, calculate_grid
from playground.load_image import load_image

dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath("%s/../output" % dir)

if __name__ == '__main__':
    start_time = time.time()
    for file in listdir("../walls_test"):
        try:
            img = load_image(f"../walls_test/{file}")
            grid, result_grid = calculate_grid(False)
            display_grid(img, output_dir, file, grid, result_grid)

            grid, result_grid = calculate_grid(True)
            calculate_intersect_grid(img, grid, result_grid)
            distances = find_distances(result_grid)
            print(f"{file}={distances}")
        except TopologicalError:
            print(f"error={file}")


    end_time = time.time()
    print(f"time={end_time - start_time}")



    # grid, result_grid = calculate_grid(False)
    # file = "color_wall_bad_3.jpg"
    # img = load_image(f"../walls_test/{file}")
    # display_grid(img, output_dir, f"{file}", grid, result_grid)
    #
    # grid, result_grid = calculate_grid(True)
    # calculate_intersect_grid(img, grid, result_grid)
    # distances = find_distances(result_grid)
    # print(f"{file}={distances}")
