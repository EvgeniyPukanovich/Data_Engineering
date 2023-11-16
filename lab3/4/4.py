import xml.etree.ElementTree as ET
import json
from zipfile import ZipFile
from statistics import mean, stdev

zip_file_path = "zip_var_46.zip"

all_data = []

category_freq = dict()

with ZipFile(zip_file_path, "r") as zip_ref:
    file_list = zip_ref.namelist()

    for filename in file_list:
        with zip_ref.open(filename) as file:
            html_content = file.read()

        root = ET.fromstring(html_content)

        clothing_data = []

        for clothing_elem in root.findall(".//clothing"):
            clothing_id = clothing_elem.findtext("id")
            name = clothing_elem.findtext("name")
            category = clothing_elem.findtext("category")
            size = clothing_elem.findtext("size")
            color = clothing_elem.findtext("color")
            material = clothing_elem.findtext("material")
            price_str = clothing_elem.findtext("price")
            rating_str = clothing_elem.findtext("rating")
            reviews_str = clothing_elem.findtext("reviews")
            sporty = clothing_elem.findtext("sporty")

            clothing_id = clothing_id.strip() if clothing_id is not None else None
            name = name.strip() if name is not None else None
            category = category.strip() if category is not None else None
            size = size.strip() if size is not None else None
            color = color.strip() if color is not None else None
            material = material.strip() if material is not None else None
            price = int(price_str) if price_str is not None else None
            rating = float(rating_str) if rating_str is not None else None
            reviews = int(reviews_str) if reviews_str is not None else None
            sporty = sporty.strip() if sporty is not None else None

            if category:
                category_freq[category] = category_freq.get(category, 0) + 1

            data = {
                "id": clothing_id,
                "name": name,
                "category": category,
                "size": size,
                "color": color,
                "material": material,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "sporty": sporty,
            }

            all_data.append(data)


sorted_data = sorted(all_data, key=lambda x: x["rating"])

with open("result_sorted_rating.json", "w") as r_json:
    r_json.write(
        json.dumps(
            sorted_data,
            indent=2,
            ensure_ascii=False,
        )
    )

filtered_data = list(filter(lambda x: x["reviews"] > 200000, sorted_data))

with open("result_filtered_reviews_200000.json", "w") as r_json:
    r_json.write(
        json.dumps(
            filtered_data,
            indent=2,
            ensure_ascii=False,
        )
    )

price_values = [item.get("price", 0) for item in all_data]
price_sum = sum(price_values)
price_min = min(price_values)
price_max = max(price_values)
price_avg = mean(price_values)
price_stdev = stdev(price_values)

price_sats = {
    "price_sum": price_sum,
    "price_min": price_min,
    "price_max": price_max,
    "price_avg": price_avg,
    "price_stdev": price_stdev,
}

with open("price_sats.json", "w") as r_json:
    r_json.write(
        json.dumps(
            price_sats,
            indent=2,
            ensure_ascii=False,
        )
    )

with open("category_freq.json", "w") as r_json:
    r_json.write(
        json.dumps(
            category_freq,
            indent=2,
            ensure_ascii=False,
        )
    )
