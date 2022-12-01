with open('input.txt') as f:
    input_data = list(map(lambda x: x.replace('\n', ''), f.readlines()))

buckets = []

current_bucket = []

for item in input_data:
    if item == '':
        buckets.append(list(current_bucket))
        current_bucket = []
    else:
        current_bucket.append(int(item))
buckets.append(current_bucket)

# print(buckets)

def part_1():
    max_food = 0
    max_id = 0
    for elf, bucket in enumerate(buckets):
        bucket_count = sum(bucket)
        if max_food < bucket_count:
            max_food = bucket_count
            max_id = elf
    return max_id, max_food

def part_1_better():
    sum_buckets = sorted([sum(bucket) for bucket in buckets], reverse=True)
    return sum_buckets[0]

def part_2_better():
    return sum(sorted([sum(bucket) for bucket in buckets], reverse=True)[0:3])

def part_2():
    max_food = [0, 0, 0]
    for bucket in buckets:
        bucket_count = sum(bucket)
        if min(max_food) < bucket_count:
            temp = min(max_food)
            res = [i for i, j in enumerate(max_food) if j == temp]
            max_food[res[0]] = bucket_count

    return sum(max_food)

print(f"Part 1: {part_1()}")
print(f"Part 1 better: {part_1_better()}")
print(f"Part 2: {part_2()}")
print(f"Part 2 better: {part_2_better()}")
