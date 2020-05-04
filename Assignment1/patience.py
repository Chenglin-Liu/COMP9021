from random import seed, shuffle
from copy import deepcopy


def generate_dial_and_centre(for_seed):
    colours = 'CDHS' # Clubs, Diamonds, Hearts, Spades
    #                                            jacks, queens, kings
    ranks = list(str(x) for x in range(1, 11)) + list('jqk')
    seed(for_seed)
    cards = [colour + rank for colour in colours for rank in ranks]
    shuffle(cards)
    dial = dict.fromkeys(range(1, 13))
    for i in range(12):
        dial[i + 1] = [cards[i + 13 * j] for j in range(4)]
    return dial, [cards[12 + 13 * j] for j in range(4)]


def print_pokers(hour, hidden_card_num, dial):
    hidden_card_number = hidden_card_num[hour]
    facing_card_number = len(dial[hour]) - hidden_card_number
    card_code = []
    for i in range(len(dial[hour])):
        color = dial[hour][i][0]
        rank = dial[hour][i][1:]
        # Map card to unicode(Source: http://www.unicode.org/charts/PDF/U1F0A0.pdf)
        rank_dict = {'10': 'A', 'j': 'B', 'q': 'D', 'k': 'E'}
        color_dict = {'C': '1F0D', 'D': '1F0C', 'H': '1F0B', 'S': '1F0A'}
        card_color = color_dict[color]
        if rank in rank_dict.keys():
            rank = rank_dict[rank]
        # Make up Hexadecimal code and transfer to decimal
        card_code.append(int(f'{card_color}{rank}', 16))

    if facing_card_number != 0:
        string = str(chr(card_code[0]))
        for fc in card_code[1: facing_card_number]:
            string += '  ' + str(chr(fc))
        for hc in card_code[facing_card_number: len(dial[hour])]:
            string += '  hidden' + str(chr(hc))

    else:
        string = 'hidden' + str(chr(card_code[0]))
        for hc in card_code[1:]:
            string += '  hidden' + str(chr(hc))
    print(string)


def initial_hour(hour, dial):
    hidden_card_num = {x: 4 for x in range(13)}
    print_pokers(hour, hidden_card_num, dial)


# ------------------ Test -------------------------
dial, centre = generate_dial_and_centre(0)
for hour in dial:
    print(f'{hour:2}', dial[hour], sep=': ')
print(centre)

initial_hour(12, dial)
initial_hour(10, dial)
initial_hour(3, dial)
initial_hour(2, dial)
initial_hour(9, dial)
initial_hour(4, dial)
initial_hour(5, dial)
initial_hour(7, dial)
initial_hour(6, dial)
initial_hour(8, dial)
# ---------------------------------------------------


# Simulate take off the card
def take_off(hour, hidden_card_num, local_centre, local_dial):
    hidden_card_num[hour] -= 1
    if hour == 13:
        card = local_centre[-1]
        local_centre.pop()
    else:
        card = local_dial[hour][-1]
        local_dial[hour].pop()
    return card, local_dial, local_centre


# Simulate place in the card
def place_in(card, rank_dict, local_dial, local_centre):
    card_rank = card[1:]
    if card_rank in rank_dict.keys():
        next_hour = rank_dict[card_rank]
    else:
        next_hour = int(card_rank)

    if next_hour == 13:
        local_centre.insert(0, card)
    else:
        local_dial[next_hour].insert(0, card)
    return next_hour, local_dial, local_centre


def hour_after_playing_from_beginning_for_at_most(hour, nb_of_steps, dial, centre):
    rank_dict = {'j': 11, 'q': 12, 'k': 13}
    hidden_card_num = {x: 4 for x in range(1, 14)}
    if nb_of_steps >= 1:
        next_hour = 13
    local_hour = deepcopy(hour)
    local_centre = deepcopy(centre)
    local_dial = deepcopy(dial)
    for _ in range(nb_of_steps):
        card, local_dial, local_centre = take_off(next_hour, hidden_card_num, local_centre, local_dial)
        # When take off the facing card stop the function
        for num in list(hidden_card_num.values()):
            if num < 0 and nb_of_steps < 52 and local_hour != 13:
                print('Could not play that far...')
                return
            # This is for question 3
            if num < 0 and local_hour == 13:
                print('No success...')
                return
        next_hour, local_dial, local_centre = place_in(card, rank_dict, local_dial, local_centre)

    # Following code is for question 3, except the last code
    if local_hour == 13:
        card_code = []
        for i in range(len(local_centre)):
            color = local_centre[i][0]
            rank = local_centre[i][1:]
            rank_dict = {'10': 'A', 'j': 'B', 'q': 'D', 'k': 'E'}
            color_dict = {'C': '1F0D', 'D': '1F0C', 'H': '1F0B', 'S': '1F0A'}
            card_color = color_dict[color]
            if rank in rank_dict.keys():
                rank = rank_dict[rank]
            card_code.append(int(f'{card_color}{rank}', 16))

        print("  ".join(chr(x) for x in card_code))
        return

    print_pokers(hour, hidden_card_num, local_dial)


# --------------------- Test -------------------------
dial, centre = generate_dial_and_centre(0)
# Tested
hour_after_playing_from_beginning_for_at_most(12, 1, dial, centre)
hour_after_playing_from_beginning_for_at_most(12, 2, dial, centre)

hour_after_playing_from_beginning_for_at_most(10, 2, dial, centre)
hour_after_playing_from_beginning_for_at_most(10, 3, dial, centre)

hour_after_playing_from_beginning_for_at_most(3, 3, dial, centre)
hour_after_playing_from_beginning_for_at_most(3, 4, dial, centre)

hour_after_playing_from_beginning_for_at_most(10, 4, dial, centre)
hour_after_playing_from_beginning_for_at_most(10, 5, dial, centre)

hour_after_playing_from_beginning_for_at_most(2, 5, dial, centre)
hour_after_playing_from_beginning_for_at_most(2, 6, dial, centre)

hour_after_playing_from_beginning_for_at_most(12, 6, dial, centre)
hour_after_playing_from_beginning_for_at_most(9, 7, dial, centre)

hour_after_playing_from_beginning_for_at_most(4, 8, dial, centre)
hour_after_playing_from_beginning_for_at_most(5, 9, dial, centre)
hour_after_playing_from_beginning_for_at_most(7, 10, dial, centre)
hour_after_playing_from_beginning_for_at_most(6, 11, dial, centre)
hour_after_playing_from_beginning_for_at_most(8, 13, dial, centre)
hour_after_playing_from_beginning_for_at_most(10, 45, dial, centre)

hour_after_playing_from_beginning_for_at_most(10, 46, dial, centre)

dial, centre = generate_dial_and_centre(18)
hour_after_playing_from_beginning_for_at_most(1, 52, dial, centre)
hour_after_playing_from_beginning_for_at_most(10, 53, dial, centre)
# ----------------------------------------------------


def kings_at_end_of_game(dial, centre):
    hour_after_playing_from_beginning_for_at_most(13, 52, dial, centre)


# ------------- Test ---------------
dial, centre = generate_dial_and_centre(0)
kings_at_end_of_game(dial, centre)

dial, centre = generate_dial_and_centre(18)
kings_at_end_of_game(dial, centre)


