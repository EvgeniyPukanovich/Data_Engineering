from bs4 import BeautifulSoup
import csv

filename = "text_5_var_46"

items = list()

with open(filename, encoding="utf-8") as file:
    lines = file.readlines()
    html = ""
    for line in lines:
        html += line

    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")
    rows = rows[1:]
    for row in rows:
        cells = row.find_all("td")
        item = {
            "company": cells[0].text,
            "contact": cells[1].text,
            "country": cells[2].text,
            "price": cells[3].text,
            "item": cells[4].text
        }
        items.append(item)

with open("r_" + filename, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in items:
        writer.writerow(item.values())
