# Written by Eric Martin for COMP9021


from random import seed, randrange
from collections import Counter


def give_values_to_letters(for_seed):
    seed(for_seed)
    return [randrange(1, 10) for _ in range(26)]

def capture_words():
    words = {}
    with open('dictionary.txt') as dictionary:
        for word in dictionary:
            word = word[: -1]
            words[word] = Counter(word)
    return words

# word and letters are both meant to be strings of nothing but
# uppercase letters, values, a list returned by
# give_values_to_letters(). Returns:
# - -1 if word is not in dictionary.txt
# - 0 if word is in dictionary.txt but cannot be built from letters
# - the value of word according to values otherwise.
def can_be_built_from_with_value(word, letters, values):
    try:
        word_letters = capture_words()[word]
    except KeyError:
        return -1
    values = {chr(ord('A') + i): values[i] for i in range(26)}
    available_letters = Counter(letters)
    try:
        if all(word_letters[c] <= available_letters[c] for c in word_letters):
            return sum(values[c] for c in word)
        else:
            raise KeyError
    except KeyError:
        return 0

# letters is meant to be a string of nothing but uppercase letters.
# Returns the list of words in dictionary.txt that can be built
# from letters and whose value according to values is maximal.
# Longer words come before shorter words.
# For a given length, words are lexicographically ordered.
def most_valuable_solutions(letters, values):
    words = capture_words()
    values = {chr(ord('A') + i): values[i] for i in range(26)}
    available_letters = Counter(letters)
    solutions = []
    best_value = 0
    for word in words:
        word_letters = words[word]
        try:
            if all(word_letters[c] <=\
                          available_letters[c] for c in word_letters
                  ):
                value = sum(values[c] for c in word)
                if value > best_value:
                    best_value = value
                    solutions = [word]
                elif value == best_value:
                    solutions.append(word)
        except KeyError:
            continue
    solutions.sort(key=lambda x: -len(x))
    return solutions
