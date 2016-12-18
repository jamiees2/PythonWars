from .world import GameObject, EMPTY

class Portal(GameObject):
    type = "PORTAL"

    def __init__(self, id):
        self.id = id
        self._world = None
        self.matching_portal = None

    def collision(self, other):
        x, y = self._world.get_object(self.matching_portal.id)
        self._world.move(other, x, y)
        self._world.tick()
        self._world._time.append([other.id, "TELEPORT", x, y])
        return None

