from math import sqrt
from itertools import permutations
from collections import Counter
import re

# A number is a good prime if it is prime and consists of nothing but
# distinct nonzero digits.
# Returns True or False depending on whether the integer provided as
# argument is or is not a good prime, respectively.
# Will be tested with for number a positive integer at most equal to
# 10_000_000.


def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, round(sqrt(number)) + 1):
        if number % i == 0:
            return False

    return True


def is_good_prime(number):
    number_string = str(number)
    if '0' in number_string:
        return False

    counter = list(Counter(number_string).values())
    for count in counter:
        if count > 1:
            return False

    if is_prime(number):
        return True
    else:
        return False


# ------------------- Test ------------------
is_good_prime(867)
is_good_prime(4027)
is_good_prime(12923)
is_good_prime(16879)
is_good_prime(26317)
# -------------------------------------------


# pattern is expected to be a nonempty string consisting of underscores
# and digits of length at most 7.
# Underscores have to be replaced by digits so that the resulting number
# is the smallest good prime, in case it exists.
# The function returns that number if it exists, None otherwise.
def smallest_good_prime(pattern):
    if '0' in pattern:
        return

    num_list = list(range(1, 10))
    exist_num = re.findall(r'(\d+)', pattern)
    if len(exist_num) == 1:
        for j in range(len(exist_num[0])):
            exist_num.append(exist_num[0][j])
        exist_num.pop(0)

    counter = list(Counter(exist_num).values())
    for count in counter:
        if count > 1:
            return

    if '_' not in pattern and is_prime(int(pattern)):
        return int(pattern)
    # Remove numbers that are already in pattern
    for num in exist_num:
        num_list.remove(int(num))

    num_of_underscore = pattern.count('_')
    # Generate possible combination of number
    possible_combination = list(permutations(num_list, num_of_underscore))
    for comb in possible_combination:
        possible_number = pattern
        for i in range(num_of_underscore):
            possible_number = possible_number.replace('_', str(comb[i]), 1)
        if is_prime(int(possible_number)):
            return possible_number


# --------------------- Test -----------------------
smallest_good_prime('_0_')
smallest_good_prime('2_2')
smallest_good_prime('123')
smallest_good_prime('_98')
smallest_good_prime('3167')
smallest_good_prime('__')
smallest_good_prime('___')
smallest_good_prime('1_7')
smallest_good_prime('_89')
smallest_good_prime('_89_')
smallest_good_prime('_2_4_')
smallest_good_prime('1__4_7')
# --------------------------------------------------
