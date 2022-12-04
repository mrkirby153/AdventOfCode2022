import argparse

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

assignments = []

for row in input_data:
    one, two = row.split(',')
    one_start, one_end = one.split('-')
    two_start, two_end = two.split('-')
    assignments.append(((int(one_start), int(one_end)), (int(two_start), int(two_end))))

dprint(assignments)


def partially_contained(range_one, range_two):
    x1, x2 = range_one.start, range_one.stop
    y1, y2 = range_two.start, range_two.stop
    return x1 <= y2 and y1 <= x2

def fully_contained(range_one, range_two):
    x1, x2 = range_one.start, range_one.stop
    y1, y2 = range_two.start, range_two.stop
    return y1 >= x1 and y2 <= x2

def part_1():
    overlapping_count = 0
    for (one_start, one_end), (two_start, two_end) in assignments:
        r1 = range(one_start, one_end)
        r2 = range(two_start, two_end)
        if fully_contained(r1, r2) or fully_contained(r2, r1):
            dprint(f"overlapping: {(one_start, one_end)}, {(two_start, two_end)}")
            overlapping_count += 1
    return overlapping_count

def part_2():
    overlapping_count = 0
    for (one_start, one_end), (two_start, two_end) in assignments:
        r1 = range(one_start, one_end)
        r2 = range(two_start, two_end)
        if partially_contained(r1, r2) or partially_contained(r2, r1):
            dprint(f"overlapping: {(one_start, one_end)}, {(two_start, two_end)}")
            overlapping_count += 1
    return overlapping_count

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")