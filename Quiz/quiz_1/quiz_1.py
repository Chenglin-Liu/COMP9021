# Written by *** and Eric Martin for COMP9021
#
# Generates a random list of integers between 1 and 6
# whose length is chosen by the user, displays the list,
# outputs the difference between last and first values,
# then displays the values as horizontal bars of stars,
# then displays the values as vertical bars of stars
# surrounded by a frame.


from random import seed, randrange
import sys


try:
    for_seed, length = (int(x) for x in input('Enter two integers, the second '
                                              'one being strictly positive: '
                                             ).split()
                       )
    if length <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
values = [randrange(1, 7) for _ in range(length)]
print('Here are the generated values:', values, end='\n\n')
print('The difference between last and first values is:')
# INSERT CODE HERE
difference = values[-1] - values[0]
print('   ' + str(difference) + '\n')
print('Here are the values represented as horizontal bars:\n')
# INSERT CODE HERE
for i in range(0, len(values)):
      print('    ' + ' * ' * values[i])

print('\nHere are the values represented as vertical bars, '
      'with a surrounding frame:\n'
     )
# INSERT CODE HERE
import numpy as np


def print_horizontal_line(list_length):
    # Print horizontal bars
    print('   ' + '-' * (3 * list_length + 2))


# method 1
def reverse_pattern(values):
    """
    Reverse the pattern
    :param values: a list
    :return: a list of reversed pattern
    """

    # Create a matrix of the input list
    max_value = max(values)
    values_matrix = []
    for i_0 in range(0, len(values)):
        row = [1] * values[i_0] + [0] * (max_value - values[i_0])
        values_matrix.append(row)
    matrix = np.mat(values_matrix)  # Transform list into matrix

    num_row = matrix.shape[0]  # Number of rows
    num_col = matrix.shape[1]  # Number of columns

    # Reverse the matrix
    reversed_mat = np.zeros(shape=(num_col, num_row))  # Create a zeros matrix to store reserved matrix
    for j in range(0, num_row):
        for i in range(0, num_col):
            reversed_mat[i, j] = matrix[j, (num_col - 1 - i)]  # Assign values according to the reversing rule

    reversed_list = reversed_mat.tolist()  # Transform matrix into list
    return reversed_list


def print_pattern(pattern_list):
    # Print the pattern with a frame

    num_row = len(pattern_list)  # number of rows
    num_col = len(pattern_list[0])  # number of columns

    print_horizontal_line(num_col)  # Upper horizontal bars
    # --------------------- Body -------------------------
    for output_i in range(0, num_row):
        print('   ' + '|', end='')  # Set the bar at begging of one line
        for output_j in range(0, num_col):
            # Print '*' or ' ' according following rules:
            # 1 -> ' * '
            # 0 -> '   '
            if pattern_list[output_i][output_j] == 1.:
                print(' * ', end='')
            else:
                print('   ', end='')
        print('|')  # Set the bar at the end of one line
    # -------------------- End of Body ----------------------
    print_horizontal_line(num_col)  # Bottom horizontal bars
    print()  # Output a blank line


def main():
    reversed_list = reverse_pattern(values)
    print_pattern(reversed_list)


# Draw the frame
if __name__ == '__main__':
    main()



