import os
from os import listdir

from shapely.errors import TopologicalError

from playground.barrier.find_way import find_distances
from playground.grid.count_grid import display_grid, calculate_intersect_grid, calculate_grid
from playground.load_image import load_image

dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath("%s/../output" % dir)

if __name__ == '__main__':
    grid, result_grid = calculate_grid()

    # for file in listdir("../robo_car3"):
    #     try:
    #         img = load_image(f"../robo_car3/{file}")
    #         # calculate_intersect_grid(img, grid, result_grid)
    #         display_grid(img, output_dir, file, grid, result_grid)
    #
    #         distances = find_distances(result_grid)
    #         print(f"{file}={distances}")
    #     except TopologicalError:
    #         print(f"error={file}")
    #
    file = "color_1.jpg"
    img = load_image(f"../walls_test/{file}")
    display_grid(img, output_dir, f"{file}", grid, result_grid)
