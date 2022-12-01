#!/bin/sh

[ $# -ne 1 ] && echo "Usage: $0 <day>" && exit 1

mkdir -p $1

cat > $1/$1.py <<EOF
with open('input.txt') as f:
    input_data = list(map(lambda x: x.replace('\n', ''), f.readlines()))

def part_1():
    pass

def part_2():
    pass

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")
EOF
touch $1/input.txt
echo "Done!"