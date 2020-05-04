# Prompts the user for a seed, a dimension dim, and an upper bound N.
# Randomly fills a grid of size dim x dim with numbers between 0 and N
# and computes:
# - the largest value n such that there is a path of the form (0, 1, 2,... n);
# - the number of such paths.
# A path is obtained by repeatedly moving in the grid one step north, south,
# west, or east.
import sys
from random import seed, randint
from collections import Counter


def display_grid():
    for row in grid:
        print(' '.join(f'{e:{len(str(upper_bound))}}' for e in row))


# Define direction (up, left, right, down)
directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]


def get_longest_path(y, x, n):
    if grid[y][x] == n:
        path = []
        for direction in directions:
            next_y = y + direction[0]
            next_x = x + direction[1]
            if 0 <= next_y < dim and 0 <= next_x < dim:
                # path.append(get_longest_path(next_y, next_x, n + 1)[0])
                p, c = get_longest_path(next_y, next_x, n + 1)
                path.extend(p for _ in range(c))

        longest_path = max(path)
        count = dict(Counter(path))[longest_path]
        # count = 4 means it reach the end point OR at the start point (e.g. 0 surrounded by 1)
        # otherwise count can be at most 3
        if (len(set(path)) == 1 and n != 0) or (longest_path == 0):
            count = 1
        return [longest_path, count]
    else:  # Base case: next number != n + 1
        return [n - 1, 1]


def value_and_number_of_longest_paths():
    # Create a list to store path and count
    path_map = [[0 for _ in range(dim)] for _ in range(dim)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            path_map[y][x] = get_longest_path(y, x, 0)

    path_dict = dict()
    for i in range(len(path_map)):
        for j in range(len(path_map[i])):
            if path_map[i][j][0] not in path_dict.keys():
                path_dict[path_map[i][j][0]] = path_map[i][j][1]
            else:
                path_dict[path_map[i][j][0]] += path_map[i][j][1]

    max_value = max(path_dict.keys())
    number_of_path = path_dict[max_value]

    return max_value, number_of_path


provided_input = input('Enter three integers: ').split()
if len(provided_input) != 3:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    for_seed, dim, upper_bound = (abs(int(e)) for e in provided_input)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [[randint(0, upper_bound) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()

max_value, nb_of_paths_of_max_value = value_and_number_of_longest_paths()
if not nb_of_paths_of_max_value:
    print('There is no 0 in the grid.')
else:
    print('The longest paths made up of consecutive numbers starting '
          f'from 0 go up to {max_value}.')
    if nb_of_paths_of_max_value == 1:
        print('There is one such path.')
    else:
        print('There are', nb_of_paths_of_max_value, 'such paths.')
