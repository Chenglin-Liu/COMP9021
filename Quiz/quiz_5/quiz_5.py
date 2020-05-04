# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# In both functions below, grid is supposed to be a sequence of strings
# all of the same length, consisting of nothing but spaces and *s,
# and represent one or more "full polygons" that do not "touch" each other.

def display(*grid):
    for line in grid:
        print(' '.join(line))


def get_padded_pattern(grid):
    """Pad the pattern with whitespace"""

    padding_grid = list(grid)
    length = len(padding_grid[0])
    # Add empty lines at the start and end of the pattern
    padding_grid.insert(0, ' '*length)
    padding_grid.append(' ' * length)
    # Add spaces at the start and end of the lines
    for i in range(len(padding_grid)):
        padding_grid[i] = ' ' + padding_grid[i] + ' '
    return padding_grid


def is_boundary(y, x, grid):
    # If current position's left / right / up / down are both not '*'
    # This position is boundary
    number_of_star = 0
    left = grid[y][x - 1]
    right = grid[y][x + 1]
    up = grid[y - 1][x]
    down = grid[y + 1][x]
    for i in [left, right, up, down]:
        if i != ' ':
            number_of_star += 1

    string_list = list(grid[y])
    if number_of_star < 4:
        string_list[x] = '1'
    else:
        string_list[x] = '0'
    grid[y] = ''.join(string_list)


def find_all_boundaries(y, x, grid):
    """
    Recursively scan if surrounding 8 positions is boundary
    Pass first boundary(y, x, grid)
    """
    if grid[y][x] == '*':
        is_boundary(y, x, grid)
        # position = current coordinate + below coordinate
        upleft = (-1, -1)
        up = (-1, 0)
        upright = (-1, 1)
        left = (0, -1)
        right = (0, 1)
        downleft = (1, -1)
        down = (1, 0)
        downright = (1, 1)
        surrounding = [upleft, up, upright, left, right, downleft, down, downright]

        # Scan surrounding position
        for position in surrounding:
            find_all_boundaries(y + position[0], x + position[1], grid)


def display_leftmost_topmost_boundary(*grid):
    padded_grid = get_padded_pattern(grid)

    # Search the coordinate of 1st boundary
    search_result = 0
    for y in range(1, len(padded_grid) - 1):
        for x in range(1, len(padded_grid[y]) - 1):
            if padded_grid[y][x] == '*':
                search_result = 1
                break
        if search_result == 1:
            break

    find_all_boundaries(y, x, padded_grid)
    result = []
    for i in range(1, len(padded_grid) - 1):
        padded_grid[i] = padded_grid[i].replace('*', '0')
        padded_grid[i] = padded_grid[i].replace('0', ' ')
        padded_grid[i] = padded_grid[i].replace('1', '*')
        result.append(padded_grid[i][1: -1])

    display(*tuple(result))


# —————————————— Test ————————————————————
grid_1 = ('  *    ',
          ' ****  ',
          '*****  ',
          '****** ',
          ' ****  ',
          ' **    '
          )

display(*grid_1)
display_leftmost_topmost_boundary(*grid_1)

grid_2 = (' *        ',
          '***   **  ',
          ' *** ***  ',
          ' ***  *   ',
          '****      ',
          ' **       '
          )
display(*grid_2)
display_leftmost_topmost_boundary(*grid_2)


grid_3 = ('      ',
          '  *  *',
          ' ** **',
          ' **** ',
          ' *****',
          '   *  ',
          '**    ',
          '**    ',
          '      ',
          )
display(*grid_3)
display_leftmost_topmost_boundary(*grid_3)
