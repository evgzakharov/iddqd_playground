def cam_v(angle=0):
    print(f"{__name__}.cam_v {angle}")


def cam_h(angle=0):
    print(f"{__name__}.cam_h {angle}")


def steer(angle=0):
    print(f"{__name__}.steer {angle}")


def reset():
    print(f"{__name__}.reset")
    cam_v(0)
    cam_h(0)
    steer(0)


def check():
    print(f"{__name__}.check")
