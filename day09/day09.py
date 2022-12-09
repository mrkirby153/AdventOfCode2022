import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

import math

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


input_data = [(x[0], x[1]) for x in map(lambda x: x.split(" "), input_data)]

dprint(input_data)

# Right/Left = Positive/Negative X
# Up/Down = Positive/Negative Y



def move_head(starting_position, direction, amount):
    x, y = starting_position
    if direction == "R":
        x += amount
    elif direction == "L":
        x -= amount
    elif direction == "U":
        y += amount
    elif direction == "D":
        y -= amount
    return (x, y)

def should_move_tail(head_position, tail_position):
    hx, hy = head_position
    tx, ty = tail_position

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            # dprint(f"{tx+dx}, {hy+dy}")
            if tx+dx == hx and ty+dy == hy:
                return False
    return True

def move_tail(tail_position, head_position):

    if not should_move_tail(head_position, tail_position):
        return tail_position

    hx, hy = head_position
    tx, ty = tail_position

    if hy == ty:
        # The tail needs to move horizontally
        tail_direction = hx - tx
        return (tx+tail_direction+ (1 if tail_direction < 0 else -1), ty)
    elif hx == tx:
        # The tail needs to move vertically
        tail_direction = hy - ty
        return (tx, ty+tail_direction + (1 if tail_direction < 0 else -1))
    else:
        # The tail needs to move diagonally
        if hy > ty and hx > tx:
            # The tail must move up and to the right
            return (tx + 1, ty + 1)
        elif hy < ty and hx < tx:
            # The tail must move down and to the left
            return (tx - 1, ty - 1)
        elif hy > ty and hx < tx:
            # The tail must move up and to the left
            return(tx-1, ty+1)
        elif hy < ty and hx > tx:
            # The tail must move down and to the right
            return (tx+1, ty-1)
        else:
            dprint("TAIL IS IN UNKNOWN LOCATION")
            print_grid(5, head_position, tail_position)
            exit(1)

def print_grid(size, head_loc, tail_loc):
    for y in range(size-1, -1, -1):
        for x in range(0, size+1):
            point = (x, y)
            if head_loc == point and tail_loc == point:
                dprint("X", end="")
            elif head_loc == point:
                dprint("H", end="")
            elif tail_loc == point:
                dprint("T", end="")
            elif point == (0, 0):
                dprint("s", end="")
            else:
                dprint(".", end="")
        dprint()

def manhattan_distance(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return abs(x1-x2) - abs(y1-y2)

def part_1():
    head_location = (0, 0)
    tail_location = (0, 0)

    tail_visited = set()

    for direction, amount in input_data:
        dprint(f"--- {direction, amount} ---")
        print_grid(5, head_location, tail_location)
        dprint()
        dprint()
        for i in range(int(amount)):
            head_location = move_head(head_location, direction, 1)
            tail_location = move_tail(tail_location, head_location)
            tail_visited.add(tail_location)
            print_grid(5, head_location, tail_location)
            dprint()
            dprint()
    return len(tail_visited)

def part_2():
    pass

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")