import math

filename = "text_3_var_46"

with open(filename) as f:
    lines = f.readlines()

allLines = list()

for l in lines:
    nums = l.strip().split(",")
    res = list()
    for i in range(len(nums)):
        if nums[i] == "NA" or nums[i] == "-1":
            num = float((int(nums[i-1]) + int(nums[i+1]))/2)
            if math.sqrt(num) >= 96:
                res.append(num)
        else:
            num = float(nums[i])
            if math.sqrt(num) >= 96:
                res.append(num)
    allLines.append(res)

with open("r_" + filename, "w") as f:
    for row in allLines:
        for num in row:
            f.write(str(int(num)) + ",")
        f.write("\n")
