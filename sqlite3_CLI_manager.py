import sqlite3
import sys
from prompt_toolkit import PromptSession
from completer import DynamicCompleter

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
#> help
#> exit

# autocomplete_options = ['table', 'test', 'list', 'next', 'update', 'insert', 'delete', 'help', 'exit']

def main(database:str):
    connection = sqlite3.connect(database)
    cur = connection.cursor()
    cur.execute(f'SELECT name FROM sqlite_master')
    tables = cur.fetchall()
    autocomplete_options = {}
    autocomplete_options["table"] = set()
    for table_tuple in tables:
        autocomplete_options["table"].add(table_tuple[0])
    # completer = NestedCompleter.from_nested_dict(autocomplete_options)
    completer = DynamicCompleter.from_dict(autocomplete_options)
    session = PromptSession(completer=completer)

    while True:
        try:
            text = session.prompt('> ')

            if text == 'add':
                completer.add(key='table', value='new value')

            if text == 'help':
                print_help()

            if text == 'exit':
                break

        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.

def print_help():
    print('table [tablename]')
    print('    Connect to a table')
    print('list [optional page]')
    print('    List all paginated rows in database. Optionally provide a page number.')
    print('next')
    print('    Show next page of rows. Used only after list.')
    print('update [column name] [primary key]')
    print('    Update a single value in a row. Primary key must exist.')
    print('insert [optional id]')
    print('    Insert new row to the table. Optionally provide an id for new row.')
    print('    If table contains NOT NULL columns, wizard will ask you to fill each of them one by one.')
    print('delete [primary key]')
    print('    Delete the row. Primary key must exist')
    print('help')
    print('    Show this help.')
    print('exit')
    print('    Terminate the CLI program.')

if __name__ == '__main__':
    db = sys.argv[1]
    main(db)