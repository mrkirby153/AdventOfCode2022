import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from collections import defaultdict
from copy import copy

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

input_data = input_data[0]

rocks = [
    [
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 1, 0, 0], 
        [1, 1, 1, 0], 
        [0, 1, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 1, 0], 
        [0, 0, 1, 0], 
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ],
    [
        [1, 0, 0, 0], 
        [1, 0, 0, 0], 
        [1, 0, 0, 0], 
        [1, 0, 0, 0]
    ],
    [
        [1, 1, 0, 0], 
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
]

# The row of the origin of the piece (starting from the top bottom)
rock_lowest = [
    0, 2, 2, 3, 1
]

rock_heights = [
    1, 3, 3, 4, 2
]

dprint(input_data)

def piece_size(rock):
    return max([len(x) for x in rock])

def print_tube(tube):
    for row in tube:
        for col in row:
            dprint('.' if col == 0 else 'X', end="")
        dprint()

def move_rock(grid, rock_id, current_x, current_y, delta_x, delta_y):
    new_x, new_y = current_x + delta_x, current_y + delta_y
    for i in range(4):
        for j in range(4):
            if rocks[rock_id][i][j] == 0: continue # Empty space in the rock grid, don't care
            rock_x = new_x + j
            rock_y = new_y + i
            if rock_x < 0 or rock_x > 6: # Out of range, can't move that way
                return None
            if rock_y > 0:
                return None # Off the bottom of the grid
            if grid[rock_x, rock_y] != 0:
                return None
    return (new_x, new_y)

def print_grid(grid, rows):
    for y in range(-rows, 1, 1):
        #dprint(y if y != 0 else f" {y}", end=" ")
        dprint("|", end="")
        for x in range(7):
            dprint('.' if grid[x, y] == 0 else '#', end="")
        dprint("|")
    dprint(f"+{'-'*7}+")

def move_rock_into_grid(grid, rock_id, rock_x, rock_y):
    for i in range(4):
        for j in range(4):
            if rocks[rock_id][i][j] == 0: continue
            lookup_x = rock_x + j
            lookup_y = rock_y + i
            assert grid[lookup_x, lookup_y] == 0
            grid[lookup_x, lookup_y] = 1

def print_grid_with_rock_at(grid, rock_id, rock_x, rock_y, rows):
    new_grid = copy(grid)
    move_rock_into_grid(new_grid, rock_id, rock_x, rock_y)
    print_grid(new_grid, rows)

def get_highest_row(grid):
    for y_coordinate in range(1_000_000_000):
        y_coordinate = -y_coordinate
        filled_row = False
        for x_coordinate in range(7):
            if grid[x_coordinate, y_coordinate] == 1:
                filled_row = True
                break
        if not filled_row:
            return (-y_coordinate) - 1

def part_1():
    grid = defaultdict(int)


    # Floor is at 0
    # Negative numbers go up the tube
    highest_y = 0
    rock_id = 0
    stream_index = 0

    GRID_TO_PRINT_SIZE = 50 # 21

    for i in range(2022):
        rock_x = 2
        rock_y = highest_y - 3 - rock_lowest[rock_id]
        dprint(f"Spawned Rock {i+1} at ", (rock_x, rock_y), rocks[rock_id])
        print_grid_with_rock_at(grid, rock_id, rock_x, rock_y, GRID_TO_PRINT_SIZE)
        dprint("----")
        while True:
            direction = -1 if input_data[stream_index] == '<' else 1
            dprint(f"Moving", 'left' if direction == -1 else 'right')
            lateral_movement = move_rock(grid, rock_id, rock_x, rock_y, direction, 0)
            if lateral_movement is not None:
                rock_x, rock_y = lateral_movement
            else:
                dprint("no movement")
            print_grid_with_rock_at(grid, rock_id, rock_x, rock_y, GRID_TO_PRINT_SIZE)

            down_movement = move_rock(grid, rock_id, rock_x, rock_y, 0, 1)
            stream_index = (stream_index + 1) % len(input_data)
            if down_movement is None:
                dprint("Hit the bottom")
                break
            else:
                rock_x, rock_y = down_movement
                #dprint("new coordinates", rock_x, rock_y)
                dprint("Moving down")
                print_grid_with_rock_at(grid, rock_id, rock_x, rock_y, GRID_TO_PRINT_SIZE)

        dprint("Done")
        move_rock_into_grid(grid, rock_id, rock_x, rock_y)
        print_grid(grid, GRID_TO_PRINT_SIZE)
        highest_y = -get_highest_row(grid) - 1
        dprint("Highest y: ", highest_y)

        rock_id = (rock_id + 1) % len(rocks)

    print(f"Done!")
    return -highest_y

def part_2():
    pass

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")