# Written by *** and Eric Martin for COMP9021
from random import seed, shuffle
import sys
import pysnooper
import time
from functools import wraps


def timefn(fn):
    """计算性能的修饰器"""
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {fn.__name__} took {t2 - t1: .5f} s")
        return result
    return measure_time


# for_seed is meant to be an integer, length a strictly positive integer.
# length will not be large for most tests, but can be as large as 10_000_000.
def generate_permutation(for_seed, length):
    seed(for_seed)
    values = list(range(1, length + 1))
    shuffle(values)
    return values

# Question 1
def maps_to(values, x):
    id = values.index(x) + 1
    return id


# ———————————————————— Question 1 Test ——————————————————————————
values = generate_permutation(1, 10)
maps_to(values, 8)
maps_to(values, 7)
# ———————————————————— Question 1 Test ——————————————————————————


@pysnooper.snoop()
def test(values, x):
    counter = 1  # Counter of length of cycle
    pointer = values[x-1]  # Pointer: point to next value
    if pointer == x:
        pass  # There is no cycle
    else:
        for _ in range(len(values)):
            if values[pointer-1] != x:
                counter += 1
                pointer = values[pointer-1]
            else:
                counter += 1
                break
    return counter

# test1
values = generate_permutation(0, 10)
test(values, 1)
test(values, 3)
test(values, 6)
# test2
values = generate_permutation(1, 15)
test(values, 1)
test(values, 2)
# test3
t1 = time.time()
values = generate_permutation(2, 1000)
test(values, 500)
t2 = time.time()
print(f'Costs {t2-t1}s')
# Question 2

@pysnooper.snoop()
def length_of_cycle_containing(values, x):
    counter = 1  # Counter of length of cycle
    pointer = values[x-1]  # Pointer: point to next value
    if pointer == x:
        pass  # There is no cycle
    else:
        for _ in range(len(values)):
            if values[pointer-1] != x:
                counter += 1
                pointer = values[pointer-1]
            else:
                counter += 1
                break
    return counter

# Returns a list of length len(values) + 1, with 0 at index 0
# and for all x in {1, ..., len(values)}, the length of the cycle
# containing x at index x.
def analyse(values):
    cycle_dict = {}  # Dictionary storing calculated cycle
    for x in range(len(values)):
        if str(x+1) not in cycle_dict.keys():
            list_of_pointer = []
            counter = 1  # Counter of length of cycle
            pointer = values[x]  # Pointer: point to next value
            list_of_pointer.append(x + 1)
            if pointer == x+1:
                pass  # There is no cycle
            else:
                for _ in range(len(values)):
                    if values[pointer-1] != x+1:  # Determine if current value = 1st value
                        list_of_pointer.append(pointer)
                        counter += 1
                        pointer = values[pointer-1]
                    else:
                        list_of_pointer.append(pointer)
                        counter += 1
                        break

            # Store calculated cycle into dictionary to reduce times of calculation
            for val in list_of_pointer:
                cycle_dict[str(val)] = counter
        # If this cycle has been calculated, skip it
        else:
            continue

    # Generate cycle list
    cycle_list = [0]
    for index in range(1, len(values)+1):
        cycle_list.append(cycle_dict[str(index)])

    return cycle_list



# ----------------- method 1-----------------
# dict = {f'{x}' : 1 for x in range(5)}
# dict.keys()
# dict[str(1)]

@timefn
def analyse_test(values):
    cycle_dict = {}
    for x in range(len(values)):
        if str(x+1) not in cycle_dict.keys():
            list_of_pointer = []
            counter = 1  # Counter of length of cycle
            pointer = values[x]
            list_of_pointer.append(x + 1)
            if pointer == x+1:
                pass  # There is no cycle
            else:
                for _ in range(len(values)):
                    if values[pointer-1] != x+1:  # Determine if current value = 1st value
                        list_of_pointer.append(pointer)
                        counter += 1
                        pointer = values[pointer-1]
                    else:
                        list_of_pointer.append(pointer)
                        counter += 1
                        break

            # Store calculated cycle into dictionary to reduce times of calculation
            for val in list_of_pointer:
                cycle_dict[str(val)] = counter
        else:
            continue

    # Generate cycle list
    cycle_list = [0]
    for index in range(1, len(values)+1):
        cycle_list.append(cycle_dict[str(index)])

    return cycle_list


# test 1
values = generate_permutation(0, 10)
analyse_test(values)
# test 2
values = generate_permutation(1, 15)
values
c = analyse_test(values)
c
# test 3
values = generate_permutation(2, 1000)
cycle_lengths = analyse_test(values)
len(cycle_lengths)
cycle_lengths[500]

# Large number test

# Tradition method
@timefn
def tradition(values):
    c_list = [0]
    for i in range(len(values)):
        c_list.append(test(values, i+1))
    return c_list

# Large number tese
values = generate_permutation(2, 1_000_00)
cycle_lengths = analyse_test(values)
cycle_lengths_t = tradition(values)


