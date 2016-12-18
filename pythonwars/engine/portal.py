from .world import GameObject, EMPTY


class Portal(GameObject):
    type = "PORTAL"

    def __init__(self, id):
        self.id = id
        self._world = None
        self.matching_portal = None
        self.waiting = False

    def collision(self, other):
        if self.waiting:
            self.waiting = False
            return None
        x,y = self._world.get_object(self.matching_portal.id)
        print(x,y)
        self.matching_portal.waiting = True
        self._world.move_object(other,x,y)
        self._world._time.append([other.id, "TELEPORT", x, y])
        return None

