with open('input.txt') as f:
    input_data = list(map(lambda x: x.replace('\n', ''), f.readlines()))

input_data = [(x[0], x[2]) for x in input_data]

ROCK = 1
PAPER = 2
SCISORS = 3

mapping = {
    'A': ROCK, # Rock
    'B': PAPER, # Paper
    'C': SCISORS, # Scisors
    'X': ROCK, # Rock
    'Y': PAPER, # Paper
    'Z': SCISORS # Scisors
}

win_mapping = {
    ROCK: PAPER,
    PAPER: SCISORS,
    SCISORS: ROCK
}
lose_mapping = {v: k for k, v in win_mapping.items()}


def calculate_score(us, them):
    us = mapping[us] if type(us) is str else us
    them = mapping[them] if type(them) is str else them

    if us == ROCK and them == SCISORS:
        return us + 6
    elif us == SCISORS and them == PAPER:
        return us + 6
    elif us == PAPER and them == ROCK:
        return us + 6
    elif us == them:
        return us + 3 # Draw
    else:
        return us # Lose

def get_play(us, them):
    them = mapping[them]
    if us == 'X':
        return lose_mapping[them]
    elif us == 'Y':
        return them
    elif us == 'Z':
        return win_mapping[them]

def part_1():
    total_score = 0
    for them, us in input_data:
        total_score += calculate_score(us, them)
    return total_score

def part_2():
    total_score = 0
    for them, us in input_data:
        total_score += calculate_score(get_play(us, them), them)
    return total_score

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")
