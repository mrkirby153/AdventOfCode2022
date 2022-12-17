import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

import re
from functools import lru_cache
from math import inf

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
def get_max_flow_rate(current_position, opened_valves, time_left):
    if time_left <= 0:
        return 0
    
    # If the valve can open, we want to open the valve and consider the case where we can't open the valve
    # If the valve can't open, we just want to cosnider the adjacent spaces
    if valve_flow_rates[current_position] == 0 or current_position in opened_valves:
        best = 0
        for adjacent in valve_tunnels[current_position]:
            best = max(best, get_max_flow_rate(adjacent, opened_valves, time_left - 1))
        return best
    else:
        gained_flow = (time_left - 1) * valve_flow_rates[current_position]
        best = 0
        opened = tuple(sorted(opened_valves + (current_position,)))
        for adjacent in valve_tunnels[current_position]:
            best = max(best, gained_flow + get_max_flow_rate(adjacent, opened, time_left - 2))
            best = max(best, get_max_flow_rate(adjacent, opened_valves, time_left - 1))
        return best

valve_distances = {}

def djikstra(valve):
    possible = {valve: 0}
    explored = set()
    while len(explored) < len(valve_tunnels):
        current = min(((k, v) for k, v in possible.items() if k not in explored), key=lambda x: x[1])[0]
        for other in valve_tunnels[current]:
            new_dist = possible[current] + 1
            if possible.get(other, inf) > new_dist:
                explored.discard(other)
                possible[other] = new_dist
            explored.add(current)
    return possible


valve_distances = {k: djikstra(k) for k in valve_tunnels.keys() }

max_flow_seen = 0
@lru_cache(maxsize=None)
def run_part_2(cur, other, closed_valves):
    cur_time_left, cur_pos = cur
    other_time_left, other_pos = other
    totals = [0]
    for valve in closed_valves:
        time_to_valve = valve_distances[cur_pos].get(valve) + 1
        time_left = cur_time_left - time_to_valve
        if time_left <= 0:
            continue # Can't get to the valve and open it

        flow_gained = time_left * valve_flow_rates[valve]

        # Move the person that has the most time left
        if time_left > other_time_left:
            totals.append(flow_gained + run_part_2((time_left, valve), other, closed_valves - {valve}))
        else:
            totals.append(flow_gained + run_part_2(other, (time_left, valve), closed_valves - {valve}))
    max_flow = max(totals)

    global max_flow_seen
    if max_flow > max_flow_seen:
        print("New max:", max_flow)
        max_flow_seen = max_flow
    return max_flow

def part_1():
    return get_max_flow_rate('AA', (), 30)

def part_2():
    return run_part_2((26, 'AA'), (26, 'AA'), frozenset(potential_valves))

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")