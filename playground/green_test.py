import os

from playground.load_image import load_image
from playground.cars.process import process

dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath("%s/../output/green" % dir)

if __name__ == '__main__':
    img = load_image("../calibrate_2_6.jpg")
    process(img, output_dir, 1)
