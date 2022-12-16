import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

import re
from functools import lru_cache

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

valve_flow_rates = {}
valve_tunnels = {}

input_re = re.compile(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
for line in input_data:
    matcher = input_re.match(line)
    valve, rate, tunnels = matcher.groups()
    tunnels = tunnels.split(', ')
    valve_flow_rates[valve] = int(rate)
    valve_tunnels[valve] = tunnels

dprint(valve_flow_rates)
dprint(valve_tunnels)

potential_valves = sorted([x[0] for x in valve_flow_rates.items() if x[1] != 0])


@lru_cache(maxsize=None)
def get_max_flow_rate(current_position, opened_valves, time_left, depth=0):
   # dprint("  "*depth, current_position, opened_valves, time_left)
    if time_left <= 0:
        return 0
    
    # If the valve can open, we want to open the valve and consider the case where we can't open the valve
    # If the valve can't open, we just want to cosnider the adjacent spaces
    if valve_flow_rates[current_position] == 0 or current_position in opened_valves:
        best = 0
        for adjacent in valve_tunnels[current_position]:
            best = max(best, get_max_flow_rate(adjacent, opened_valves, time_left - 1, depth+1))
        return best
    else:
        gained_flow = (time_left - 1) * valve_flow_rates[current_position]
        best = 0
        opened = tuple(sorted(opened_valves + (current_position,)))
        for adjacent in valve_tunnels[current_position]:
            best = max(best, gained_flow + get_max_flow_rate(adjacent, opened, time_left - 2, depth+1))
            best = max(best, gained_flow + get_max_flow_rate(adjacent, opened_valves, time_left - 1, depth+1))
        return best

def part_1():
    return get_max_flow_rate('AA', (), 30)

def part_2():
    pass

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")