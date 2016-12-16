import csv

EMPTY = 1
WALL = 2

class GameObject(object):
    pass

class World(object):
    def __init__(self, file):
        self._maze = []
        self._objects = {}
        self._moves = []
        self._time = []
        with open(file) as c:
            reader = csv.reader(c)
            for row in reader:
                self._maze.append(row)
        self._s = '\n'.join(','.join(str(i) for i in row) for row in self._maze)


    def get_at(x,y):
        if self.check_bounds(x,y):
            return self._maze[x][y]

    def create_object(o,x,y):
        if self.get_at(x,y) == EMPTY:
            o._world = self
            self._maze[x][y] = o
            self._time.append([o.id, 'CREATE', o.type, x, y])
        else:
            raise TypeError("Can't place object on a wall")

    def destroy_object(o):
        o_id = o.id
        x,y = self._objects[o_id]
        self._maze[x][y] == EMPTY
        self._time.append([o.id, 'DESTRUCT'])

    def move_object(o,newx,newy):
        x,y = self.get_object(o.id)
        res = self.get_at(newx,newy)
        flag = False
        if isinstance(res,GameObject):
            flag = res.collision(o)
        if res == EMPTY or flag:
            self._objects[o_id] = (newx,newy)
            self._maze[newx][newy] = o
            self._maze[x][y] = EMPTY

    def move(o,d):
        x,y = self.get_object(o.id)
        if d == 'UP':
            self.move_object(o,x,y+1)
            self._time.append([o.id,'UP'])
        elif d == 'DOWN':
            self.move_object(o,x,y-1)
            self._time.append([o.id,'DOWN'])
        elif d == 'LEFT':
            self.move_object(o,x-1,y)
            self._time.append([o.id,'LEFT'])
        elif d == 'RIGHT':
            self.move_object(o,x+1,y)
            self._time.append([o.id,'RIGHT'])


    def get_object(id):
        return self._objects[id]

    def check_bounds(x,y):
        if 0 < x < len(self._maze):
            if 0 < y < len(self._maze[0]):
                return True
        raise TypeError("Arguments out of bounds")

    def tick():
        self._moves.append(self._time)
        self._time = []






 
