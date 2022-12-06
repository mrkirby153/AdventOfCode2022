import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from collections import Counter

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

dprint(input_data)


def part_1():
    last_four = []
    for i, char in enumerate(input_data):
        i = i + 1
        if len(last_four) == 4:
            last_four = last_four[1:]
        last_four.append(char)
        dprint(f"{i}: {last_four}")
        count = Counter(last_four)
        if all(map(lambda x: x == 1, count.values())) and len(last_four) == 4:
            return i

def part_2():
    last_fourteen = []
    for i, char in enumerate(input_data):
        i = i + 1
        if len(last_fourteen) == 14:
            last_fourteen = last_fourteen[1:]
        last_fourteen.append(char)
        dprint(f"{i}: {last_fourteen}")
        count = Counter(last_fourteen)
        if all(map(lambda x: x == 1, count.values())) and len(last_fourteen) == 14:
            return i

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")