import math
from collections import defaultdict

with open('input.txt') as f:
    input_data = list(map(lambda x: x.replace('\n', ''), f.readlines()))

def do_split(compartment):
    size = math.floor(len(compartment) / 2)
    return compartment[0:size], compartment[size:]

compartments = [do_split(x) for x in input_data]


def find_common(pocket1, pocket2, pocket3=None, target=1):
    a = defaultdict(lambda: 0)
    seen_a = []
    seen_b = []
    for i in pocket1:
        if i not in seen_a:
            a[i] += 1
            seen_a.append(i)
    for i in pocket2:
        if i not in seen_b:
            a[i] += 1
            seen_b.append(i)
    if pocket3 is not None:
        seen_c = []
        for i in pocket3:
            if i not in seen_c:
                a[i] += 1
                seen_c.append(i)
    return [k for k, v in a.items() if v > target]

def get_priority(item):
    if item <= 'Z' and item >= 'A':
        alphabet = (26 - ('Z'.encode()[0] - item.encode()[0])-1) + 27
        return alphabet
    if item <= 'z' and item >= 'a':
        alphabet = 26 - ('z'.encode()[0] - item.encode()[0])
        return alphabet

def part_1():
    priority = 0
    for a, b in compartments:
        common = find_common(a, b)
        priority += sum([get_priority(x) for x in common])
    return priority

def part_2():
    priority = 0
    for x in range(0, len(input_data), 3):
        group = input_data[x:x+3]
        common = find_common(group[0], group[1], group[2], 2)
        priority += sum([get_priority(x) for x in common])
    return priority


print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")
