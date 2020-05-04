# Written by Eric Martin for COMP9021
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
print('Here are the generated values:', values)
print('\nThe difference between last and first values is:')
print('  ', values[-1] - values[0])
print()
the_max = max(values)
print('Here are the values represented as horizontal bars:')
print()
for e in values:
    print('   ', ' * ' * e)
print()
print('Here are the values represented as vertical bars, '
      'with a surrounding frame:'
     )
print()
print('   ', '---' * length, '--', sep='')
for i in range(the_max, 0, -1):
    print('   |', end='')
    for e in values:
        print(' * ', end='') if e >= i else print('   ', end='')
    print('|')
print('   ', '---' * length, '--', sep='')
print()
