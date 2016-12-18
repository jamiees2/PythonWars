EMPTY = 1
WALL = 2



class GameObject(object):
    pass


class World(object):
    def __init__(self, maze):
        self._objects = {}
        self._moves = []
        self._time = []
        self._maze_default = maze
        self._maze_csv = '\n'.join(','.join(str(i) for i in row) for row in self._maze_default)
        self._maze = [list(j) for j in maze]

    def get_data(self, hidden=False):
        out = {"moves": self._moves, "maze": self._maze_csv}
        if hidden:
            out["maze"] = "".join(c if c in [",", "\n"] else str(WALL) for c in out["maze"])
        return out

    def get_at(self, x, y):
        if self.check_bounds(x, y):
            return self._maze[y][x]

    def create_object(self, o, x, y, static=True):
        if self.get_at(x, y) == EMPTY:
            o._world = self
            if static:
                self._maze_default[y][x] = o
            self._maze[y][x] = o
            self._time.append([o.id, 'CREATE', o.type, x, y])
            self._objects[o.id] = (x, y)
        else:
            raise TypeError("Can't place object on a wall")

    def destroy_object(self, o, repl=None):
        o_id = o.id
        x, y = self._objects[o_id]
        if repl is None:
            repl = self._maze_default[y][x]
        self._maze[y][x] == repl
        self._time.append([o.id, 'DESTRUCT'])
        del self._objects[o.id]

    def move(self, o, newx, newy):
        x, y = self.get_object(o.id)
        self._objects[o.id] = (newx, newy)
        self._maze[newy][newx] = o
        self._maze[y][x] = self._maze_default[y][x]

    def move_check(self, o, newx, newy):
        res = self.get_at(newx, newy)
        flag = False
        if isinstance(res, GameObject):
            flag = res.collision(o)
            if flag is None:
                return
        if res == EMPTY or flag:
            self.move(o, newx, newy)
        else:
            raise TypeError("Cannot walk through walls!")

    def move_dir(self, o, d):
        x, y = self.get_object(o.id)
        self._time.append([o.id, d])
        if d == 'UP':
            self.move_check(o, x, y - 1)
        elif d == 'DOWN':
            self.move_check(o, x, y + 1)
        elif d == 'LEFT':
            self.move_check(o, x - 1, y)
        elif d == 'RIGHT':
            self.move_check(o, x + 1, y)

    def get_object(self, id):
        return self._objects[id]

    def check_bounds(self, x, y):
        if 0 <= x < len(self._maze[0]):
            if 0 <= y < len(self._maze):
                return True
        raise TypeError("Arguments out of bounds")

    def tick(self):
        self._moves.append(self._time)
        self._time = []







