import json
from bs4 import BeautifulSoup
from statistics import mean, stdev
import os
import re

file_path = "court.html"

data_list = list()

judge_freq = dict()

def clean_string(input_string):
    cleaned_string = input_string.replace('\n', ' ')
    cleaned_string = re.sub(r'\s+', ' ', cleaned_string).strip()
    return cleaned_string

with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

table = soup.find(id="tablcont")

columns = [header.text.strip() for header in table.find("tr").find_all("td")]

rows = table.find_all("tr")[1:]

for row in rows:
    data = {}
    columns_data = row.find_all("td")

    if len(columns_data) == len(columns):
        for i in range(len(columns)):
            text = clean_string(columns_data[i].text.strip())
            data[columns[i]] = text

            if columns[i] == "Судья" and text != "":
                judge_freq[text] = judge_freq.get(text, 0) + 1

        data_list.append(data)

sorted_pp = sorted(data_list, key=lambda x: float(x["№ п/п"]))

filtered_time = list(
    filter(lambda x: int(x["Время слушания"].split(":")[0]) > 12, sorted_pp)
)

with open("result_sorted_pp.json", "w") as r_json:
    r_json.write(
        json.dumps(
            sorted_pp,
            indent=2,
            ensure_ascii=False,
        )
    )

with open("result_filtered_time12.json", "w") as r_json:
    r_json.write(
        json.dumps(
            filtered_time,
            indent=2,
            ensure_ascii=False,
        )
    )

time_values = [int(time["Время слушания"].split(":")[0]) for time in data_list]
time_sum = sum(time_values)
time_min = min(time_values)
time_max = max(time_values)
time_avg = mean(time_values)
time_stdev = stdev(time_values)

time_stats = {
    "sum": time_sum,
    "min": time_min,
    "max": time_max,
    "avg": time_avg,
    "stdev": time_stdev,
}

with open("time_stats.json", "w") as r_json:
    r_json.write(
        json.dumps(
            time_stats,
            indent=2,
            ensure_ascii=False,
        )
    )


with open("judge_freq.json", "w") as r_json:
    r_json.write(
        json.dumps(
            judge_freq,
            indent=2,
            ensure_ascii=False,
        )
    )

directory_path = "pages"

dicts = list()

for foldername, subfolders, filenames in os.walk(directory_path):
    for filename in filenames:
        with open(directory_path + "/" + filename, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")
        # Find the div with id 'cont1'
        div_cont1 = soup.find("div", {"id": "cont1"})

        # Find the table within the div
        table = div_cont1.find("table", {"id": "tablcont"})

        # Initialize an empty dictionary to store the scraped data
        data_dict = {}

        # Iterate through rows in the table
        for row in table.find_all("tr"):
            # Find all cells in the row
            cells = row.find_all("td")

            # Check if the row contains 2 cells
            if len(cells) == 2:
                # Extract key and value from the cells
                key = cells[0].text.strip()
                value = cells[1].text.strip()

                # Add key-value pair to the dictionary
                data_dict[key] = value

        dicts.append(data_dict)

with open("pages_data.json", "w") as r_json:
    r_json.write(
        json.dumps(
            dicts,
            indent=2,
            ensure_ascii=False,
        )
    )
