# Written by Eric Martin for COMP9021


from random import seed, shuffle
import sys


# for_seed is meant to be an integer, length a strictly positive integer.
# length will not be large for most tests, but can be as large as 10_000_000.
def generate_permutation(for_seed, length):
    seed(for_seed)
    values = list(range(1, length + 1))
    shuffle(values)
    return values

def maps_to(values, x):
    return values.index(x) + 1

def length_of_cycle_containing(values, x):
    length = 1
    y = values[x - 1]
    while y != x:
        length += 1
        y = values[y - 1]
    return length

# Returns a list of length len(values) + 1, with 0 at index 0
# and for all x in {1, ..., len(values)}, the length of the cycle
# containing x at index x.
def analyse(values):
    cycle_lengths = [0 for _ in range(len(values) + 1)]
    the_values = list(values)
    for i in range(len(values)):
        if not the_values[i]:
            continue
        seen_values = {i}
        j = i
        while the_values[j]:
            seen_values.add(j)
            k = j
            j = the_values[j] - 1
            the_values[k] = None
        length = len(seen_values)
        for e in seen_values:
            cycle_lengths[e + 1] = length
    return cycle_lengths
