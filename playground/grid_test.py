import os
from os import listdir

from playground.grid.count_grid import count_grid
from playground.load_image import load_image

dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath("%s/../output" % dir)

if __name__ == '__main__':
    # for file in listdir("../robo_car3"):
    #     img = load_image(f"../robo_car3/{file}")
    #     process(img, output_dir, file)

    file = "new2_118.jpg"
    img = load_image(f"../robo_car3/{file}")
    count_grid(img, output_dir, f"{file}")

