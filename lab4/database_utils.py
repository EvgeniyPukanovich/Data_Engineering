import sqlite3


class SQLiteConnection:
    def __init__(self, database_name):
        self.__database_name = database_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.__database_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()
