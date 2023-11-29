import os
import sys
import json
import msgpack
import sqlite3

sys.path.append("..")
from json_utils import insert_data


database_name = os.path.join("..", "database.db")
data_file_path = "task_4_var_46_product_data.msgpack"
update_file_path = "task_4_var_46_update_data.json"


def insert_products(cursor, data):
    cursor.executemany(
        """
        INSERT INTO Products (name, price, quantity, category, fromCity, isAvailable, views, changeCount)
        VALUES(:name, :price, :quantity, :category, :fromCity, :isAvailable, :views, 0)
    """,
        data,
    )


def quantity_sub(cursor, conn, param, product_name):
    try:
        cursor.execute(
            """
            UPDATE Products
            SET quantity = quantity - ?, changeCount = changeCount + 1
            WHERE name = ?
        """,
            (param, product_name),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("exception in quantity_sub")


def quantity_add(cursor, conn, param, product_name):
    try:
        cursor.execute(
            """
            UPDATE Products
            SET quantity = quantity + ?, changeCount = changeCount + 1
            WHERE name = ?
        """,
            (param, product_name),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("exception in quantity_add")


def price_abs(cursor, conn, param, product_name):
    try:
        cursor.execute(
            """
            UPDATE Products
            SET price = price + ?, changeCount = changeCount + 1
            WHERE name = ?
        """,
            (param, product_name),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("exception in price_abs")


def price_percent(cursor, conn, param, product_name):
    try:
        cursor.execute(
            """
            UPDATE Products
            SET price = price * (1 + ? / 100), changeCount = changeCount + 1
            WHERE name = ?
        """,
            (param, product_name),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("exception in price_percent")


def available(cursor, conn, param, product_name):
    try:
        cursor.execute(
            """
            UPDATE Products
            SET isAvailable = ?, changeCount = changeCount + 1
            WHERE name = ?
        """,
            (param, product_name),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("exception in available")


def remove(cursor, conn, param, product_name):
    try:
        cursor.execute(
            """
            DELETE FROM Products
            WHERE name = ?
        """,
            (product_name,),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("exception in remove")


def top_changeCount(cursor):
    cursor.execute(
        """
        SELECT name, changeCount FROM Products
        ORDER BY changeCount DESC
        LIMIT 10
    """
    )
    return cursor.fetchall()


# sum, min, max, avg of price for each group by category
def price_stats(cursor):
    cursor.execute(
        """
        SELECT category, SUM(price), MIN(price), MAX(price), AVG(price)
        FROM Products
        GROUP BY category
    """
    )
    return cursor.fetchall()


# sum, min, max, avg of qunatity for each group by category
def quantity_stats(cursor):
    cursor.execute(
        """
        SELECT category, SUM(quantity), MIN(quantity), MAX(quantity), AVG(quantity)
        FROM Products
        GROUP BY category
    """
    )
    return cursor.fetchall()


def where_price(cursor):
    cursor.execute(
        """
        SELECT * FROM Products
        WHERE price > 100
    """
    )
    return cursor.fetchall()


with open(data_file_path, "rb") as f:
    data = msgpack.load(f)

with open(update_file_path, "r") as f:
    update_data = json.load(f)

with sqlite3.connect(database_name) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "Products" (
            "id"	INTEGER,
            "name"	TEXT,
            "price"	REAL CHECK("price" >= 0),
            "quantity"	INTEGER CHECK("quantity" >= 0),
            "category"	TEXT,
            "fromCity"	TEXT,
            "isAvailable"	INTEGER,
            "views"	INTEGER CHECK("views" >= 0),
            "changeCount"	INTEGER CHECK("changeCount" >= 0),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
    )

    for d in data:
        d["isAvailable"] = 1 if d["isAvailable"] == True else 0
        if "category" not in d:
            d["category"] = "None"

    insert_products(cursor, data)

    for update in update_data:
        product_name = update["name"]
        method = update["method"]
        param = update["param"]
        if method == "quantity_sub":
            quantity_sub(cursor, conn, param, product_name)
        if method == "quantity_add":
            quantity_add(cursor, conn, param, product_name)
        if method == "price_abs":
            price_abs(cursor, conn, param, product_name)
        if method == "price_percent":
            price_percent(cursor, conn, param, product_name)
        if method == "available":
            available(cursor, conn, param, product_name)
        if method == "remove":
            remove(cursor, conn, param, product_name)


    top_cc = [dict(row) for row in top_changeCount(cursor)]
    price_st = [dict(row) for row in price_stats(cursor)]
    quantity_st = [dict(row) for row in quantity_stats(cursor)]
    wh = [dict(row) for row in where_price(cursor)]

    os.makedirs("results", exist_ok=True)

    insert_data(os.path.join("results", "top_changeCount.json"), top_cc)
    insert_data(os.path.join("results", "price_stats.json"), price_st)
    insert_data(os.path.join("results", "quantity_stats.json"), quantity_st)
    insert_data(os.path.join("results", "where_price.json"), wh)

