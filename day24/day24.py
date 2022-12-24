import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from collections import defaultdict
from functools import cache
from math import lcm

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


@cache
def load_grid():
    grid = defaultdict(list)
    for y, row in enumerate(input_data):
        for x, col in enumerate(row):
            point = complex(x, y)
            if col in ['^', 'v', '<', '>']:
                grid[point].append(col)
            if col == '#':
                grid[point] = False
    return grid


def print_grid(grid, print_func=dprint):
    x, y = [int(point.real) for point in grid], [int(point.imag) for point in grid]
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)

    for y in range(min_y, max_y+1):
        row = ""
        for x in range(min_x, max_x+1):
            point = complex(x, y)
            point = grid[point]
            if point == False:
                row += "#"
            elif len(point) == 1:
                row += str(point[0])
            elif len(point) == 0:
                row += "."
            else:
                row += str(len(point))
        print_func(row)

def get_start_end_positions(grid):
    return grid[0].index("."), grid[-1].index(".") + (len(grid) - 1) * 1j

direction_map = {
    '^': 0-1j,
    'v': 0+1j,
    '>': 1+0j,
    '<': -1+0j
}

def get_grid_dimensions(grid):
    x, y = [int(point.real) for point in grid], [int(point.imag) for point in grid]
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)
    return (min_x, max_x), (min_y, max_y)


directions = [
    0-1j, # Up
    0+1j, # Down
    1+0j, # Left
    -1+0j, # Right
    0 # Don't move
]

def bfs(start, end, safe, wrap, start_time=0):
    queue = [(start, start_time)]
    seen = set()
    i = 0
    while queue:
        pos, time = queue.pop(0)
        if pos == end:
            print()
            return time
        if i % 1000 == 0: # print status every 1000 rounds
            print(time, len(queue), end="\r")
        i += 1
        if (pos, time) in seen:
            continue # Already explored

        seen.add((pos, time))
        new_time = time + 1
        for dir in directions:
            new_pos = pos + dir
            if new_pos in safe and (new_time % wrap) in safe[new_pos]:
                queue.append((new_pos, new_time))
    assert False # No paths found


def get_dimensions(grid):
    return len(grid), len(grid[0])

def get_wrap_time(grid):
    rows, cols = get_dimensions(grid)
    return lcm(rows - 2, cols - 2)

def determine_safe_points(grid):
    rows, cols = get_dimensions(grid)
    wrap = get_wrap_time(grid)
    safe = {
        complex(x, y): set(range(wrap)) for y in range(rows) for x in range(cols)
    }

    for y, row in enumerate(input_data):
        for x, col in enumerate(row):
            position = complex(x, y)

            if col == "#":
                safe[position] = set() # Outside edge is never safe
                continue
            if col == '.':
                continue # No blizzard at this point currently

            direction = direction_map[col]

            for t in range(wrap):
                safe[position].discard(t)  # Mark all spaces that this blizzard traces as unsafe
                position += direction
                position = complex((position.real - 1) % (cols - 2) + 1, (position.imag - 1) % (rows - 2) + 1)
    return safe

def part_1():
    start, end = get_start_end_positions(input_data)
    print(start, end)

    wrap = get_wrap_time(input_data) # The grid is identical every wrap steps
    safe_points = determine_safe_points(input_data)
    return bfs(start, end, safe_points, wrap)


def part_2():
    start, end = get_start_end_positions(input_data)
    print(start, end)

    wrap = get_wrap_time(input_data) # The grid is identical every wrap steps
    safe_points = determine_safe_points(input_data)

    there = bfs(start, end, safe_points, wrap)
    back = bfs(end, start, safe_points, wrap, there)
    there2 = bfs(start, end, safe_points, wrap, back)
    return there2

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")