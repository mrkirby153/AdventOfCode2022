import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

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


snafu_map = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

def from_snafu(number):
    num_reversed = reversed(number)
    base10_number = 0
    for place, num in enumerate(num_reversed):
        multiplier = pow(5, place)
        base10_number += (snafu_map[num] * multiplier)
        dprint(num, "in the", multiplier, "place")
    return base10_number


rev_map = {
    0: ('0', 0),
    1: ('1', 0),
    2: ('2', 0),
    3: ('=', 2),
    4: ('-', 1)
}
def to_snafu(base10_number):
    num = base10_number
    digits = []
    
    while num:
        mod = num % 5
        digit, offset = rev_map[mod]
        digits.append(digit)
        num = (num + offset) // 5
    return ''.join(digits[::-1])
def part_1():
    acc = 0
    for line in input_data:
        acc += from_snafu(line)
    return to_snafu(acc)

print(f"Part 1: {part_1()}")