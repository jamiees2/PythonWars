from .world import GameObject, EMPTY

class Portal(GameObject):
    type = "PORTAL"

    def __init__(self, id):
        self.id = id
        self._world = None
        self.matching_portal = None
        self.crate = False

    def collision(self, other):
        if other.type == 'CRATE':
            self.crate = True
            self.matching_portal.crate = True
            other.in_portal = True
            return True
        if not self.crate:
            x, y = self._world.get_object(self.matching_portal.id)
            self._world.move(other, x, y)
            self._world.tick()
            self._world._time.append([other.id, "TELEPORT", x, y])
        return None

