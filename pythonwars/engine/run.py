from .robot import Robot


def run(code, level):
    robot = Robot(1)
    # TODO: horrible, horrible security
    # Maybe run in subprocess (for timeout), and in pysandbox?
    d = {}
    exec(code, globals(), d)

    d['move'](robot)
    return robot._moves
