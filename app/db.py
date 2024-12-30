import sqlite3
from sqlite3 import Connection
from typing import Final, List, Tuple, Union


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
        primary_key = self.get_primary_key(table_name)[0]
        cur.execute(f'UPDATE {table_name} SET {column} = ? WHERE {primary_key} = ?', (value, row_id))
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
    
    def get_primary_key(self, table_name:str) -> list:
        cur = self.connection.cursor()
        cur.execute(f"PRAGMA table_info('{table_name}')")
        columns_info = cur.fetchall()
        # col[5] indicates if the column is a primary key
        primary_key_info = [col for col in columns_info if col[5] > 0]
        # primary_key_info[0][1] is the column name
        # primary_key_info[0][2] is the column type
        return (primary_key_info[0][1], primary_key_info[0][2])

    def get_not_null_columns_without_default(self, table_name:str) -> list:
        cur = self.connection.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = cur.fetchall()
        not_null_columns = []
        for col in columns:
            col_name = col[1]        # Column name
            not_null = col[3]        # 1, if NOT NULL
            default_value = col[4]   # Default Value
            if not_null == 1 and default_value is None:
                not_null_columns.append(col_name)
        return not_null_columns
    
    def insert_row(self, table_name: str, primary_key_column: Union[str, None], primary_key: Union[str, None]) -> str:
        cur = self.connection.cursor()
        not_null_columns = self.get_not_null_columns_without_default(table_name)
        if primary_key and primary_key_column:
            if len(not_null_columns) == 1 and primary_key_column in not_null_columns:
                cur.execute(f'INSERT INTO {table_name} ({primary_key_column}) VALUES ({primary_key})')
            elif len(not_null_columns) > 1:
                placeholders = ", ".join(["?" for _ in not_null_columns])
                not_null_columns.remove(primary_key_column)
                columns = ", ".join(not_null_columns)
                values = []
                values.append(primary_key)
                values.extend(["0" for _ in not_null_columns])
                query = f"INSERT INTO {table_name} ({primary_key_column}, {columns}) VALUES ({placeholders})"
                cur.execute(query, values)
            else:
                cur.execute(f'INSERT INTO {table_name} ({primary_key_column}) VALUES ({primary_key})')
        else:
            if len(not_null_columns) == 1 and primary_key_column in not_null_columns:
                cur.execute(f'INSERT INTO {table_name} DEFAULT VALUES')
            elif len(not_null_columns) > 1:
                not_null_columns.remove(primary_key_column)
                placeholders = ", ".join(["?" for _ in not_null_columns])
                columns = ", ".join(not_null_columns)
                values = ["0" for _ in not_null_columns]
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cur.execute(query, values)
            else:
                cur.execute(f'INSERT INTO {table_name} DEFAULT VALUES')
        rowid = cur.lastrowid
        self.connection.commit()
        return rowid
    
    def delete_row(self, table_name: str, primary_key_column: str, primary_key: str):
        cur = self.connection.cursor()
        cur.execute(f'DELETE FROM {table_name} WHERE {primary_key_column} = ?', (primary_key,))
        self.connection.commit()

    def get_row_id(self, table_name: str, primary_key_column: str, primary_key: str) -> str:
        cur = self.connection.cursor()
        cur.execute(f'SELECT {primary_key_column} FROM {table_name} WHERE {primary_key_column} = ?',(primary_key,))
        id = cur.fetchone()
        row_id = id[0] if id else None
        return row_id

    def __del__(self):
        self.connection.close()