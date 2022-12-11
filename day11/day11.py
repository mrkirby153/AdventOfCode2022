import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

from collections import defaultdict
from functools import reduce
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

class Monkey:

    def __init__(self, num, items, operation, test, if_true, if_false) -> None:
        self.num = num
        self.items = items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false

def load_data():
    monkeys = {}
    i = 0
    while i < len(input_data):
        target_lines = input_data[i:i+6]
        dprint(target_lines)
        monkey_num = int(target_lines[0].split(" ")[1][:-1])
        dprint(f"Monkey number {monkey_num}")
        starting_items = target_lines[1].strip().split(" ")[2:]
        starting_items = list(map(lambda x: int(x.replace(',', '')), starting_items))
        dprint(f"Starting items: {starting_items}")
        operation_text = target_lines[2].split(": ")[1].split("= ")[1]
        operation_func = eval(f"lambda old: {operation_text}")
        dprint(f"Operation: {operation_text} - {operation_func}")
        test = int(target_lines[3].split(" ")[-1])
        if_true = int(target_lines[4].split(" ")[-1])
        if_false = int(target_lines[5].split(" ")[-1])
        dprint(f"Test: divisible by {test}: {if_true} else {if_false}")
        monkeys[monkey_num] = Monkey(monkey_num, starting_items, operation_func, test, if_true, if_false)
        i += 7
    return monkeys

def inspect_all_items(monkey: Monkey):
    destinations = defaultdict(lambda: [])
    dprint(f"Monkey {monkey.num}")
    for item in monkey.items:
        dprint(f"==> Inspecting item with worry level {item}")
        new_worry_level = monkey.operation(item)
        dprint(f"Worry level is now {new_worry_level}")
        new_worry_level //= 3
        dprint(f"Worry level is now {new_worry_level}")
        test_results = new_worry_level % monkey.test == 0
        dprint(f"Test results: {test_results}")
        target_monkey = monkey.if_true if test_results else monkey.if_false
        dprint(f"Throwing item with {new_worry_level} to {target_monkey}")
        destinations[target_monkey].append(new_worry_level)
    return destinations

def inspect_all_items_pt2(monkey: Monkey, lcm):
    destinations = defaultdict(lambda: [])
    dprint(f"Monkey {monkey.num}")
    for item in monkey.items:
        dprint(f"==> Inspecting item with worry level {item}")
        new_worry_level = monkey.operation(item)
        dprint(f"Worry level is now {new_worry_level}")
        new_worry_level = new_worry_level % lcm
        dprint(f"Worry level is now {new_worry_level}")
        test_results = new_worry_level % monkey.test == 0
        dprint(f"Test results: {test_results}")
        target_monkey = monkey.if_true if test_results else monkey.if_false
        dprint(f"Throwing item with {new_worry_level} to {target_monkey}")
        destinations[target_monkey].append(new_worry_level)
    return destinations


def print_all_monkey_items(monkeys):
    for k, v in monkeys.items():
        dprint(f"Monkey {k}: {','.join(map(str, v.items))}")

def part_1():
    monkeys = load_data()
    dprint(monkeys)

    inspected = defaultdict(lambda: 0)

    for i in range(20):
        for mid, monkey in monkeys.items():
            if len(monkey.items) > 0:
                inspected[mid] += len(monkey.items)
                destinations = inspect_all_items(monkey)
                monkey.items = [] # monkey has thrown all of its items
                for dest_monkey, items in destinations.items():
                    monkeys[dest_monkey].items += items
            else:
                dprint(f"Monkey {mid} has no items. Skipping")
        dprint()
        dprint(f"END OF ROUND {i+1}")
        print_all_monkey_items(monkeys)
    
    inspected = {k: v for k, v in inspected.items()}

    monkey_business = sorted(inspected.values(), reverse=True)
    dprint(monkey_business)
    return monkey_business[0] * monkey_business[1]

def part_2():
    monkeys = load_data()
    dprint(monkeys)

    inspected = defaultdict(lambda: 0)

    # The trick: All monkey values are prime, which means we can smoosh them all together and use that as a modulo to keep the numbers from going bananas
    modulo = reduce(lambda x, y: x*y, map(lambda x: x.test, monkeys.values()), 1)

    dprint(f"modulo: {modulo}")
    for i in tqdm(range(10000)):
        for mid, monkey in monkeys.items():
            if len(monkey.items) > 0:
                inspected[mid] += len(monkey.items)
                destinations = inspect_all_items_pt2(monkey, modulo)
                monkey.items = [] # monkey has thrown all of its items
                for dest_monkey, items in destinations.items():
                    monkeys[dest_monkey].items += items
            else:
                dprint(f"Monkey {mid} has no items. Skipping")
        dprint()
        dprint(f"END OF ROUND {i+1}")
        to_print = {k: v for k, v in inspected.items()}
        dprint(to_print)
        
    
    inspected = {k: v for k, v in inspected.items()}

    monkey_business = sorted(inspected.values(), reverse=True)
    dprint(monkey_business)
    return monkey_business[0] * monkey_business[1]

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")