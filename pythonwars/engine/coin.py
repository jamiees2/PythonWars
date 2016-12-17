from .world import GameObject, EMPTY


class Coin(GameObject):
    type = "COIN"

    def __init__(self, id):
        self.id = id
        self._world = None

    def collision(self, other):
        other.coins_collected += 1
        self._world.destroy_object(self, repl=EMPTY)
        return True

