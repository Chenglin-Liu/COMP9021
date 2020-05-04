from random import randint
from random import seed  # delete
from collections import Counter
# When submit assignment, delete it


def dice_type_recogniser(dice):
    counter = {}
    for num in range(6):
        counter[num] = 0
    for d in dice:
        counter[d] += 1

    max_dice_num = max(counter.values())
    if max_dice_num == 2:
        # e.g. [1, 1, 2, 2, 5], len = 3
        if len(set(dice)) == 4:
            hands = 'One pair'
        else:
            hands = 'Two pair'
    elif max_dice_num == 3:
        # e.g. [1, 1, 1, 2, 3], len = 3
        if len(set(dice)) == 3:
            hands = 'Three of a kind'
        else:
            hands = 'Full house'
    elif max_dice_num == 4:
        hands = 'Four of a kind'
    elif max_dice_num == 5:
        hands = 'Five of a kind'
    else:
        if max(dice) - min(dice) == 4:
            hands = 'Straight'
        else:
            hands = 'Bust'

    return hands


def dealer(dice_num):
    dice = [randint(0, 5) for _ in range(dice_num)]
    return sorted(dice)


def print_dice(dice, poker):
    hands = dice_type_recogniser(sorted(dice))
    print('The roll is: ' + ' '.join(poker))
    print(f'It is a {hands}')


def play():
    # Map number to poker
    num_to_poker = {}
    for index, poker in enumerate(['Ace', 'King', 'Queen', 'Jack', '10', '9']):
        num_to_poker[index] = poker
    poker_to_num = {'Ace': 0, 'King': 1, 'Queen': 2, 'Jack': 3, '10': 4, '9': 5}

    roll = 1
    roll_dict = {2: 'second', 3: 'third'}
    # Generate poker code at the 1st roll
    dice = dealer(5)

    # Max roll is 3
    while roll <= 3:
        poker = [num_to_poker[d] for d in sorted(dice)]
        print_dice(dice, poker)

        roll += 1
        if roll == 4:
            break
        # Number of Dice to keep that are same with current hands

        condition = 1
        while condition:
            choice = input(f'Which dice do you want to keep for the {roll_dict[roll]} roll? ').split()
            same_dice_num = 0
            if not choice:
                dice = dealer(5)
                break

            if choice[0].lower() == 'all':
                print('Ok, done.')
                roll = 4  # To break the outside while loop
                break

            for chose_dice in set(choice):
                # Check if poker chose are in current hands and  are not more than pokers can be chose
                if Counter(choice)[chose_dice] <= Counter(poker)[chose_dice]:
                    same_dice_num += 1
                else:
                    print('That is not possible, try again!')
                    break

            if len(choice) == len(dice):
                print('Ok, done.')
                roll = 4
                break

            if same_dice_num == len(set(choice)):
                dice = [poker_to_num[x] for x in choice] + dealer(5 - len(choice))
                break



# -------------------- Test --------------------------
seed(0)
play()


# ----------------------------------------------------
def simulate(n):
    dice_type = ['Five of a kind', 'Four of a kind', 'Full house', 'Straight',
                 'Three of a kind', 'Two pair', 'One pair', 'Bust']
    statistics = {x: 0 for x in dice_type}

    for _ in range(n):
        dice = dealer(5)
        hands = dice_type_recogniser(dice)
        statistics[hands] += 1

    for item in dice_type[:-1]:
        print(f'{item:15}: {(statistics[item] / n)*100 :.2f}%')

