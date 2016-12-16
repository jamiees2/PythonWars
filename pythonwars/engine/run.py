from .robot import Robot
from .coin import Coin
from .world import World


def run(code, level):
    world = World(level)
    world.create_object(Coin("Coin1"), 1, 1)
    robot = Robot("Robot1")
    world.create_object(robot, 1, 2)

    world.tick()
    # TODO: better way of doing this?
    robot._world = world

    # TODO: horrible, horrible security
    # Maybe run in subprocess (for timeout), and in pysandbox?
    d = {}
    exec(code, globals(), d)

    d['move'](robot)
    return world._moves
