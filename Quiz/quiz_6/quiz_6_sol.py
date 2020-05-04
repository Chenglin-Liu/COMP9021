# Prompts the user for a seed, a dimension dim, and an upper bound N.
# Randomly fills a grid of size dim x dim with numbers between 0 and N
# and computes:
# - the largest value n such that there is a path of the form (0, 1, 2,... n);
# - the number of such paths.
# A path is obtained by repeatedly moving in the grid one step north, south,
# west, or east.

# Written by Eric Martin for COMP9021


import sys
from random import seed, randint


def display_grid():
    for row in grid:
        print(' '.join(f'{e:{len(str(upper_bound))}}' for e in row)) 

def update(max_value, nb_of_paths_of_max_value, value, nb_of_paths):
    if value > max_value:
        return value, nb_of_paths
    if value == max_value:
        return value, nb_of_paths_of_max_value + nb_of_paths
    return max_value, nb_of_paths_of_max_value

def value_and_number_of_longest_paths():
    max_value = 0
    nb_of_paths_of_max_value = 0
    for i in range(dim):
        for j in range(dim):
            if grid[i][j]:
                continue
            max_value, nb_of_paths_of_max_value =\
                       update(max_value, nb_of_paths_of_max_value,
                              *_value_and_number_of_longest_paths(i, j)
                             )
    return max_value, nb_of_paths_of_max_value

def _value_and_number_of_longest_paths(i, j):
    nb_of_paths_of_max_value = 1
    max_value = grid[i][j]
    if i and grid[i - 1][j] == grid[i][j] + 1:
        max_value, nb_of_paths_of_max_value =\
                   update(max_value, nb_of_paths_of_max_value,
                          *_value_and_number_of_longest_paths(i - 1, j)
                         )
    if i < dim - 1 and grid[i + 1][j] == grid[i][j] + 1:
        max_value, nb_of_paths_of_max_value =\
                   update(max_value, nb_of_paths_of_max_value,
                          *_value_and_number_of_longest_paths(i + 1, j)
                         )
    if j and grid[i][j - 1] == grid[i][j] + 1:
        max_value, nb_of_paths_of_max_value =\
                   update(max_value, nb_of_paths_of_max_value,
                          *_value_and_number_of_longest_paths(i, j - 1)
                         )
    if j < dim - 1 and grid[i][j + 1] == grid[i][j] + 1:
        max_value, nb_of_paths_of_max_value =\
                   update(max_value, nb_of_paths_of_max_value,
                          *_value_and_number_of_longest_paths(i, j + 1)
                         )
    return max_value, nb_of_paths_of_max_value
        

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
          f'from 0 go up to {max_value}.'
         )
    if nb_of_paths_of_max_value == 1:
        print('There is one such path.')
    else:
        print('There are', nb_of_paths_of_max_value, 'such paths.')
