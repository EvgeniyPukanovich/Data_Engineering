import xml.etree.ElementTree as ET
import json
from zipfile import ZipFile
from statistics import mean, stdev

zip_file_path = "zip_var_46.zip"

all_data = []

constellation_freq = dict()

with ZipFile(zip_file_path, "r") as zip_ref:
    file_list = zip_ref.namelist()

    for filename in file_list:
        with zip_ref.open(filename) as file:
            html_content = file.read()

        root = ET.fromstring(html_content)

        name = root.find("name").text.strip()
        constellation = root.find("constellation").text.strip()
        spectral_class = root.find("spectral-class").text.strip()
        radius = int(root.find("radius").text.strip())
        rotation = float(root.find("rotation").text.split()[0])
        age = float(root.find("age").text.split()[0])
        distance = float(root.find("distance").text.split()[0])
        absolute_magnitude = float(root.find("absolute-magnitude").text.split()[0])

        data = {
            "name": name,
            "constellation": constellation,
            "spectral_class": spectral_class,
            "radius": radius,
            "rotation": rotation,
            "age": age,
            "distance": distance,
            "absolute_magnitude": absolute_magnitude,
        }

        if constellation != "":
            constellation_freq[constellation] = constellation_freq.get(constellation, 0) + 1

        all_data.append(data)


sorted_data = sorted(all_data, key=lambda x: x["age"])

with open("result_sorted_age.json", "w") as r_json:
    r_json.write(
        json.dumps(
            sorted_data,
            indent=2,
            ensure_ascii=False,
        )
    )

filtered_data = list(filter(lambda x: x["constellation"] == "Телец", sorted_data))

with open("result_filtered_Telec.json", "w") as r_json:
    r_json.write(
        json.dumps(
            filtered_data,
            indent=2,
            ensure_ascii=False,
        )
    )

radius_values = [item["radius"] for item in all_data]
radius_sum = sum(radius_values)
radius_min = min(radius_values)
radius_max = max(radius_values)
radius_avg = mean(radius_values)
radius_stdev = stdev(radius_values)

stats_data = {
    "radius_sum": radius_sum,
    "radius_min": radius_min,
    "radius_max": radius_max,
    "radius_avg": radius_avg,
    "radius_stdev": radius_stdev,
}


with open("radius_sats.json", "w") as r_json:
    r_json.write(
        json.dumps(
            stats_data,
            indent=2,
            ensure_ascii=False,
        )
    )

with open("constellation_freq.json", "w") as r_json:
    r_json.write(
        json.dumps(
            constellation_freq,
            indent=2,
            ensure_ascii=False,
        )
    )