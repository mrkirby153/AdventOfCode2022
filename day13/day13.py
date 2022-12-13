import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

parser = argparse.ArgumentParser()
parser.add_argument('--sample', '-s', help='Run with sample data', action='store_true', default=False)
parser.add_argument('--debug', '-d', required=False, type=int)

parsed_args = parser.parse_args()

if parsed_args.sample:
    print("Using sample data!")

def dprint(*args, **kwargs):
    if parsed_args.sample:
        print(*args, **kwargs)

with open('input.txt' if not parsed_args.sample else 'sample.txt') as f:
    input_data = list(map(lambda x: x.replace('\n', ''), f.readlines()))

#dprint(input_data)

pairs = [(eval(input_data[i]), eval(input_data[i+1])) for i in range(0, len(input_data), 3)]

#dprint(f"Pairs: {pairs}")

def compare(left, right, depth=0):
    prefix="    "*depth
    dprint(f"{prefix}Comparing {left} vs {right}")
    if isinstance(left, list) and isinstance(right, list):
        # Both items are a list
        for i in range(min(len(left), len(right))):
            result = compare(left[i], right[i], depth+1)
            # dprint(f"{prefix}Result: {result}")
            if result == None:
                continue
            else:
                return result
        dprint(f"{prefix}out of items", 'left' if len(left) < len(right) else 'right')
        if len(left) != len(right):
            return len(left) < len(right)
        else:
            return None
    elif isinstance(left, list) or isinstance(right, list):
        # Coalesce the integer into a list
        dprint(f"{prefix*2}Mixed types, covnerting")
        return compare(left if isinstance(left, list) else [left], right if isinstance(right, list) else [right], depth+1)
    else:
        # dprint(f"{prefix}Direct comparison", left == right, left <= right)
        # Direct comparison
        if left == right:
            return None
        return left <= right
def part_1():
    if parsed_args.debug is not None:
        i = parsed_args.debug -1
        dprint(f"Debugging pair {i}")
        dprint()
        first, second = pairs[i]
        return compare(first, second)
    acc = 0
    results = {}
    for i, (first, second) in enumerate(pairs):
        results[i+1] = compare(first, second)

    for k, v in results.items():
        dprint(f"Pair {k}: {v}")
        if v:
            acc += k
    return acc

# Python program for implementation of Bubble Sort
 
def bubble_sort(arr):
    n = len(arr)
    # optimize code, so if the array is already sorted, it doesn't need
    # to go through the entire process
    swapped = False
    # Traverse through all array elements
    for i in range(n-1):
        # range(n) also work but outer loop will
        # repeat one time more than needed.
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            # if arr[j] > arr[j + 1]:
            if compare(arr[j+1], arr[j]):
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
         
        if not swapped:
            # if we haven't needed to make a single swap, we
            # can just exit the main loop.
            return

def part_2():
    all_packets = list(filter(lambda x: x.strip() != "", input_data))
    all_packets += ["[[2]]", "[[6]]"]
    dprint(all_packets)
    def _mapper(x):
        return eval(x)

    all_packets = list(map(_mapper, all_packets))
    dprint(all_packets)
    bubble_sort(all_packets)

    decoder_key = 1
    for i, f in enumerate(all_packets):
        if f == [[6]] or f == [[2]]:
            decoder_key *= i + 1
    return decoder_key
    

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")