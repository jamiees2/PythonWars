from .world import GameObject


class Robot(GameObject):
    type = "PLAYER"

    def __init__(self, id):
        self.id = id
        self.coins_collected = 0
        self._world = None
        self.moves = 0

    def _move(self, dir):
        self.moves += 1
        self._world.move_dir(self, dir)
        self._world.tick()

    def collision(self, other):
        return False

    def up(self):
        self._move("UP")

    def down(self):
        self._move("DOWN")

    def left(self):
        self._move("LEFT")

    def right(self):
        self._move("RIGHT")
