from .world import GameObject, WALL

class Plate(GameObject):
    type = "PLATE"

    def __init__(self, id):
        self.id = id
        self._world = None
        self.used = False

    def collision(self, other):
        if not self.used:
            self.used = True
            return True
        return False

    def remove(self):
        self._world.destroy_object(self, WALL)


