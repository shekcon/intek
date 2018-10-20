from collections import deque

class Parent():
    def __init__(self, id_parent, pos):
        self.id = id_parent
        self.pos = pos
        self.found = False
        self.parent = deque([pos])
        self.child = deque()

    def add_child(self, other):
        if other is not None:
            self.child.extend(other)

    def pop_parent(self):
        try:
            return self.parent.popleft()
        except Exception:
            return None

    def refesh_parent(self):
        self.parent = self.child.copy()
        self.child = deque()

class Track():
    def __init__(self, maze):
        self.row = len(maze)
        self.col = len(maze[0])
        self.maze_track = []
        self.empty_track()

    def mark(self, pos):
        self.maze_track[pos[0]][pos[1]] = " "

    def is_mark(self, pos):
        return self.maze_track[pos[0]][pos[1]] == " "

    def empty_track(self):
        del self.maze_track[:]
        for _ in range(self.row):
            self.maze_track.append(["#" for _ in range(self.col)])
