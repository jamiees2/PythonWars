from .world import GameObject, EMPTY
from .robot import Robot


class Coin(GameObject):
    type = "COIN"

    def __init__(self, id):
        self.id = id
        self._world = None

    def collision(self, other):
        # On collision, collect the coin, but only if it is a robot
        if not isinstance(other, Robot):
            return None
        other.coins_collected += 1
        self._world.destroy_object(self, repl=EMPTY)
        return True

