import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

import re
from collections import defaultdict
from aoc_common.benchmark import print_timing
import copy

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

def read_tower():
    tower = defaultdict(lambda: [])
    tower_buffer = []
    for line in input_data:
        if line.lstrip().startswith('1'):
            # Reached the key
            key = [int(x) for x in re.sub('\s+', ' ', line).split(' ') if x]
            dprint(f'Found key: {key}')
            for buffered_line in tower_buffer:
                row = [buffered_line[i] for i in range(1, len(buffered_line), 4)]
                for i in range(len(row)):
                    if row[i] != ' ':
                        tower[i+1].append(row[i])
            break
        else:
            tower_buffer.append(line)

    reversed_tower = {}
    for k, v in tower.items():
        reversed_tower[k] = [x for x in reversed(v)]
    return reversed_tower


instruction_regex = re.compile(r"move (\d+) from (\d+) to (\d+)")

instructions = []

# Read the instructions
for line in input_data:
    if not line.startswith('move'):
        dprint(f"Skipping line {line}")
        continue
    dprint(f"Parsing instruction {line}")
    instruction = instruction_regex.match(line)
    instructions.append(instruction.groups())


def print_tower(tower):
    # Print the tower
    for x in range(1, len(tower.keys())+1):
        v = tower[x]
        dprint(f"{x}: {v}")

for instruction in instructions:
    dprint(f"* {instruction}")


@print_timing
def part_1():
    tower = read_tower()
    for amount, source_col, dest_col in instructions:
        dprint("--- Iteration ---")
        source_col = int(source_col)
        amount = int(amount)
        dest_col = int(dest_col)
        dprint(f"Moving {amount} from {source_col} to {dest_col}")

        source_col = tower[source_col]
        dest_col = tower[dest_col]
        for i in range(amount):
            dest_col.append(source_col.pop())
        print_tower(tower)
    
    final = ""
    for i in range(1, len(tower.keys())+1):
        final += tower[i][-1]
    return final

@print_timing
def part_2():
    tower = read_tower()
    for amount, source_col, dest_col in instructions:
        dprint("--- Iteration ---")
        source_col = int(source_col)
        amount = int(amount)
        dest_col = int(dest_col)
        dprint(f"Moving {amount} from {source_col} to {dest_col}")

        source_col = tower[source_col]
        dest_col = tower[dest_col]
        buffer = []
        for i in range(amount):
            buffer.append(source_col.pop())
        
        for item in reversed(buffer):
            dest_col.append(item)

        print_tower(tower)
    
    final = ""
    for i in range(1, len(tower.keys())+1):
        final += tower[i][-1]
    return final

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")