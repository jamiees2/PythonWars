from .world import GameObject, WALL, EMPTY


class Robot(GameObject):
    type = "PLAYER"

    def __init__(self, id):
        self.id = id
        self.coins_collected = 0
        self._world = None
        self.moves = 0
        self._hidden = False

    def _move(self, dir):
        # A generic move function, just pass through to world
        self.moves += 1
        self._world.move_dir(self, dir)
        self._world.tick()

    def collision(self, other):
        # Nothing may collide with me
        return False

    def see(self, x, y):
        # If we are in invisible mode, we only give the blocks immediately around us.
        if self._hidden:
            mx, my = self.get_pos()
            if abs(mx - x) > 1 or abs(my - y) > 1:
                return None
        # Otherwise, return whatever type of object is at that point
        res = self._world.get_at(x, y)
        if isinstance(res, GameObject):
            return res.type
        else:
            if res == WALL:
                return "WALL"
            elif res == EMPTY:
                return "EMPTY"

    def get_pos(self):
        # Return our x, y position
        return self._world.get_object(self.id)

    # Directional movement
    def up(self):
        self._move("UP")

    def down(self):
        self._move("DOWN")

    def left(self):
        self._move("LEFT")

    def right(self):
        self._move("RIGHT")
