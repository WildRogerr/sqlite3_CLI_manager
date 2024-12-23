import sqlite3
from sqlite3 import Connection
from typing import Final, List, Tuple

PAGE_SIZE: Final[int] = 2

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

    def list_rows(self, table_name: str, page_number: int) -> List[Tuple]:
        cur = self.connection.cursor()
        cur.execute(f'SELECT * FROM {table_name} LIMIT {PAGE_SIZE} OFFSET {(page_number-1) * PAGE_SIZE}')
        rows = cur.fetchall()
        return rows
    
    def get_table_size(self, table_name: str) -> int:
        cur = self.connection.cursor()
        cur.execute(f'SELECT COUNT(*) FROM {table_name}')
        row_count = int(cur.fetchone()[0])
        return row_count