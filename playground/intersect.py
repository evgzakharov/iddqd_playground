from shapely.geometry import Polygon

if __name__ == '__main__':
    p1 = Polygon([(0, 0), (1, 1), (1, 0)])
    p2 = Polygon([(0, 1), (1, 0), (1, 1)])
    print(p1.intersects(p2))