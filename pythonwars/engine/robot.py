class Robot(object):
    def __init__(self, id):
        self._moves = []
        self._id = id

    def moves(self):
        return self._moves

    def forward(self):
        self._moves.append({"id": self._id, "move": 1})

    def rotateLeft(self):
        self._moves.append({"id": self._id, "rotate": -1})

    def rotateRight(self):
        self._moves.append({"id": self._id, "rotate": 1})
