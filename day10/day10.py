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

input_data = [(x.split(' ')[0], int(x.split(' ')[1]) if len(x.split(' ')) == 2 else None) for x in input_data]

# nput_data = [(x, 0 if x[0] == "noop" else 1) for x in input_data]
dprint(input_data)


def cycle_generator():
    next_cycle = 20
    while True:
        yield next_cycle
        next_cycle += 40


x = 1
cycle = 1
target = 20
strengths = []

def step_cycle(delta_x):
    global x
    global cycle
    global target
    dprint(f"Cycle {cycle} start")
    if cycle == target:
        dprint(f"Triggered at cycle {cycle}: {x}")
        strengths.append(cycle * x)
        target += 40
    x += delta_x
    dprint(f"Moved x by {delta_x} -> {x}")
    cycle += 1

def part_1():
    for instruction, data in input_data:
        if instruction == "noop":
            step_cycle(0)
        if instruction == "addx":
            step_cycle(0)
            step_cycle(data)
    return sum(strengths)

current_row = ""
screen = ""

def sprite_position(x):
    pos = ""
    for i in range(40):
        if x - 1 <= i <= x + 1:
            pos += '█'
        else:
            pos += ' '
    return pos

def draw_sprite(delta_x):
    global x
    global cycle
    global current_row
    global screen
    dprint(f"Cycle {cycle} start")
    position = (cycle % 40) - 1
    current_row += '█' if x - 1 <= position <= x + 1 else ' '
    if cycle % 40 == 0:
        screen += f"{current_row}\n"
        current_row = ""
    x += delta_x
    dprint(f"CRT row: {current_row}")
    dprint(f"End of cycle {cycle}")
    dprint(f"Sprite Position: {sprite_position(x)}")
    cycle += 1


def part_2():
    for instruction, data in input_data:
        if instruction == "noop":
            draw_sprite(0)
        if instruction == "addx":
            draw_sprite(0)
            draw_sprite(data)
    return f"\n{screen}"

print(f"Part 1: {part_1()}")
x = 1
cycle = 1

print(f"Part 2: {part_2()}")