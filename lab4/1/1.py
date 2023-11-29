import csv
import os
import sys

sys.path.append("..")
from database_utils import SQLiteConnection
from json_utils import insert_data


database_name = os.path.join("..", "database.db")
csv_file_path = "task_1_var_46_item.csv"
N = 56


def populate_db(cursor):
    with open(csv_file_path, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")

        rows_to_insert = [
            {
                "id": int(row["id"]),
                "name": row["name"],
                "city": row["city"],
                "begin": row["begin"],
                "system": row["system"],
                "tours_count": int(row["tours_count"]),
                "min_rating": int(row["min_rating"]),
                "time_on_game": int(row["time_on_game"]),
            }
            for row in csv_reader
        ]

        cursor.executemany(
            """
            INSERT INTO Tournaments (id, name, city, begin, system, tours_count, min_rating, time_on_game)
            VALUES (:id, :name, :city, :begin, :system, :tours_count, :min_rating, :time_on_game)
        """,
            rows_to_insert,
        )


def get_frequncies(cursor):
    cursor.execute(
        """
        SELECT city, COUNT(*) AS frequency
        FROM tournaments
        GROUP BY city
    """
    )

    return cursor.fetchall()


def get_first_n_tournaments(cursor):
    cursor.execute(
        """
        SELECT *
        FROM tournaments
        ORDER BY begin
        LIMIT ?
    """,
        (N,),
    )

    return cursor.fetchall()


def min_rating(cursor):
    cursor.execute(
        """
        SELECT MIN(min_rating)
        FROM tournaments
    """
    )

    return cursor.fetchone()


def filter_and_sort(cursor):
    cursor.execute(
        """
        SELECT *
        FROM tournaments
        WHERE system = 'Olympic'
        ORDER BY time_on_game
        LIMIT ?
    """,
        (N,),
    )

    return cursor.fetchall()


with SQLiteConnection(database_name) as cursor:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "Tournaments" (
        "id"	INTEGER,
        "name"	TEXT,
        "city"	TEXT,
        "begin"	TEXT,
        "system"	TEXT,
        "tours_count"	INTEGER,
        "min_rating"	INTEGER,
        "time_on_game"	INTEGER,
        PRIMARY KEY("id")
        );
    """
    )

    #populate_db(cursor)

    first_n = [dict(row) for row in get_first_n_tournaments(cursor)]
    min_r = int(min_rating(cursor)[0])
    freqs = [dict(row) for row in get_frequncies(cursor)]
    filtered_and_sorted = [dict(row) for row in filter_and_sort(cursor)]

    os.makedirs("results", exist_ok=True)

    insert_data(os.path.join("results", "firstN.json"), first_n)
    insert_data(os.path.join("results", "minRating.json"), min_r)
    insert_data(os.path.join("results", "freqs.json"), freqs)
    insert_data(os.path.join("results", "filteredSorted.json"), filtered_and_sorted)
