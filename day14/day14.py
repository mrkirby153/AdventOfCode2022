import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from aoc_common.io import print_2d_matrix

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

# dprint(input_data)


paths = []

for line in input_data:
    points = line.split(' -> ')
    path = []
    for point in points:
        x, y = point.split(',')
        path.append((int(x), int(y)))
    paths.append(path)

dprint(paths)
SAND_GENERATION_POINT = (500, 0)

# Determine the size of the grid that we need
x_points = [x[0] for path in paths for x in path]
min_x = min(x_points)
max_x = max(x_points)

y_points = [x[1] for path in paths for x in path]
max_y = max(y_points)

print(f"X coordinates: {min_x} to {max_x}")
print(f"Y coordinates 0 to {max_y}")

def translate_x_coordinate_to_local_position(x_coordinate):
    """
    Translates an x coordinate from the global space to the local space
    """
    return x_coordinate - min_x

dprint("min x local", translate_x_coordinate_to_local_position(min_x))
dprint("max x local", translate_x_coordinate_to_local_position(max_x))

def translate_to_local_position(position):
    x, y = position
    return (translate_x_coordinate_to_local_position(x), y)


def get_points_for_segment(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2

    if x1 == x2:
        if y2 < y1:
            return [(x1, y) for y in range(y1, y2-1, -1)]
        else:
            return [(x1, y) for y in range(y1, y2+1)]
    if y1 == y2:
        if x2 < x1:
            return [(x, y1) for x in range(x1, x2-1, -1)]
        else:
            return [(x, y1) for x in range(x1, x2+1)]

def get_local_points_for_path(path):
    points = []
    for i in range(1, len(path)):
        point_2 = path[i]
        point_1 = path[i-1]
        points += list(map(translate_to_local_position, get_points_for_segment(point_1, point_2)))
    return points


def generate_grid():
    grid = []
    for _ in range(max_y+1):
        grid.append([None for _ in range(max_x - min_x + 1)])

    sand_x, sand_y = translate_to_local_position(SAND_GENERATION_POINT)
    grid[sand_y][sand_x] = '+'

    for path in paths:
        dprint(f"Plotting path {path}")
        dprint(get_local_points_for_path(path))
        for x, y in get_local_points_for_path(path):
            grid[y][x] = "#"

    print_grid(grid)
    return grid

def print_grid(grid):
    def _translator(point):
        return '.' if point is None else point
    print_2d_matrix(grid, dprint, _translator)

def drop_sand(grid):
    x, y = translate_to_local_position(SAND_GENERATION_POINT)
    dprint("Dropping from ", x, y)
    while y < len(grid):
        y += 1
        dprint("Below", grid[y][x])
        if grid[y][x] is not None:
            # There is something in the way
            left = x - 1
            right = x + 1
            dprint("Left", left, grid[y][left])
            dprint("Right", right, grid[y][right])
            if grid[y][left] is None:
                dprint("Space left")
                x = left
            elif grid[y][right] is None:
                dprint("Space right")
                x = right
            else:
                dprint("Set")
                return (x, y-1)

def part_1():
    grid = generate_grid()

    i = 0
    try:
        while True:
            x, y = drop_sand(grid)
            grid[y][x] = 'o'
            print_grid(grid)
            i += 1
    except IndexError:
        return i

def part_2():
    pass

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")