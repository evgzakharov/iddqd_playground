import os
from os import listdir

from playground.load_image import load_image
from playground.walls.process import process

dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath("%s/../output" % dir)

if __name__ == '__main__':
    for file in listdir("../walls_test"):
        img = load_image(f"../walls_test/{file}")
        process(img, output_dir, file)
    #
    # file = "color_final_8.jpg"
    # img = load_image(f"../walls_test/{file}")
    # process(img, output_dir, f"{file}")

