import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from tqdm import tqdm
import re

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


def manhattan_distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(x2 - x1) + abs(y2 - y1)

dprint(input_data)

sensors_to_beacons = {}
beacon_distances = {}

pattern = re.compile(r"Sensor at x=(-?\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

for line in input_data:
    match = pattern.match(line)
    sensor_x, sensor_y = int(match.group(1)), int(match.group(2))
    beacon_x, beacon_y = int(match.group(3)), int(match.group(4))
    dprint(f"Sensor {sensor_x}, {sensor_y}: {beacon_x}, {beacon_y}")
    sensors_to_beacons[(sensor_x, sensor_y)] = (beacon_x, beacon_y)
    beacon_distances[(sensor_x, sensor_y)] = manhattan_distance((sensor_x, sensor_y), (beacon_x, beacon_y))

dprint(sensors_to_beacons)
dprint(beacon_distances)


x_coordinates = [x[0] for x in list(sensors_to_beacons.keys()) + list(sensors_to_beacons.values())]
#dprint(x_coordinates)
min_x = min(x_coordinates)
max_x = max(x_coordinates)

y_coordinates = [x[1] for x in list(sensors_to_beacons.keys()) + list(sensors_to_beacons.values())]
min_y = min(y_coordinates)
max_x = max(y_coordinates)

def find_min_max(pairs):
    min_x, max_x = None, None
    for x, y in pairs:
        if min_x is None or x - pairs[x, y] < min_x:
            min_x = x - pairs[x, y]
        if max_x is None or x + pairs[x, y] > max_x:
            max_x = x + pairs[x, y]
    return min_x, max_x

def get_empty_beacon(y, sensors_to_beacons, beacon_distances):
    min_x, max_x = find_min_max(beacon_distances)
    invalid = 0
    for x in tqdm(range(min_x, max_x + 1)):
        for (beacon_x, beacon_y), distance in beacon_distances.items():
            if manhattan_distance((x, y), (beacon_x, beacon_y)) <= distance:
                invalid += 1
                break
    beacons_at_y = set((x for x in sensors_to_beacons.values() if x[1] == y))
    dprint(beacons_at_y)

    return invalid - len(beacons_at_y)

def part_1():
    row = 10 if parsed_args.sample else 2000000
    return get_empty_beacon(row, sensors_to_beacons, beacon_distances)

def part_2():
    pass

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")