import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from aoc_common.io import to_2d_matrix
from functools import reduce
from aoc_common.benchmark import print_timing

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


input_data = to_2d_matrix(input_data, mapper=lambda x: int(x))

dprint(input_data)

size_x = len(input_data[0])
size_y = len(input_data[1])

dprint(f"Grid is {size_x}x{size_y}")


def get_tree_at(x, y, grid):
    dprint(f"Getting tree at {x},{y}", end="")
    val = grid[y][x]
    dprint(f": {val}")
    return val


def visible_from(pos, grid, side):
    x, y = pos
    tree_height = grid[y][x]

    if x == 0:
        return True
    if x == size_x-1:
        return True
    if y == 0:
        return True
    if y == size_y-1:
        return True

    if side == "top":
        for dy in range(y):
            h = get_tree_at(x, dy, grid)
            if h >= tree_height:
                dprint(f"Tree {pos} is not visible from the top")
                return False
        dprint(f"Tree {pos} is visible from the top")
        return True
    if side == "bottom":
        for dy in range(size_y-1, y, -1):
            h = get_tree_at(x, dy, grid)
            if h >= tree_height:
                dprint(f"Tree {pos} is not visible from the bottom")
                return False
        dprint(f"Tree {pos} is visible from the bottom")
        return True
    if side == "left":
        for dx in range(x):
            h = get_tree_at(dx, y, grid)
            if h >= tree_height:
                dprint(f"Tree {pos} is not visible from the left")
                return False
        dprint(f"Tree {pos} is visible from the left")
        return True
    
    if side == "right":
        for dx in range(size_x-1, x, -1):
            h = get_tree_at(dx, y, grid)
            if h >= tree_height:
                dprint(f"Tree {pos} is not visible from the right")
                return False
        dprint(f"Tree {pos} is visible from the right")
        return True

def trace_to_edge(pos, grid, edge):
    x, y = pos
    if edge == "top":
        return [get_tree_at(x, dy, grid) for dy in range(y-1, -1, -1)]
    
    if edge == "bottom":
        return [get_tree_at(x, dy, grid) for dy in range(y+1, size_y)]

    if edge == "left":
        return [get_tree_at(dx, y, grid) for dx in range(x-1, -1, -1)]
    
    if edge == "right":
        return [get_tree_at(dx, y, grid) for dx in range(x+1, size_x)]

def get_obstructed_index(tree_height, trace):
    for i in range(len(trace)):
        dprint(f"Obstructed? {tree_height} <= {trace[i]}?")
        if tree_height <= trace[i]:
            return i+1
    return len(trace)

def scenic_score(pos, grid):
    x, y = pos
    return reduce(lambda x, acc: x*acc, [get_obstructed_index(get_tree_at(x, y, grid), trace_to_edge((x, y), grid, edge)) for edge in ["top", "bottom", "left", "right"]])

def is_visible(pos, grid):
    grid = [visible_from(pos, grid, x) for x in ["top", "bottom", "left", "right"]]
    dprint(f"Tree {pos} is visible from {grid}")
    return any(grid)

@print_timing
def part_1():
    count = 0
    for x in range(size_x):
        for y in range(size_y):
            if is_visible((x, y), input_data):
                count += 1
    return count

@print_timing
def part_2():
     return max([scenic_score((x, y), input_data) for x in range(size_x) for y in range(size_y)])

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")