import requests
from bs4 import BeautifulSoup

# Make a request to the API
url = "https://rickandmortyapi.com/api/character"
response = requests.get(url)
data = response.json()

# Extract the "results" array
characters = data["results"]

# Create an HTML document with a table
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rick and Morty Characters</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        img {
            max-width: 50px;
            max-height: 50px;
        }
    </style>
</head>
<body>
    <h2>Rick and Morty Characters</h2>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Status</th>
                <th>Species</th>
                <th>Type</th>
                <th>Gender</th>
                <th>Image</th>
            </tr>
        </thead>
        <tbody>
"""

for character in characters:
    html_content += f"""
            <tr>
                <td>{character["id"]}</td>
                <td>{character["name"]}</td>
                <td>{character["status"]}</td>
                <td>{character["species"]}</td>
                <td>{character["type"]}</td>
                <td>{character["gender"]}</td>
                <td><img src="{character["image"]}" alt="{character["name"]}"></td>
            </tr>
"""

html_content += """
        </tbody>
    </table>
</body>
</html>
"""

# Save the HTML content to a file
with open("rick_and_morty_characters.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML file created: rick_and_morty_characters.html")
