filename = "text_2_var_46"

with open(filename) as f:
    lines = f.readlines()

res = list()

for l in lines:
    nums = l.split(",")
    sum = 0
    for num in nums:
        sum += int(num)

    res.append(sum)


with open("r_" + filename, "w") as f:
    for w in res:
        f.write(f"{w}\n")