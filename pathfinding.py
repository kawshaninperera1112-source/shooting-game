from collections import deque


class PathFinding:
    """Breadth-first-search pathfinding on the tile grid.

    Instead of running one BFS per enemy per frame, we run a single BFS outward
    from the player. That gives every reachable tile a pointer to the neighbouring
    tile that is one step closer to the player, so every enemy can look up its next
    step instantly. The result only changes when the player moves to a new tile
    (the walls never change), so it is cached until then.
    """

    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self._goal = None
        self._toward_goal = {}
        self.get_graph()

    def get_path(self, start, goal):
        """Return the next tile to step to when walking from `start` towards `goal`."""
        if start == goal:
            return goal
        if goal != self._goal:
            self._toward_goal = self.bfs(goal)
            self._goal = goal
        return self._toward_goal.get(start, start)   # unreachable tile: stay where we are

    def bfs(self, goal):
        queue = deque([goal])
        toward_goal = {goal: None}

        while queue:
            cur_node = queue.popleft()
            for next_node in self.graph.get(cur_node, ()):
                if next_node not in toward_goal:
                    toward_goal[next_node] = cur_node
                    queue.append(next_node)
        return toward_goal

    def get_next_nodes(self, x, y):
        world_map = self.game.map.world_map
        nodes = []
        for dx, dy in self.ways:
            if (x + dx, y + dy) in world_map:
                continue
            # no diagonal moves that cut through the corner of a wall
            if dx and dy and ((x + dx, y) in world_map or (x, y + dy) in world_map):
                continue
            nodes.append((x + dx, y + dy))
        return nodes

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if not tile:
                    self.graph[(x, y)] = self.get_next_nodes(x, y)