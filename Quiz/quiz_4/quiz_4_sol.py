# Written by Eric Martin for COMP9021


from math import sqrt
from itertools import permutations


# A number is a good prime if it is prime and consists of nothing but
# distinct nonzero digits.
# Returns True or False depending on whether the integer provided as
# argument is or is not a good prime, respectively.
# Will be tested with for number a positive integer at most equal to
# 10_000_000.
def is_good_prime(number):
    number_str = str(number)
    if len(set(number_str)) != len(number_str) or '0' in number_str:
        return False
    return sieve_of_primes_up_to(number)[number]

# pattern is expected to be a nonempty string consisting of underscores
# and digits of length at most 7.
# Underscores have to be replaced by digits so that the resulting number
# is the smallest good prime, in case it exists.
# The function returns that number if it exists, None otherwise.
def smallest_good_prime(pattern):
    available_digits = set(chr(ord('0') + d) for d in range(1, 10))
    free_slots = []
    schema = []
    for i in range(len(pattern)):
        c = pattern[i]
        schema.append(c)
        if c.isdigit():
            if c in available_digits:
                available_digits.remove(c)
            else:
                return
        elif c == '_':
            free_slots.append(i)
        else:
            return
    available_digits = sorted(available_digits)
    sieve = sieve_of_primes_up_to(10 ** len(pattern))
    for digits in permutations(available_digits, len(free_slots)):
        for i in range(len(free_slots)):
            schema[free_slots[i]] = digits[i]
        candidate = int(''.join(schema))
        if sieve[candidate]:
            return candidate

def sieve_of_primes_up_to(n):
    sieve = [False, False] + [True] * (n - 1)
    for p in range(2, round(sqrt(n)) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return sieve
