from playground.load_image import load_image
from playground.walls.process import process

if __name__ == '__main__':
    img = load_image("../robo_car3/new2_104.jpg")
    img = process(img)
