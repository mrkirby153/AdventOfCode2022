import argparse
import datetime
import os
import shutil
from pytz import timezone

parser = argparse.ArgumentParser(description='Make day script')
parser.add_argument('--year', '-y', help='The year', required=False)
parser.add_argument('--no-input', help='Grab input and puzzle', required=False, action='store_true', default=False)
parser.add_argument('day', help='The day of the puzzle', nargs='?')

args = parser.parse_args()

year = datetime.date.today().year if args.year is None else int(args.year)
if args.day is None:
    # Automatically determining day
    tz = timezone('EST')
    now = datetime.datetime.now(tz)
    day = now.day
    if day > 25:
        print("Could not automatically determine day. Is it after christmas?")
        exit(1)
else:
    day = int(args.day)

print(f"Creating template for {year} day {day}")

day_dir = f"day{day:02d}"

if not os.path.exists(day_dir):
    os.mkdir(day_dir)
    shutil.copy(".scripts/template.py", f"{day_dir}/{day_dir}.py")
else:
    print("Day already exists. Not overwriting...")

if not args.no_input:
    from aocd.models import Puzzle
    print(f"Retrieving puzzle input {year} {day}")
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = puzzle.input_data
    sample_input = puzzle.example_data

    with open(f"{day_dir}/input.txt", "w") as f:
        f.write(puzzle_input)
    with open(f"{day_dir}/sample.txt", "w") as f:
        f.write(sample_input)