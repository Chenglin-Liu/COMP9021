# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION
from random import seed, randrange
from collections import Counter


def give_values_to_letters(for_seed):
    seed(for_seed)
    return [randrange(1, 10) for _ in range(26)]


with open('/Users/chenglin/PycharmProjects/COMP9021/Week3/dictionary.txt', 'r')as file:
    dictionary = [line[: -1] for line in file]


def get_value_dict(values):
    # Dictionary that maps letters to values
    values_dict = {}
    letters_list = [chr(i) for i in range(65, 91)]
    for i in range(len(values)):
        values_dict[letters_list[i]] = values[i]

    return values_dict


# -----------------------
# word and letters are both meant to be strings of nothing but
# uppercase letters, values, a list returned by
# give_values_to_letters(). Returns:
# - -1 if word is not in dictionary.txt
# - 0 if word is in dictionary.txt but cannot be built from letters
# - the value of word according to values otherwise.

def can_be_built_from_with_value(word, letters, values):
    global dictionary

    if word not in dictionary:
        return -1

    # list of non-repetitive letter
    unique_letters = [*set(word)]
    for uni_word in unique_letters:
        word_freq = Counter(word).get(uni_word)
        letters_freq = 0 if Counter(letters).get(uni_word) is None else Counter(letters).get(uni_word)
        if word_freq > letters_freq:
            return 0

    values_dict = get_value_dict(values)
    return sum([values_dict[letter] for letter in word])


# ------------- test -------------
values = give_values_to_letters(0)
can_be_built_from_with_value('FIFHT', 'ABZUFTTHI', values)  # -1
can_be_built_from_with_value('FIFTH', 'ABZUFTTHI', values)  # 0

can_be_built_from_with_value('FIFTH', 'ABFZUFTTHI', values)  # 34
can_be_built_from_with_value('ZOOM', 'OABZYABZMOMYABZYO', values)  # 11


values = give_values_to_letters(1)
can_be_built_from_with_value('WRISTWATCHES', 'HTWSRWSITACE', values)  # 49


# --------------------------------
# letters is meant to be a string of nothing but uppercase letters.
# Returns the list of words in dictionary.txt that can be built
# from letters and whose value according to values is maximal.
# Longer words come before shorter words.
# For a given length, words are lexicographically ordered.

def most_valuable_solutions(letters, values):
    global dictionary

    # 1. Find out all word can be built from letters
    word_from_letters = []
    for word in dictionary:
        unique_letter = [*set(word)]
        counter = 0
        for uni_word in unique_letter:
            word_freq = Counter(word).get(uni_word)
            letters_freq = 0 if Counter(letters).get(uni_word) is None else Counter(letters).get(uni_word)
            if word_freq <= letters_freq:
                counter += 1
            else:
                break
        # Add word into list IF all word_freq <= letters_freq
        if counter == len(unique_letter):
            word_from_letters.append(word)

    # 2. Calculate word's value and sort
    value_dict = get_value_dict(values)
    word_to_value = {}
    for w in word_from_letters:
        value = sum([value_dict[letter] for letter in w])
        word_to_value.setdefault(value, []).append(w)

    if len(word_to_value) != 0:
        max_value = max(list(word_to_value.keys()))
        max_value_words = word_to_value[max_value]
        return sorted(max_value_words, key=lambda i: len(i), reverse=True)
    else:
        return []


# --------------------- test ------------------------
values = give_values_to_letters(0)
most_valuable_solutions('UUU', values)  # []
most_valuable_solutions('ABFZUFTTHI', values)  # ['FIFTH']
most_valuable_solutions('OABZYABZMOMYABZYO', values)  # ['BOMBAY']
most_valuable_solutions('ABCDEFGHIJKLMNOPQRSTUVWXYZ', values)  # ['AMBIDEXTROUSLY']
most_valuable_solutions('AAAEEEIIIOOOUUUBMNOPR', values)  # ['POMERANIA', 'IBERIAN']
most_valuable_solutions('THISORTHAT', values)  # ['THROATS', 'ARTIST', 'STRAIT', 'TRAITS']

values = give_values_to_letters(1)
most_valuable_solutions('HTWSRWSITACE', values)  # ['WRISTWATCHES']
most_valuable_solutions('THISORTHAT', values)  # ['THROATS', 'THIRST', 'THRASH']
most_valuable_solutions('LEURA', values)  # ['EARL', 'LEAR', 'REAL']
most_valuable_solutions('OBAMA', values)  # ['MAO']
most_valuable_solutions('QWERTYUIO', values)  # ['EQUITY', 'TORQUE']
