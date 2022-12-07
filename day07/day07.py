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


def dprint(*args, **kwargs):
    if parsed_args.sample:
        print(*args, **kwargs)


class DirectoryNode:

    def __init__(self, path, size=None) -> None:
        self.path = path
        self.children = {}
        self.parent = None
        self.size = size

    def add_child(self, path, size):
        node = DirectoryNode(path, size)
        node.parent = self
        self.children[path] = node
        return node
    
    def get_child(self, path):
        if path == "..":
            return self.parent
        else:
            return self.children[path]
    
    def is_file(self):
        return self.size is not None

    def get_all_files_rec(self):
        files = []
        def _get(node):
            if node.is_file():
                files.append((node.path, node.size))
            else:
                for n in [x for x in node.children.values()]:
                    _get(n)
        _get(self)
        return files
    
    def sum_of_files(self):
        return sum([int(x[1]) for x in self.get_all_files_rec()])

    def __repr__(self) -> str:
        return f"{'dir ' if not self.is_file() else ''}{self.path}"



if parsed_args.sample:
    print("Using sample data!")


with open('input.txt' if not parsed_args.sample else 'sample.txt') as f:
    input_data = list(map(lambda x: x.replace('\n', ''), f.readlines()))

dprint(input_data)

directory_tree = DirectoryNode("/")

# Drop the first line cos we're assuming we're in /

current_node = directory_tree


for line in input_data[1:]:
    dprint(f"Processing line {line}")
    if line.startswith("$"):
        command = line[2:].split(" ")
        dprint(f"Processing command {command}")
        if command[0] == "cd":
            dprint(f"Moving into directory {command[1]}")
            current_node = current_node.get_child(command[1])
            dprint(f"New node: {current_node}")
    else:
        # This is output from ls
        size, filename = line.split(" ")
        if size == "dir":
            dprint(f"Directory {filename}")
            current_node.add_child(filename, None)
        else:
            dprint(f"File of size {size}, adding to directory {current_node.path}")
            current_node.add_child(filename, size)

def print_directory_tree(directory: DirectoryNode, depth=0):
    display = f'(file, size={directory.size})' if directory.is_file() else f'(dir, size {directory.sum_of_files()})'
    dprint(f"{'  '*(depth)} {directory.path} {display}")
    for child in directory.children.values():
        print_directory_tree(child, depth+1)

print_directory_tree(directory_tree)

def part_1():
    candidates = []
    def _walk(node: DirectoryNode):
        if not node.is_file():
            dir_size = node.sum_of_files()
            dprint(f"Node {node.path} has a size of {dir_size}")
            if dir_size < 100000:
                candidates.append((node.path, dir_size))
        for child in node.children.values():
            _walk(child)
    _walk(directory_tree)
    dprint(candidates)

    return sum([size for _path, size in candidates])

def part_2():
    TOTAL_DISK_SIZE = 70000000
    UNUSED_SPACE_REQUIRED = 30000000

    current_free_space = TOTAL_DISK_SIZE - directory_tree.sum_of_files()
    dprint(f"Current free space: {current_free_space}")

    space_to_free = UNUSED_SPACE_REQUIRED - current_free_space
    dprint(f"Space needed: {space_to_free}")
    candidates = []
    def _walk(node: DirectoryNode):
        if not node.is_file():
            dir_size = node.sum_of_files()
            dprint(f"Node {node.path} has a size of {dir_size}")
            if dir_size >= space_to_free:
                candidates.append((node.path, dir_size))
        for child in node.children.values():
            _walk(child)
    _walk(directory_tree)
    dprint(candidates)

    return min([size for _path, size in candidates])


print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")