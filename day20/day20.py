import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from collections import deque
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

dprint(input_data)

file = [int(x) for x in input_data]

def mix(file, indicies, pos=0):
    dprint("I", indicies)
    dprint("F", file)
    for i in tqdm(range(len(file)), "Mixing", position=pos, leave=False):
        dprint()
        dprint(f"Processing move {i+1}")
        source_index = indicies.index(i)
        dprint(f"Target is at {source_index}")

        # Rotate the file so the source number is first
        indicies.rotate(-source_index)
        file.rotate(-source_index)

        # Remove it
        index = indicies.popleft()
        number = file.popleft()

        dprint("1I", indicies)
        dprint("1F", file)

        dprint(f"Moving", number)
        
        # Move the file so the target is first
        indicies.rotate(-number)
        file.rotate(-number)

        dprint("2I", indicies)
        dprint("2F", file)

        # Prepend to the file
        file.appendleft(number)
        indicies.appendleft(index)

        dprint("FI", indicies)
        dprint("FF", file)


def get_grove_coordinates(mixed_file):
    location = mixed_file.index(0)
    def _get_at(number):
        return mixed_file[number % len(mixed_file)]
    return _get_at(location + 1000) + _get_at(location + 2000) + _get_at(location + 3000)


def part_1():
    file_queue = deque(file)
    indicies = deque(range(len(file)))
    mix(file_queue, indicies)
    return get_grove_coordinates(file_queue)

def part_2():
    DECRYPTION_KEY = 811589153
    decrypted_file = deque([x * DECRYPTION_KEY for x in file])
    indicies = deque(range(len(file)))

    for _ in tqdm(range(10), position=0, leave=False):
        mix(decrypted_file, indicies, pos=1)
    return get_grove_coordinates(decrypted_file)


print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")