"""
Return a sequence of moves that, no matter where the robot starts, it will always pass the EXIT

######
#.#E.#
#....#
######

DRRUL

# return shortest command or any command?
# ANY

# all points are reachable and therefore there's always a solution?
# run the path from node A -> EXIT, then revert, then run the next path from B -> EXIT, then revert...
# doesn't work, LR-> doesn't return to the same point, what if there's a wall on the left side?

# brute force
# start from all points, randomly pick a direction
# start[(0,0)...] all the possible starting points
# when do I backtrack? how do I know the algorithm will terminate?
# try all possible combinations (4*4*4... 4^n)

"""

directions = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def bruteforce(grid):
    starts = []  # this being a node, each edge going forward is UDLR
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "E":
                exit_x, exit_y = i, j
            elif grid[i][j] == ".":
                starts.append((i, j))
    # DFS vs BFS
    # pick BFS, shortest path, DFS...I am not sure it will finish
    path = []
    current_level = [(starts, path)]
    next_level = []
    while current_level:
        # process every node in the current level
        for node, path in current_level:
            for direction in ["U", "D", "L", "R"]:
                new_node = []
                for point in node:
                    # take one step towards the new direction
                    dx, dy = directions[direction]
                    new_x, new_y = point[0] + dx, point[1] + dy
                    if (
                        0 <= new_x < len(grid)
                        and 0 <= new_y < len(grid[0])
                        and grid[new_x][new_y] != "#"
                    ):
                        # valid move
                        next_point = (new_x, new_y)
                        if next_point != (
                            exit_x,
                            exit_y,
                        ):  # otherwise, we reached the exit
                            new_node.append(next_point)
                    else:
                        new_node.append(point)  # noop, append the same old point
                new_path = path + [direction]
                if not new_node:
                    return new_path
                next_level.append((new_node, new_path))
        # move to the next level
        current_level = next_level
        next_level = []
