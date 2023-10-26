import csv

filename = "text_4_var_46"
age = 25 + (46 % 10)

average_salary = 0
items = list()

with open(filename, newline="\n", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        item = {
            "number": int(row[0]),
            "name": row[2] + ' ' + row[1],
            "age": int(row[3]),
            "salary": int(row[4][0:-1])
        }

        average_salary += item["salary"]
        items.append(item)

average_salary /= len(items)

filtered = filter(lambda item: item["salary"] > average_salary and item["age"] > age, items)

sorted = sorted(filtered, key=lambda item: item["number"])

for item in sorted:
    item["salary"] = str(item["salary"]) + "₽"

with open("r_" + filename, 'w', encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in sorted:
        writer.writerow(item.values())
