from .world import GameObject, EMPTY

class Crate(GameObject):
    type = "CRATE"

    def __init__(self, id):
        self.id = id
        self._world = None
        self.in_portal = False

    def collision(self, other):
        if not self.in_portal:
            rx, ry = self._world.get_object(other.id)
            x, y = self._world.get_object(self.id)
            if rx == x - 1:
                self._world.move_dir(self, 'RIGHT')
            elif rx == x + 1:
                self._world.move_dir(self, 'LEFT')
            elif ry == y - 1:
                self._world.move_dir(self, 'DOWN')
            else:
                self._world.move_dir(self, 'UP')
            self._world.tick()
        return True

