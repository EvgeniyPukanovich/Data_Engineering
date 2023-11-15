import json
import zipfile
import sys
from bs4 import BeautifulSoup

zip_file_path = "zip_var_46.zip"

data = list()

rating_max = 0
rating_min = sys.maxsize
rating_non_empty = 0
rating_sum = 0

category_freq = dict()


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

        category = (
            soup.find("div", class_="book-wrapper")
            .find_all_next("div")[0]
            .find_next("span")
            .get_text(strip=True)
            .split(":")[1]
            .strip()
        )

        if category != "":
            category_freq[category] = category_freq.get(category, 0) + 1

        book_title = soup.find("h1", class_="book-title").get_text(strip=True)
        author = soup.find("p", class_="author-p").get_text(strip=True)
        pages = int(soup.find("span", class_="pages").get_text(strip=True).split()[1])
        year = int(soup.find("span", class_="year").get_text(strip=True).split()[-1])

        isbn = (
            soup.find("div", class_="book-wrapper")
            .find_all_next("div")[2]
            .find_all_next("span")[2]
            .get_text(strip=True)
            .split(":")[1]
            .strip()
        )

        description = (
            soup.find("div", class_="book-wrapper")
            .find_all_next("div")[2]
            .find_next("p")
            .get_text(strip=True)
            .split("Описание", 1)[1]
            .strip()
        )

        img_src = soup.find("img")["src"]

        rating = float(
            soup.find("div", class_="book-wrapper")
            .find_all_next("div")[4]
            .find_all_next("span")[0]
            .get_text(strip=True)
            .split(":")[1]
            .strip()
        )

        rating_max, rating_min, rating_non_empty, rating_sum = handle_int_value(
            rating, rating_max, rating_min, rating_non_empty, rating_sum
        )

        views = int(
            soup.find("div", class_="book-wrapper")
            .find_all_next("div")[4]
            .find_all_next("span")[1]
            .get_text(strip=True)
            .split(":")[1]
            .strip()
        )

        book_data = {
            "category": category,
            "title": book_title,
            "author": author,
            "pages": pages,
            "year": year,
            "isbn": isbn,
            "description": description,
            "img_src": img_src,
            "rating": rating,
            "views": views,
        }

        data.append(book_data)


print(data)

sorted_rating = sorted(data, key=lambda x: x["year"])

filtered_pages = list(filter(lambda x: x["pages"] > 400, sorted_rating))

with open("result_sorted_year.json", "w") as r_json:
    r_json.write(
        json.dumps(
            sorted_rating,
            indent=2,
            ensure_ascii=False,
        )
    )

with open("result_filtered_pages400.json", "w") as r_json:
    r_json.write(
        json.dumps(
            filtered_pages,
            indent=2,
            ensure_ascii=False,
        )
    )

avr = rating_sum / rating_non_empty

s = 0

for d in data:
    if d["rating"] >= 0:
        s += (d["rating"] - avr) ** 2

dev = (s / rating_non_empty) ** 0.5

with open("rating_stats.json", "w") as r_json:
    r_json.write(
        json.dumps(
            {
                "sum": rating_sum,
                "min": rating_min,
                "max": rating_max,
                "average": avr,
                "deviation": dev,
            },
            indent=2,
        )
    )

freq_sorted = dict(sorted(category_freq.items(), key=lambda x: x[1], reverse=True))

with open("category_freq.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
