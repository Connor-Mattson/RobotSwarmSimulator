from ..obstacles.Wall import Wall
import random
import time

class Node:
    def __init__(self, i, j):
        self.i = i
        self.j = j

        # 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT
        self.edges = []

    def add_edge(self, max_i, max_j):
        if len(self.edges) == 4:
            return None
        possible_edges = []
        if self.j > 0 and 3 not in self.edges:
            possible_edges.append(3)
        if self.i < (max_i - 1) and 2 not in self.edges:
            possible_edges.append(2)
        if self.j < (max_j - 1) and 1 not in self.edges:
            possible_edges.append(1)
        if self.i > 0 and 0 not in self.edges:
            possible_edges.append(0)
        if not possible_edges:
            return None
        choice = random.choice(possible_edges)
        self.edges.append(choice)

        if choice == 0:
            return [-1, 0]
        elif choice == 1:
            return [0, 1]
        elif choice == 2:
            return [1, 0]
        elif choice == 3:
            return [0, -1]
        return None

    def add_exact_edge(self, i_offset, j_offset):
        if i_offset == -1 and j_offset == 0:
            self.edges.append(0)
        elif i_offset == 1 and j_offset == 0:
            self.edges.append(2)
        elif i_offset == 0 and j_offset == -1:
            self.edges.append(3)
        elif i_offset == 0 and j_offset == 1:
            self.edges.append(1)

    def __str__(self):
        return f"{(self.i, self.j)}, E: {self.edges}"

    def __repr__(self):
        return f"({(self.i, self.j)}, E: {self.edges})"

class Maze:
    def __init__(self, world_w, world_h, grid_w, grid_h, wall_width=2, padding=10):
        self.world_dims = (world_w, world_h)
        self.cells = (grid_w, grid_h)
        self.total_states = grid_w * grid_h
        self.graph = [[Node(i, j) for j in range(grid_w)] for i in range(grid_h)]
        self.wall_width = wall_width
        self.padding = padding

    def wall_between(self, i1, j1, i2, j2):
        cell_w, cell_h = self.world_dims[0] // self.cells[0], self.world_dims[1] // self.cells[1]

        x1, x2 = (j1 * cell_w), (j2 * cell_w)
        y1, y2 = (i1 * cell_h), (i2 * cell_h)
        x1, x2 = x1 + self.padding, x2 + self.padding
        y1, y2 = y1 + self.padding, y2 + self.padding

        upper_corner = (min(x1, x2), min(y1, y2))
        lower_corner = (max(x1, x2) + self.wall_width, max(y1, y2) + self.wall_width)
        w, h = lower_corner[0] - upper_corner[0], lower_corner[1] - upper_corner[1]
        return Wall(None, upper_corner[0], upper_corner[1], w, h)

    def get_wall_representation(self):
        walls = []
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                # Check Down, then check Right
                state = self.graph[i][j]
                if state.i < self.cells[1] - 1 and 2 not in state.edges:
                    walls.append(self.wall_between(state.i, state.j, state.i + 1, state.j))
                if state.j < self.cells[0] - 1 and 1 not in state.edges:
                    walls.append(self.wall_between(state.i, state.j, state.i, state.j + 1))
        return walls

    def solve_and_return(self):
        # First Pass
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                if len(self.graph[i][j].edges) == 0:
                    step_i, step_j = self.graph[i][j].add_edge(self.cells[1], self.cells[0])
                    self.graph[i + step_i][j + step_j].add_exact_edge(-step_i, -step_j)

        fully_explorable = False
        while not fully_explorable:
            bfs_full, seen = self.BFS_Fully_Explorable()
            print(bfs_full, str(seen))
            if bfs_full:
                fully_explorable = True
            else:
                for i in range(len(self.graph)):
                    added = False
                    for j in range(len(self.graph[i])):
                        if self.graph[i][j] not in seen and len(self.graph[i][j].edges) < 4:
                            step = self.graph[i][j].add_edge(self.cells[1], self.cells[0])
                            if step is None:
                                continue
                            step_i, step_j = step
                            self.graph[i + step_i][j + step_j].add_exact_edge(-step_i, -step_j)
                            added = True
                            break

        return self.get_wall_representation()

    def BFS_Fully_Explorable(self):
        seen = [self.graph[0][0]]
        queue = [self.graph[0][0]]
        while queue:
            state = queue.pop(0)
            outbound_edges = []
            for edge in state.edges:
                if edge == 0:
                    outbound_edges.append(self.graph[state.i - 1][state.j])
                elif edge == 1:
                    outbound_edges.append(self.graph[state.i][state.j + 1])
                elif edge == 2:
                    outbound_edges.append(self.graph[state.i + 1][state.j])
                elif edge == 3:
                    outbound_edges.append(self.graph[state.i][state.j - 1])
            for node in outbound_edges:
                if node not in seen:
                    seen.append(node)
                    queue.append(node)

        return len(seen) == self.total_states, seen

