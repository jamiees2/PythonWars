from .world import GameObject


class Robot(GameObject):
    type = "PLAYER"

    def __init__(self, id):
        self.id = id
        self.coins_collected = 0
        self._world = None

    def _move(self, dir):
        self._world.move(self, dir)
        self._world.tick()

    def up(self):
        self._move("UP")

    def down(self):
        self._move("DOWN")

    def left(self):
        self._move("LEFT")

    def right(self):
        self._move("RIGHT")
