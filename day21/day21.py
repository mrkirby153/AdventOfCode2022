import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from z3 import *

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


def part_1():
    s = Solver()
    for line in input_data:
        var, body = line.split(":")
        var = var.strip()
        body = body.strip()
        #dprint(var, body)
        parts = body.split(" ")
        if len(parts) == 3:
            first, op, second = parts
            assert op in ["+", "-", "*", "/"]
            if op == "+":
                s.add(Int(var) == Int(first) + Int(second))
            if op == "-":
                s.add(Int(var) == Int(first) - Int(second))
            if op == "*":
                s.add(Int(var) == Int(first) * Int(second))
            if op == "/":
                s.add(Int(var) == Int(first) / Int(second))
        else:
            s.add(Int(var) == int(body))
    dprint(s)
    assert s.check() == sat
    model = s.model()
    dprint("Model", model)
    return model[Int("root")]

def part_2():
    s = Optimize() # Optimize and not solve due to integer division
    for line in input_data:
        var, body = line.split(":")
        var = var.strip()
        body = body.strip()
        dprint(var, body)
        parts = body.split(" ")
        if var == "humn":
            continue # Don't care anymore
        if len(parts) == 3:
            first, op, second = parts
            assert op in ["+", "-", "*", "/"]
            if var == "root":
                s.add(Int(first) == Int(second)) # Ensure the first must equal the second
            else:
                if op == "+":
                    s.add(Int(var) == Int(first) + Int(second))
                if op == "-":
                    s.add(Int(var) == Int(first) - Int(second))
                if op == "*":
                    s.add(Int(var) == Int(first) * Int(second))
                if op == "/":
                    s.add(Int(var) == Int(first) / Int(second))
        else:
            s.add(Int(var) == int(body))
    dprint("Constraints", s)
    assert s.check() == sat
    model = s.model()
    return model[Int("humn")]

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")

# 3882224466193 -- Too high