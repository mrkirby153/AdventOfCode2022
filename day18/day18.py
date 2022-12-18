import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from tqdm import tqdm

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


input_data = [tuple(map(lambda x: int(x), x.split(","))) for x in input_data]

dprint(input_data)

def get_adjacent_cubes(point):
    x, y, z = point
    cubes = []
    # Up
    cubes.append((x, y+1, z))
    # Down
    cubes.append((x, y-1, z))
    # Left
    cubes.append((x-1, y, z))
    # Right
    cubes.append((x+1, y, z))
    # Front
    cubes.append((x, y, z+1))
    # Back
    cubes.append((x, y, z-1))
    return cubes

def get_grid_dimensions(input_data):
    def _get_axis_dimensions(axis):
        assert axis >= 0
        assert axis <= 2
        points = [x[axis] for x in input_data]
        return range(min(points), max(points)+1)
    return tuple([_get_axis_dimensions(x) for x in range(3)])

def part_1():
    total_surface_area = 0
    for cube in tqdm(input_data, "Exposd Faces"):
        exposd_faces = [x for x in get_adjacent_cubes(cube) if x not in input_data]
        total_surface_area += len(exposd_faces)
    return total_surface_area

def part_2():
    global input_data
    input_data = set(input_data)
    (x_range, y_range, z_range) = get_grid_dimensions(input_data)
    print(x_range, y_range, z_range)
    exposed_faces = 0

    known_exterior_points = set()
    def check(pos):
        if pos in input_data:
            return False
        visited = set()
        pending = [pos]

        while pending:
            x, y, z = pending.pop()
            if (x, y, z) in visited:
                continue # Already visited
            visited.add((x, y, z))
            if (x, y, z) in known_exterior_points:
                # We already know this point is exterior
                known_exterior_points.update(visited - input_data) # Filter out points that aren't actually in the set of points
                return True
            if x not in x_range or y not in y_range or z not in z_range:
                # Outside of the cube, this point must be the exterior
                known_exterior_points.update(visited - input_data) # Filter out points that aren't actually in the set of points
                return True
            if (x, y, z) not in input_data:
                pending += get_adjacent_cubes((x, y, z))
        return False
    
    for point in tqdm(input_data, "Exterior"):
        for n in get_adjacent_cubes(point):
            if check(n):
                exposed_faces += 1

    return exposed_faces

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")