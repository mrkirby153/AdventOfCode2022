import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())


from collections import defaultdict
from aoc_common.io import to_2d_matrix
from aoc_common.benchmark import print_timing

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

input_data = to_2d_matrix(input_data)

dprint(input_data)


height_map = "abcdefghijklmnopqrstuvwxyz"

def get_path_height(key):
    return height_map.index(key)

def can_move_to(from_height, to_height):
    # dprint(f"{from_height} -> {to_height}")
    if from_height == 'S':
        from_height = 'a'
    if from_height == 'E':
        from_height = 'z'
    if to_height == 'E':
        to_height = 'z'
    if to_height == 'S':
        to_height = 'a'
    # dprint(f"{from_height} -> {to_height}")
    from_height = get_path_height(from_height)
    to_height = get_path_height(to_height)


    if from_height < to_height:
        return to_height - from_height == 1
    if from_height >= to_height:
        return True
    return False


def find_neighbors(pos, grid):
    neighbors = []
    x, y = pos

    if y + 1 < len(grid):
        neighbors.append((y+1, x))
    if y - 1 >= 0:
        neighbors.append((y-1, x))
    
    if x + 1 < len(grid[y]):
        neighbors.append((y, x+1))
    
    if x - 1 >= 0:
        neighbors.append((y, x-1))
    return neighbors

def find_valid_neighbors(pos, grid):
    return [(x, y) for y, x in find_neighbors(pos, grid) if can_move_to(grid[pos[1]][pos[0]], grid[y][x])]
        

def find_node(grid, node):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == node:
                return (x, y)
    return None

def find_all_nodes(grid, target_nodes):
    nodes = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in target_nodes:
                nodes.append((x, y))
    return nodes

def print_board(grid, marked_squares=None):
    if marked_squares is None:
        marked_squares = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            color = '\033[92m' if (x, y) in marked_squares else '\033[91m'
            print(f"{color}{grid[y][x]}", end=" ")
        print()
    print('\033[0m') # Reset color

def generate_graph(input_data):
    graph = {}
    for y in range(len(input_data)):
        for x in range(len(input_data[0])):
            point = (x, y)
            graph[point] = find_valid_neighbors(point, input_data)
    return graph

def bfs(graph, start, end):
    dprint(f"BFS FROM {start} -> {end}")
    queue = []
    visited = set()
    visited.add(start)
    queue.append(start)

    size = {(x, y): 0 for x in range(len(input_data[1])) for y in range(len(input_data))}
    dprint(size)

    while queue:
        m = queue.pop(0)
        for neighbor in graph[m]:
            if neighbor not in visited:
                dprint(f"at {m} -- Visting neighbor {neighbor}, {size[neighbor]}, {size[m]}")
                size[neighbor] = size[m] + 1
                visited.add(neighbor)
                queue.append(neighbor)
            if neighbor == end:
                break
    dprint(size)
    return size[end]

@print_timing
def part_1():
    start = find_node(input_data, 'S')
    end = find_node(input_data, 'E')
    graph = generate_graph(input_data)
    dprint(f"Finding path from {start} -> {end}")
    steps = bfs(graph, start, end)
    return steps

@print_timing
def part_2():
    starts = find_all_nodes(input_data, ['S', 'a'])
    end = find_node(input_data, 'E')
    graph = generate_graph(input_data)
    return min(filter(lambda x: x != 0, [bfs(graph, start, end) for start in starts]))

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")