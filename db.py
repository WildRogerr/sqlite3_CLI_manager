import sqlite3
from sqlite3 import Connection
from typing import List, Tuple

class DB:
    connection: Connection

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    def get_table_names(self):
        cur = self.connection.cursor()
        cur.execute(f'SELECT name FROM sqlite_master')
        tables = cur.fetchall()
        return [table[0] for table in tables]

    def get_column_names(self, table_name):
        cur = self.connection.cursor()
        cur.execute(f'PRAGMA table_info({table_name})')
        return [row[1] for row in cur.fetchall()]

    def update_table(self, table_name: str, column: str, row_id: int, value: str):
        cur = self.connection.cursor()
        cur.execute(f'UPDATE {table_name} SET {column} = ? WHERE id = ?', (value, row_id))
        self.connection.commit()

    # to do: page number as argument, limit ofset, stor page_number in sates
    def list_rows(self,table_name:str) -> List[Tuple]:
        cur = self.connection.cursor()
        cur.execute(f'SELECT * FROM {table_name}')
        rows = cur.fetchall()
        return rows
