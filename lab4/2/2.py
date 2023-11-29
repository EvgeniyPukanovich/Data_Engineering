import pickle
import os
import sys

sys.path.append("..")
from database_utils import SQLiteConnection
from json_utils import insert_data

database_name = os.path.join("..", "database.db")
data_file_path = "task_2_var_46_subitem.pkl"


def insert_prizes(cursor):
    with open(data_file_path, "rb") as f:
        prizes = pickle.load(f)

    cursor.execute("SELECT id, name FROM tournaments")
    tournament_data = cursor.fetchall()

    tournament_name_to_id = {row["name"]: row["id"] for row in tournament_data}

    for prize in prizes:
        tournament_name = prize["name"]
        tournament_id = tournament_name_to_id.get(tournament_name)

        if tournament_id is not None:
            cursor.execute(
                """
                INSERT INTO Prizes (tournament_id, place, prize)
                VALUES (?, ?, ?)
            """,
                (tournament_id, prize["place"], prize["prise"]),
            )


def get_all_rows(cursor):
    cursor.execute(
        """
        SELECT Tournaments.name, Prizes.place, Prizes.prize
        FROM Tournaments
        JOIN Prizes ON Tournaments.id = Prizes.tournament_id
		ORDER BY name, place
    """
    )
    return cursor.fetchall()


def get_rows_where(cursor):
    cursor.execute(
        """
        SELECT Tournaments.name, Tournaments.min_rating, Prizes.place, Prizes.prize
        FROM Tournaments
        JOIN Prizes ON Tournaments.id = Prizes.tournament_id
        WHERE Tournaments.min_rating > 2400
		ORDER BY name, place
    """
    )
    return cursor.fetchall()


def get_avg_prize(cursor):
    cursor.execute(
        """
        SELECT Tournaments.city, AVG(Prizes.prize) AS avg_prize
        FROM Tournaments
        JOIN Prizes ON Tournaments.id = Prizes.tournament_id
        GROUP BY Tournaments.city
    """
    )
    return cursor.fetchall()


with SQLiteConnection(database_name) as cursor:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "Prizes" (
            "id"	INTEGER,
            "tournament_id"	INTEGER,
            "place"	INTEGER,
            "prize"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT),
            FOREIGN KEY("tournament_id") REFERENCES "tournaments"("id")
        );
    """
    )

    # insert_prizes(cursor)

    all_rows = [dict(row) for row in get_all_rows(cursor)]
    rows_where = [dict(row) for row in get_rows_where(cursor)]
    avg_prize = [dict(row) for row in get_avg_prize(cursor)]

    os.makedirs("results", exist_ok=True)

    insert_data(os.path.join("results", "all_rows.json"), all_rows)
    insert_data(os.path.join("results", "rows_where.json"), rows_where)
    insert_data(os.path.join("results", "avg_prize.json"), avg_prize)
