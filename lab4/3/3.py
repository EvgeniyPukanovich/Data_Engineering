import os
import sys
import pickle

sys.path.append("..")
from database_utils import SQLiteConnection
from json_utils import insert_data

database_name = os.path.join("..", "database.db")
data_file_path_1 = "task_3_var_46_part_1.pkl"
data_file_path_2 = "task_3_var_46_part_2.text"

N = 56


def insert_songs(cursor, data):
    cursor.executemany(
        """
        INSERT INTO Songs (artist, song, duration_ms, year, tempo, genre)
        VALUES (:artist, :song, :duration_ms, :year, :tempo, :genre)
    """,
        data,
    )

def get_frequncies(cursor):
    cursor.execute(
        """
        SELECT artist, COUNT(*) AS frequency
        FROM Songs
        GROUP BY artist
    """
    )

    return cursor.fetchall()


def get_first_n(cursor):
    cursor.execute(
        """
        SELECT *
        FROM Songs
        ORDER BY duration_ms
        LIMIT ?
    """,
        (N,),
    )

    return cursor.fetchall()


def min_rating(cursor):
    cursor.execute(
        """
        SELECT MIN(year)
        FROM Songs
    """
    )

    return cursor.fetchone()


def filter_and_sort(cursor):
    cursor.execute(
        """
        SELECT *
        FROM Songs
        WHERE genre = 'rock'
        ORDER BY year
        LIMIT ?
    """,
        (61,),
    )

    return cursor.fetchall()

columns = ["artist", "song", "duration_ms", "year", "tempo", "genre"]
data = list()

with open(data_file_path_2, "r", encoding="utf-8") as txt_file:
    song_data = {}
    for line in txt_file:
        if line.strip() == "=====":
            song_data["duration_ms"] = int(song_data["duration_ms"])
            song_data["year"] = int(song_data["year"])
            song_data["tempo"] = float(song_data["tempo"])
            data.append(song_data)
            song_data = {}
        else:
            key, value = line.strip().split("::")
            if key in columns:
                song_data[key] = value

with open(data_file_path_1, "rb") as f:
    songs = pickle.load(f)

    for row in songs:
        song_data = {
            "artist": row["artist"],
            "song": row["song"],
            "duration_ms": int(row["duration_ms"]),
            "year": int(row["year"]),
            "tempo": float(row["tempo"]),
            "genre": row["genre"],
        }
        data.append(song_data)

with SQLiteConnection(database_name) as cursor:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "Songs" (
            "id"	INTEGER,
            "artist"	TEXT,
            "song"	TEXT,
            "duration_ms"	INTEGER,
            "year"	INTEGER,
            "tempo"	REAL,
            "genre"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
    )

    # insert_songs(cursor, data)

    first_n = [dict(row) for row in get_first_n(cursor)]
    min_r = int(min_rating(cursor)[0])
    freqs = [dict(row) for row in get_frequncies(cursor)]
    filtered_and_sorted = [dict(row) for row in filter_and_sort(cursor)]

    os.makedirs("results", exist_ok=True)

    insert_data(os.path.join("results", "firstN.json"), first_n)
    insert_data(os.path.join("results", "minYear.json"), min_r)
    insert_data(os.path.join("results", "freqs.json"), freqs)
    insert_data(os.path.join("results", "filteredSorted.json"), filtered_and_sorted)

