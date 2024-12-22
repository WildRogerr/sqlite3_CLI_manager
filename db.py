from sqlite3 import Connection


def get_table_names(connection: Connection):
    cur = connection.cursor()
    cur.execute(f'SELECT name FROM sqlite_master')
    tables = cur.fetchall()
    return [table[0] for table in tables]
