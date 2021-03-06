import os
from os import listdir
from playground.load_image import load_image
from playground.cars.process import process
from playground.cars.process import process_one

dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath("%s/../output/green" % dir)

if __name__ == '__main__':
    for file in listdir("../walls_test"):
        img = load_image(f"../walls_test/{file}")
        process(img, output_dir, 10, file)

    # img = load_image("../bad_color/color_bad_green_5.jpg")
    # process_one(img, output_dir, 5)
