import argparse
from pathlib import Path
import sys

# Add aoc_common to the python path
file = Path(__file__)
root = file.parent.parent
sys.path.append(root.as_posix())

import re
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

board = {}

steps = None

for r, row in enumerate(input_data):

    if len(row) > 0 and row[0] not in [' ', '.', '#']:
        steps = row
        continue # Instruction line

    for c, col in enumerate(row):
        pos = r + 1, c + 1
        if col == ' ':
            continue
        board[pos] = 1 if col == '#' else 0

assert steps

def get(row, col, board):
    pos = row, col
    return board[pos] if pos in board else None

def dimensions(board):
    max_row = max(map(lambda x: x[0], board.keys()))
    max_col = max(map(lambda x: x[1], board.keys()))
    return range(max_row+1), range(max_col+1)

def print_board(board, marked_points=None, print_func=dprint):
    max_row = max(map(lambda x: x[0], board.keys()))
    max_col = max(map(lambda x: x[1], board.keys()))
    dprint("Max Row:", max_row)
    dprint("Max Col:", max_col)

    board_str = ""
    for row in range(max_row+1):
        row_str = ""
        for col in range(max_col+1):
            val = get(row, col, board)
            if (row, col) in marked_points:
                row_str += marked_points[row, col]
            else:
                if val is None:
                    row_str += " "
                else:
                    row_str += "." if val == 0 else "#"
        board_str += f"{row_str}\n"
    print_func(board_str)

STEP_RE = re.compile("(\d+)([RL])?")
def parse_steps(steps):
    s = []
    for match in STEP_RE.findall(steps):
        amount, turn = match
        turn = turn if turn else None
        s.append((int(amount), turn))
    return s

def parse_steps_2(s):
    steps = []
    last = ''
    for c in s:
        if c in 'LR':
            if last != '':
                steps.append(int(last))
                last = ''
            steps.append(c)
        else:
            last += c
    if last != '':
        steps.append(int(last))
    return steps

def get_start_point(board):
    row_dimensions, col_dimensions = dimensions(board)
    for row in row_dimensions:
        for col in col_dimensions:
            if get(row, col, board) == 0:
                return row, col
    return None

movement_delta = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0)
}

def move_one_step(board, pos, facing):
    row, col = pos
    d_r, d_c = dimensions(board)

    delta_row, delta_col = movement_delta[facing]
    row += delta_row
    col += delta_col

    at_pos = get(row, col, board)

    if at_pos is None:
        dprint("Wraparound")
        # Wrap around
        lookback_delta = {
            0: (0, -1),
            1: (-1, 0),
            2: (0, 1),
            3: (1, 0)
        }
        new_row, new_col = pos
        dr, dc = lookback_delta[facing]
        while new_row in d_r and new_col in d_c:
            a = get(new_row, new_col, board)
            if a is None:
                break
            new_row += dr
            new_col += dc
        new_point = (new_row-dr, new_col-dc)
        if get(new_point[0], new_point[1], board) == 1:
            return pos
        return new_point

    if at_pos == 1:
        return pos # Cannot move
    else:
        return (row, col)

display_heading = {
    0: '>',
    1: 'v',
    2: '<',
    3: '^'
}

def part_1():
    facing = 0 # 0 = >, 1 = V, 2 = <, 3 = ^
    def _turn(direction):
        nonlocal facing
        assert direction in ['L', 'R']

        if direction == 'L':
            facing -= 1
            if facing == -1:
                facing = 3
        if direction == 'R':
            facing += 1
            if facing == 4:
                facing = 0
    
    instructions = parse_steps(steps)
    marked_points = {}
    point = get_start_point(board)
    
    marked_points[point] = display_heading[facing]
    for (amount, rotate) in tqdm(instructions, "Part 1"):
        dprint("Moving", amount)
        for _ in range(amount):
            point = move_one_step(board, point, facing)
            marked_points[point] = display_heading[facing]
        if rotate:
            _turn(rotate)
            marked_points[point] = display_heading[facing]

    print_board(board, marked_points)

    dprint("At", point)
    dprint("Facing", facing)

    row, col = point
    return (1000 * row) + (4 * col) + facing

def wrap(col, row, dc, dr):
    if dc == 1:
        # Right
        if col == 150:
            return 100, 151-row, -1, 0
        if col == 100:
            if 51 <= row <= 100:
                return 100 + (row - 50), 50, 0, -1
            if 101 <= row <= 150:
                return 150, 51 - (row - 100), -1, 0
        if col == 50:
            return 50 + (row - 150), 150, 0, -1
    elif dc == -1:
        # Left
        if col == 51:
            if 1 <= row <= 50:
                return 1, 151 - row, 1, 0
            if 51 <= row <= 100:
                return row - 50, 101, 0, 1
        if col == 1:
            if 101 <= row <= 150:
                return 51, 1 + (150 - row), 1, 0
            if 151 <= row <= 200:
                return row - 150 + 50, 1, 0, 1
    elif dr == 1:
        # Down
        if row == 50:
            return 100, col - 50, -1, 0
        if row == 150:
            return 50, col + 100, -1, 0
        if row == 200:
            return col + 100, 1, 0, 1
    elif dr == -1:
        # Up
        if row == 1:
            if 51 <= col <= 100:
                return 1, col+100, 1, 0
            if 101 <= col <= 150:
                return col-100, 200, 0, -1
        if row == 101:
            return 51, col+50, 1, 0
    assert(False)

facing_val = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
}

def part_2():
    assert not parsed_args.sample # Hardcoded map does not work with sample data
    instructions = parse_steps_2(steps)
    # print(instructions)

    row, col = get_start_point(board)
    print("Start", (col, row))
    dc = 1
    dr = 0

    for step in instructions:
        if isinstance(step, int):
            for _ in range(step):
                nc, nr = col+dc, row+dr
                cell = get(nr, nc, board)
                if cell is None:
                    nc, nr, ndc, ndr = wrap(col, row, dc, dr)
                    cell = get(nr, nc, board)
                    if cell == 1:
                        break # Hit a wall, don't mess with direction
                    col, row = nc, nr
                    dc, dr = ndc, ndr
                elif cell == 1:
                    break # Hit a wall!
                col, row = nc, nr
        elif step == 'R':
            dr, dc = dc, -dr
        elif step == 'L':
            dc, dr = dr, -dc
        else:
            assert(False)
    
    return 1000 * row + 4 * col + facing_val[dc,dr]

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")