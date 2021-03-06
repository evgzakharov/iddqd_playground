import os

from playground.load_image import load_image
from playground.polygon.process import process

dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath("%s/../output/polygon" % dir)

if __name__ == '__main__':
    img = load_image("../robo_car3/new2_117.jpg")
    process(img, output_dir)