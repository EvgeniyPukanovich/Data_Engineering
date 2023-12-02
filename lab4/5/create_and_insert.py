import sqlite3
import csv


def create_tables(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Countries (
            country TEXT PRIMARY KEY,
            cpi_country REAL,
            cpi_change_country REAL,
            gdp_country REAL,
            gross_tertiary_education_enrollment REAL,
            gross_primary_education_enrollment_country REAL,
            life_expectancy_country REAL,
            tax_revenue_country_country REAL,
            total_tax_rate_country REAL,
            population_country INTEGER,
            latitude_country REAL,
            longitude_country REAL
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Companies (
            name TEXT PRIMARY KEY,
            rank INTEGER,
            headquarter TEXT,
            ceo TEXT,
            market_capitalization REAL,
            total_employees INTEGER,
            sectors TEXT,
            url TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Billionaires (
            rank INTEGER PRIMARY KEY,
            finalWorth REAL,
            category TEXT,
            personName TEXT,
            age INTEGER,
            country TEXT,
            city TEXT,
            source TEXT,
            industries TEXT,
            countryOfCitizenship TEXT,
            organization TEXT,
            selfMade INTEGER,
            status TEXT,
            gender TEXT,
            birthDate TEXT,
            lastName TEXT,
            firstName TEXT,
            title TEXT,
            date TEXT,
            state TEXT,
            residenceStateRegion TEXT,
            birthYear INTEGER,
            birthMonth INTEGER,
            birthDay INTEGER,
            cpi_country REAL,
            FOREIGN KEY (country) REFERENCES Countries(country),
            FOREIGN KEY (source) REFERENCES Companies(name)
        )
    """
    )


def insert_data(cursor, table_name, data):
    for row in data:
        columns = ", ".join(row.keys())
        placeholders = ", ".join(["?" for _ in row.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        lower = [
            str(item).lower() if isinstance(item, str) else item
            for item in row.values()
        ]
        try:
            cursor.execute(query, tuple(lower))
        except:
            pass

def load_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


database_name = "db5.db"
billionaires_csv_path = "billionaires.csv"

billionaires_data = load_csv(billionaires_csv_path)

with sqlite3.connect(database_name) as conn:
    cursor = conn.cursor()

    create_tables(cursor)

    countries_data = [
        {
            k: v
            for k, v in row.items()
            if k
            in (
                "country",
                "cpi_country",
                "cpi_change_country",
                "gdp_country",
                "gross_tertiary_education_enrollment",
                "gross_primary_education_enrollment_country",
                "life_expectancy_country",
                "tax_revenue_country_country",
                "total_tax_rate_country",
                "population_country",
                "latitude_country",
                "longitude_country",
            )
        }
        for row in billionaires_data
    ]

    billionaires_data = [
        {
            k: v
            for k, v in row.items()
            if k
            not in (
                "cpi_country",
                "cpi_change_country",
                "gdp_country",
                "gross_tertiary_education_enrollment",
                "gross_primary_education_enrollment_country",
                "life_expectancy_country",
                "tax_revenue_country_country",
                "total_tax_rate_country",
                "population_country",
                "latitude_country",
                "longitude_country",
            )
        }
        for row in billionaires_data
    ]

    with open("companies.csv", "r", encoding="utf-8") as c:
        companies_data = csv.DictReader(c, delimiter=",")
        dicts = list()
        for dc in companies_data:
            dc["market_capitalization"] = (
                float(dc["market_capitalization"].split()[0]) * 1_000_000_000
                if dc["market_capitalization"]
                else 0
            )
            dicts.append(dc)
        for dc in dicts:
            insert_data(cursor, "Companies", dicts)
    
    print(billionaires_data)
    insert_data(cursor, "Countries", countries_data)
    insert_data(cursor, "Billionaires", billionaires_data)

    conn.commit()
