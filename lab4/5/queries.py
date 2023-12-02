import os
import sys
import sqlite3
import json

sys.path.append("..")
from json_utils import insert_data

database_name = "db5.db"

with sqlite3.connect(database_name) as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Countries WHERE cpi_country IS NOT '' ORDER BY cpi_country DESC LIMIT 5;")
    result1 = cursor.fetchall()

    cursor.execute(
        "SELECT country, COUNT(*) AS billionaire_count FROM Billionaires GROUP BY country ORDER BY billionaire_count DESC;"
    )
    result2 = cursor.fetchall()

    cursor.execute(
        "SELECT source, AVG(age) AS avg_billionaire_age FROM Billionaires GROUP BY source;"
    )
    result3 = cursor.fetchall()

    cursor.execute(
        "UPDATE Companies SET market_capitalization = 1500000000 WHERE name = 'CompanyXYZ';"
    )
    conn.commit()

    cursor.execute(
        "SELECT * FROM Billionaires WHERE selfMade = 'true' AND industries LIKE '%Technology%' ORDER BY finalWorth DESC;"
    )
    result5 = cursor.fetchall()

    cursor.execute(
        "SELECT SUM(population_country) AS total_population FROM Countries WHERE life_expectancy_country > 70;"
    )
    result6 = cursor.fetchall()

    cursor.execute(
        """
    SELECT B.personName as Name, B.country as Country, C.name AS company_name, C.rank AS company_rank, C.market_capitalization as company_cap
    FROM Billionaires B
    JOIN Companies C ON B.source = C.name;
    """
    )
    result7 = cursor.fetchall()


    os.makedirs("results", exist_ok=True)

    insert_data(os.path.join("results", "order_by_cpi_country.json"), result1)
    insert_data(os.path.join("results", "count_bil_by_country.json"), result2)
    insert_data(os.path.join("results", "avg_age_by_source.json"), result3)
    insert_data(
        os.path.join("results", "selfMade_and_technologies_order_by_worth.json"),
        result5,
    )
    insert_data(os.path.join("results", "popul_life_exp_70.json"), result6)
    insert_data(os.path.join("results", "bill_with_companies.json"), result7)
