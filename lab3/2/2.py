import json
import zipfile
import sys
from bs4 import BeautifulSoup
import re

# Путь к вашему ZIP-архиву
zip_file_path = "zip_var_46.zip"

data = list()

acc_max = 0
acc_min = sys.maxsize
acc_non_empty = 0
acc_sum = 0

matrix_freq = dict()


def handle_int_value(
    value: float, max: float, min: float, non_empty: float, sum: float
):
    if value >= 0:
        non_empty += 1
        sum += value
        if value > max:
            max = value
        if value < min:
            min = value
    return max, min, non_empty, sum


with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    file_list = zip_ref.namelist()

    for filename in file_list:
        with zip_ref.open(filename) as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        for product_div in soup.find_all("div", class_="pad"):
            product_data = {}

            # Extract data-id
            product_data["data_id"] = product_div.find("a", class_="add-to-favorite")[
                "data-id"
            ]

            # Extract name
            product_data["name"] = product_div.find("span").get_text(strip=True)

            # Extract price
            product_data["price"] = int(
                product_div.find("price").get_text(strip=True).replace(" ", "")[:-1]
            )

            # Extract bonus
            bonus_strong = product_div.find("strong")
            product_data["bonus"] = int(bonus_strong.get_text(strip=True).split()[2])

            # Extract data from ul
            ul_data = {}
            ul = product_div.find("ul")
            if ul:
                for li in ul.find_all("li"):
                    type_name = li["type"]
                    text = li.get_text(strip=True)
                    if (
                        type_name == "sim"
                        or type_name == "ram"
                        or type_name == "camera"
                        or type_name == "acc"
                    ):
                        match = re.match(r"\d+", text)

                        if match:
                            extracted_number = int(match.group())
                            ul_data[type_name] = extracted_number

                            if type_name == "acc":
                                (
                                    acc_max,
                                    acc_min,
                                    acc_non_empty,
                                    acc_sum,
                                ) = handle_int_value(
                                    extracted_number,
                                    acc_max,
                                    acc_min,
                                    acc_non_empty,
                                    acc_sum,
                                )
                    elif type_name == "matrix" and text != "":
                        matrix_freq[text] = matrix_freq.get(text, 0) + 1
                    else:
                        ul_data[type_name] = li.get_text(strip=True)

            product_data.update(ul_data)

            data.append(product_data)

sorted_price = sorted(data, key=lambda x: x["price"])

with open("result_sorted_price.json", "w") as r_json:
    r_json.write(
        json.dumps(
            sorted_price,
            indent=2,
            ensure_ascii=False,
        )
    )

filtered_bonus = list(filter(lambda x: x["bonus"] > 1000, sorted_price))

with open("result_filtered_bonus1000.json", "w") as r_json:
    r_json.write(
        json.dumps(
            filtered_bonus,
            indent=2,
            ensure_ascii=False,
        )
    )

avr = acc_sum / acc_non_empty

s = 0

for d in data:
    if "acc" in d:
        s += (d["acc"] - avr) ** 2

dev = (s / acc_non_empty) ** 0.5

with open("acc_stats.json", "w") as r_json:
    r_json.write(
        json.dumps(
            {
                "sum": acc_sum,
                "min": acc_min,
                "max": acc_max,
                "average": avr,
                "deviation": dev,
            },
            indent=2,
        )
    )

matrix_sorted = dict(sorted(matrix_freq.items(), key=lambda x: x[1], reverse=True))

with open("matrix_freq.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(matrix_sorted, ensure_ascii=False, indent=2))
