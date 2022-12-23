import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--sample', '-s', help='Run with sample data', action='store_true', default=False)

parsed_args = parser.parse_args()

if parsed_args.sample:
    print("Using sample data!")

def dprint(*args, **kwargs):
    if parsed_args.sample:
        print(*args, **kwargs)

with open('input.txt' if not parsed_args.sample else 'sample.txt') as f:
    input_data = list(map(lambda x: x.replace('\n', ''), f.readlines()))

dprint(input_data)


def load_board():
    board = set()
    for y, row in enumerate(input_data):
        for x, col in enumerate(row):
            if col == '#':
                board.add(complex(x, y))
    return board


offsets = {
    'north': 0-1j,
    'south': 0+1j,
    'east': 1+0j,
    'west': -1+0j
}

clear_spaces = {
    'south': [0+1j, 1+1j, -1+1j],
    'north': [0-1j, 1-1j, -1-1j],
    'east': [1+0j, 1+1j, 1-1j],
    'west': [-1+0j, -1+1j, -1-1j]
}

def determine_direction(position, order, board):
    for direction in order:
        dprint("Checking", direction)
        spaces = clear_spaces[direction]
        # results = [position + offset in board for offset in spaces]
        results = []
        for offset in spaces:
            new_pos = position + offset
            dprint("Looking at", new_pos)
            results.append(new_pos not in board)
        dprint(results)
        if all(results):
            return direction
    return None

def get_board_dimensions(board):
    x_points = [int(x.real) for x in board]
    y_points = [int(x.imag) for x in board]
    min_x, max_x = min(x_points), max(x_points)
    min_y, max_y = min(y_points), max(y_points)
    return (min_x, max_x), (min_y, max_y)

def print_board(board, print_func=dprint):
    (min_x, max_x), (min_y, max_y) = get_board_dimensions(board)

    print_func(min_x, "->", max_x)
    print_func(min_y, "->", max_y)

    for y in range(min_y, max_y+1):
        row = ""
        for x in range(min_x, max_x+1):
            row += "." if complex(x, y) not in board else "#"
        print_func(row)

def part_1():
    positions = load_board()
    init_positions = set(positions)
    dprint(positions)
    proposals = [
        lambda elf:(elf-1j,elf-1-1j,elf+1-1j), # N
        lambda elf:(elf+1j,elf-1+1j,elf+1+1j), # S
        lambda elf:(elf-1,elf-1-1j,elf-1+1j),  # W
        lambda elf:(elf+1,elf+1-1j,elf+1+1j)   # E
    ]

    for i in range(10):
        new_positions = defaultdict(list)
        for elf in positions:
            if not {elf+1, elf+1+1j, elf+1j, elf-1+1j, elf-1, elf-1-1j, elf-1j, elf+1-1j} & positions: # Elf stays put if nobody's nearby
                new_positions[elf].append(elf)
                continue
            for prop in proposals:
                if not set(prop(elf)) & positions: # Space is clear
                    new_positions[prop(elf)[0]].append(elf) # First index of prop is the direction to move
                    break
            else:
                new_positions[elf].append(elf)
        positions={(pro if len(elves)==1 else elf) for pro,elves in new_positions.items() for elf in elves}
        assert len(positions)==len(init_positions) # Ensure we didn't lose anyone
        print(f"End of round {i}", end="\r")
        print_board(positions)
        proposals.append(proposals.pop(0))
    print()
    (min_x, max_x), (min_y, max_y) = get_board_dimensions(positions)

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(positions) # 1 indexing again!!




def part_2():
    positions = load_board()
    init_positions = set(positions)
    dprint(positions)
    # Copy/paste cos part 1 mutates this list
    proposals = [
        lambda elf:(elf-1j,elf-1-1j,elf+1-1j), # N
        lambda elf:(elf+1j,elf-1+1j,elf+1+1j), # S
        lambda elf:(elf-1,elf-1-1j,elf-1+1j),  # W
        lambda elf:(elf+1,elf+1-1j,elf+1+1j)   # E
    ]

    rounds = 0
    while True:
        new_positions = defaultdict(list)
        for elf in positions:
            if not {elf+1, elf+1+1j, elf+1j, elf-1+1j, elf-1, elf-1-1j, elf-1j, elf+1-1j} & positions: # Elf stays put if nobody's nearby
                new_positions[elf].append(elf)
                continue
            for prop in proposals:
                if not set(prop(elf)) & positions: # Space is clear
                    new_positions[prop(elf)[0]].append(elf) # First index of prop is the direction to move
                    break
            else:
                new_positions[elf].append(elf)
        old = positions
        positions={(pro if len(elves)==1 else elf) for pro,elves in new_positions.items() for elf in elves}
        assert len(positions)==len(init_positions) # Ensure we didn't lose anyone
        num_moved = len(old - positions)
        rounds += 1
        print(f"End of round {rounds}, moved {num_moved}", end="\r")
        if num_moved == 0:
            break
        print_board(positions)
        proposals.append(proposals.pop(0))
    print()
    return rounds

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")