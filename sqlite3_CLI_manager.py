import sqlite3
import sys
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter

#> table [tableslist]
#> list [optional_page]

# Optional page number
# -[ RECORD 1 ]------------------------------
# id                  | 1
# name                | Niel
# age                 | 25
# hometown            | Bloemfontein
# favourite dessert   | Malva pudding
# hobbies             | Running, hiking
# -[ RECORD 2 ]------------------------------
# id                  | 2
# name                | Johan van der Merwe
# age                 | 31
# hometown            | Tweebuffelsmeteenskootmorsdoodgeskietfontein
# favourite dessert   | Melktert
# hobbies             | Hunting, fishing
# ... until 10 ...

#> next
#> update "column_name" "primary_key"
#> insert "optional_id"
#> delete "primary_key"
#> exit

sql_completer = WordCompleter(['tables'], ignore_case=True)

def main(database:str):
    connection = sqlite3.connect(database)
    session = PromptSession(completer=sql_completer)
    cur = connection.cursor()
    cur.execute(f'SELECT name FROM sqlite_master')
    table = cur.fetchall()
    print(table)
    
    while True:
        try:
            text = session.prompt('> ')
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.


if __name__ == '__main__':
    db = sys.argv[1]
    main(db)



# class Database():
    
#     def __init__(self):
#         self.conn = sqlite3.connect(self.database_path)
#         self.database_path = input('Enter path to database file: ')
#         self.database_table = input('Enter table name: ')
#         show_table = show_table()
#         print(show_table())

#     def show_table(self):
#         cur = self.conn.cursor()
#         cur.execute(f'SELECT * FROM database_table = ?',(self.database_table))
#         table = cur.fetchall()
#         return table
    
#     def __del__(self):
#         self.conn.close()