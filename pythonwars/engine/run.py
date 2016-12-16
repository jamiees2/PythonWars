from .levels import levels


def run(code, level):
    data = levels[level]()
    robot = data["robot"]
    world = data["world"]

    # TODO: horrible, horrible security
    # Maybe run in subprocess (for timeout), and in pysandbox?
    d = {}
    exec(code, globals(), d)

    d['move'](robot)
    return world._moves
