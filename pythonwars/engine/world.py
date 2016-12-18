# The tilemap id's for walls and empty
EMPTY = 1
WALL = 2


# A game object class. All objects inherit this class
class GameObject(object):
    def remove(self):
        pass


class World(object):
    def __init__(self, maze):
        self._objects = {}
        self._moves = []
        self._time = []
        self._maze_default = maze
        self._maze_csv = '\n'.join(','.join(str(i) for i in row) for row in self._maze_default)
        # Copy the maze so we can reset
        self._maze = [list(j) for j in maze]

    def get_data(self, hidden=False):
        # Return the world and movement data for the json response
        out = {"moves": self._moves, "maze": self._maze_csv}
        if hidden:
            out["maze"] = "".join(c if c in [",", "\n"] else str(WALL) for c in out["maze"])
        return out

    def get_at(self, x, y):
        # Return the object at this position
        if self.check_bounds(x, y):
            return self._maze[y][x]

    def create_object(self, o, x, y, static=True):
        # Create an object, objects may only be placed on empty spaces, except plates can be placed anywhere
        if self.get_at(x, y) == EMPTY or o.type == 'PLATE':
            o._world = self
            if static:
                self._maze_default[y][x] = o
            self._maze[y][x] = o
            self._time.append([o.id, 'CREATE', o.type, x, y])
            self._objects[o.id] = (x, y)
        else:
            raise TypeError("Can't place object on a wall")

    def destroy_object(self, o, repl=None):
        # removes an object from the world
        o_id = o.id
        x, y = self._objects[o_id]
        # also clear it from the defaults, so it doesn't come back
        if self._maze[y][x] is self._maze_default[y][x]:
            if repl is None:
                raise TypeError("Must specify replacement for static objects!")
            self._maze_default[y][x] = repl
        elif repl is None:
            repl = self._maze_default[y][x]
        self._maze[y][x] = repl
        # update the time state
        self._time.append([o.id, 'DESTRUCT'])
        del self._objects[o.id]

    def move(self, o, newx, newy):
        # Moves an object from x to y, without regard to what is there
        x, y = self.get_object(o.id)
        self._objects[o.id] = (newx, newy)
        self._maze[newy][newx] = o
        self._maze[y][x] = self._maze_default[y][x]

    def move_check(self, o, newx, newy):
        # Move, but check first that there is not a wall before the object or an object blocking collision
        res = self.get_at(newx, newy)
        x, y = self.get_object(o.id)
        flag = False
        if isinstance(res, GameObject):
            # Call the collision function of the object
            flag = res.collision(o)
            if flag is None:
                return
        if res == EMPTY or flag:
            # move the object
            self.move(o, newx, newy)
            res = self.get_at(x, y)
            if isinstance(res, GameObject):
                res.remove()
        else:
            raise TypeError("Crashed into immovable object!")

    def move_dir(self, o, d):
        # Move in a specific direction
        x, y = self.get_object(o.id)
        # Update the time array
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
        # Return the x,y coords of an object
        return self._objects[id]

    def check_bounds(self, x, y):
        # Check that x, y are within the bounds of the maze
        if 0 <= x < len(self._maze[0]):
            if 0 <= y < len(self._maze):
                return True
        raise TypeError("Arguments out of bounds")

    def tick(self):
        # One step of the simulation has elapsed
        self._moves.append(self._time)
        self._time = []







