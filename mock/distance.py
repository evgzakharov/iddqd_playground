distance = 100


def getDistance():
    global distance
    distance -= 5
    return distance


def cleanup():
    print(f"{__name__}.cleanup")
