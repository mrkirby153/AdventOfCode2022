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
        pos = r, c
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
    for (amount, rotate) in tqdm(instructions):
        dprint("Moving", amount)
        for _ in range(amount):
            point = move_one_step(board, point, facing)
            marked_points[point] = display_heading[facing]
        if rotate:
            dprint("Rotating")
            _turn(rotate)
            marked_points[point] = display_heading[facing]
        
        dprint("At", point)
        dprint("Facing", facing)
        print_board(board, marked_points)

    print_board(board, marked_points)

    dprint("At", point)
    dprint("Facing", facing)

    # 1 indexed strikes again
    row, col = point
    row += 1
    col += 1

    return (1000 * row) + (4 * col) + facing


# Origin: Top left of the cube
# [up/down/left/right]: [0]: side, [1]: clockwise rotations, [2]: face that we land on (1-4), [3]: The offset we care about
cube_data = {
    'A': {
        'origin':   (0, 50),
        'up':       ('F', 1, 4),
        'down':     ('C', 0, 1),
        'left':     ('E', 2, 4),
        'right':    ('B', 0, 4)
    },
    'B': {
        'origin':   (0, 100),
        'up':       ('F', 0, 3),
        'down':     ('C', 1, 2),
        'left':     ('A', 0, 2),
        'right':    ('D', 2, 2)
    },
    'C': {
        'origin':   (50, 50),
        'up':       ('A', 0, 3),
        'down':     ('D', 0, 1),
        'left':     ('E', 3, 1),
        'right':    ('B', 1, 3)
    },
    'D': {
        'origin':   (100, 50),
        'up':       ('C', 0, 3),
        'down':     ('F', 1, 2),
        'left':     ('E', 0, 2),
        'right':    ('B', 2, 2)
    },
    'E': {
        'origin':   (100, 0),
        'up':       ('C', 1, 4),
        'down':     ('F', 0, 1),
        'left':     ('A', 2, 4),
        'right':    ('D', 0, 4)
    },
    'F': {
        'origin':   (150, 0),
        'up':       ('E', 0, 3),
        'down':     ('B', 0, 1),
        'left':     ('A', 3, 1),
        'right':    ('D', 3, 3)
    }
}

def get_face_dimensions(face):
    assert face in cube_data
    data = cube_data[face]
    origin = data['origin']
    return range(origin[0], origin[0] + 50), range(origin[1], origin[1] + 50)

def find_face_for_point(point):
    row, col = point
    for face in cube_data:
        range_row, range_col = get_face_dimensions(face)
        if row in range_row and col in range_col:
            return face
    assert(False)

def resolve(from_point, to_point):
    current_face = find_face_for_point(from_point)
    row_range, col_range = get_face_dimensions(current_face)
    min_row, max_row = row_range.start, row_range.stop - 1
    min_col, max_col = col_range.start, col_range.stop - 1

    new_row, new_col = to_point
    if new_row < min_row:
        return 'up'
    if new_row > max_row:
        return 'down'
    if new_col < min_col:
        return 'left'
    if new_col > max_col:
        return 'right'

def translate_to_local_point(origin, row, col):
    origin_row, origin_col = origin
    return (row - origin_row), (col - origin_col)

def wrap(row, col, dr, dc):
    print("Wrapping at row", row, col, dr, dc)
    if dr == 1: # Down
        if row == 199:
            # Face F
            return (0, 100 + col), (0, 1)
        if row == 149:
            # Face D
            return (150 + col - 50, 49), (0, -1)
        if row == 49:
            # Face B
            return (col - 100 + 50, 99), (0, -1)
    elif dr == -1: # Up
        if row == 100:
            # Face E
            return (50 + col, 50), (0, 1)
        if row == 0:
            if 50 <= col <= 99:
                # Face A
                return (col - 50 + 150, 0), (0, 1)
            if 100 <= col <= 149:
                # Face B
                return (199, col - 100), (-1, 0)
    elif dc == 1: # Right
        if col == 49:
            # Face F
            return (149, 50 + row - 150), (-1, 0)
        if col == 99:
            if 50 <= row <= 99:
                # Face C
                return (49, 100 + row - 50), (-1, 0)
            if 100 <= row <= 149:
                # Face D
                return (49 - (row - 100), 149), (0, -1)
    elif dc == -1: # Left
        if col == 0:
            if 100 <= row <= 149:
                # Face E
                return (0 + row - 100, 50), (0, 1)
            if 150 <= row <= 199:
                # Face F
                return (0, 50 + row - 150), (-1, 0)
        if col == 50:
            if 0 <= row <= 49:
                # Face A
                return (149 - row, 0), (0, 1)
            if 50 <= row <= 99:
                # Face C
                return (100, row - 50), (-1, 0)
    
    assert(False) # Wrapping when not needed

facing_lookup = {
    (1, 0): 3,
    (0, 1): 0,
    (-1, 0): 1,
    (0, -1): 2
}

def part_2():
    assert not parsed_args.sample # Hardcoded map does not work with sample data
    instructions = parse_steps_2(steps)
    # print(instructions)

    row, col = get_start_point(board)
    print("Start", (row, col))

    dr = 0
    dc = -1 # 1

    for step in instructions:
        if isinstance(step, int):
            print("Moving ", step)
            for _ in range(step):
                new_row, new_col = row + dr, col + dc
                print("Considering", (new_row, new_col))
                cell = get(new_row, new_col, board)
                if cell is None:
                    # Wrap
                    (nr, nc), (ndr, ndc) = wrap(row, col, dr, dc)
                    print("Trying to wrap to", (nr, nc))
                    try:
                        (revr, revc), (revdr, revdc) = wrap(nr, nc, -ndr, -ndc)
                        if (revr, revc, -revdr, -revdc) != (row, col, dr, dc):
                            print(row, col, dr, dc)
                            print(nr, nc, -ndr, -ndc)
                            print(revr, revc, -revdr, -revdc)
                            assert(False) # Bad wrap
                    except:
                        assert(False)

                    cell = get(nr, nc, board)
                    if cell == 1:
                        break
                    row, col = new_row, new_col
                    dr, dc = dr, dc
                elif cell == 1:
                    print("hit a wall")
                    break
                row, col = new_row, new_col
        elif step == 'R':
            dr, dc = dc, -dr
        elif step == 'L':
            dc, dr = dr -dc
        break
        # if isinstance(step, int):
        #     for _ in range(step):
        #         new_row, new_col = row + dr, col + dc
        #         cell = get(new_row, new_col, board)
        #         if cell is None:
        #             # Do wrap
        #             (nr, nc), (ndr, ndc) = wrap(new_row, new_col, dr, dc)
        #             cell = get(nr, nc, board)
        #             if cell == 1:
        #                 break # hit a wall
        #             row, col = new_row, new_col
        #             dr, dc = ndr, ndc
        #         elif cell == 1:
        #             break # Hit a wall
        #         row, col = new_row, new_col
        # elif step == 'R':
        #     dr, dc = dc, -dr
        # elif step == 'L':
        #     dc, dr = dr, -dc
    # marked_points = {}
    # point = get_start_point(board)

    # marked_points[point] = display_heading[facing]
    # for (amount, rotate) in tqdm(instructions):
    #     assert get(point[0], point[1], board) != 1 # Ensure we can never start inside of a blocked space

    #     # row, col = point
    #     # delta_row, delta_col = movement_delta[facing]
    #     # for step in range(amount):
    #     #     ahead = get(row + delta_row, col + delta_col, board)
    #     #     if ahead is None:
    #     #         pass
    #     #     else:
    #     #         if ahead == 0:
    #     #             row, col = row + delta_row, col + delta_col
    #     # point = (row, col)


    #     #print("Moving", amount, rotate)
    #     # row, col = point
    #     # delta_row, delta_col = movement_delta[facing]
    #     # for step in range(amount):
    #     #     infront = get(row + delta_row, col + delta_col, board)
    #     #     if infront is None:
    #     #         (new_row, new_col), delta_rotation = wrap(row, col, delta_row, delta_col)
    #     #         target_pos_contents = get(new_row, new_col, board)
    #     #         assert target_pos_contents is not None
    #     #         if get(new_row, new_col, board) == 1: # Blocked
    #     #             continue # Can't move, blocked
    #     #         else:
    #     #             print("Wrapping from ", point, "to", (new_row, new_col))
    #     #             # Can move, step into this place
    #     #             row, col = new_row, new_col
    #     #             facing = (facing + delta_rotation) % 4
                    
    #     #     else:
    #     #         if infront == 1:
    #     #             continue # Can't move, blocked
    #     #         row, col = row + delta_row, col + delta_col
    #     # point = (row, col)
            
    #     # if rotate:
    #     #     #print("Rotating", rotate, facing)
    #     #     facing = (facing + (1 if rotate == 'R' else -1)) % 4
    #     #     #print("Done", facing)
    #     #     marked_points[point] = display_heading[facing]
    
    # print("At", point)
    # print("Facing", facing)
    # print_board(board, marked_points, print_func=print)

    # row += 1
    # col += 1

    # return (1000 * row) + (4 * col) + facing_lookup[dr, dc]



# debug()
# print(f"Part 1: {part_1()}")
# print(f"Part 2: {part_2()}")

print(wrap(0, 50, 0, -1))
print(wrap(149, 0, 0, -1))

#print_board(board, {(3, 70): '%'}, print_func=print)

# 134134 -- too low