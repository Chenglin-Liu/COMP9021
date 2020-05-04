# Written by Eric Martin for COMP9021


# In both functions below, grid is supposed to be a sequence of strings
# all of the same length, consisting of nothing but spaces and *s,
# and represent one or more "full polygons" that do not "touch" each other.

def display(*grid):
    for e in grid:
        print(' '.join(e))

def display_leftmost_topmost_boundary(*grid):
    # N, NE, E, SE, S, SW, W, NW
    moves = (-1, 0), (-1, 1,), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1),\
            (-1, -1)
    orientations = 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE', 'E'
    directions = dict(zip(moves, orientations[5 :] + orientations[: 5]))
    explorations = dict(zip(orientations,
                            (moves[i :] + moves[: i] for i in range(8))
                           )
                       )

    height = len(grid)
    width = len(grid[0])
    y, x = leftmost_topmost_star(*grid)
    starting_point = y, x
    boundary = {starting_point}
    current_point = starting_point
    # We start exploring East
    current_direction = 'SW'
    while True:
        for (j1, i1) in explorations[current_direction]:
            y1 = y + j1
            x1 = x + i1
            if -1 < y1 < height and -1 < x1 < width and grid[y1][x1] == '*':
                break
        if (y1, x1) == starting_point:
            break
        boundary.add((y1, x1))
        current_direction = directions[j1, i1]
        y = y1
        x = x1
    for y in range(height):
        print(' '.join(('*' if (y, x) in boundary else ' ')
                           for x in range(width)
                      )
             )

def leftmost_topmost_star(*grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '*':
                return y, x
