import sqlite3
import sys
from prompt_toolkit import PromptSession
from clistate import CliState, CliStateName
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



COMPLETIONS = {
    CliStateName.DEFAULT: ['table', 'list', 'help', 'exit'],
    CliStateName.TABLE: ['table', 'list', 'next', 'update', 'insert', 'delete', 'help', 'exit'],
    CliStateName.UPDATE: [],
    CliStateName.INSERT: [],
    CliStateName.EXIT: [],
}

def main(database:str):
    connection = sqlite3.connect(database)
    tables = get_table_names(connection)
    autocomplete_options = {
        'table': set(tables), 
        'help': None, 
        'exit': None, 
    }
    completer = DynamicCompleter.from_dict(autocomplete_options)
    session = PromptSession(completer=completer)
    state = CliState()
    
    while True:
        try:
            text: str = session.prompt('> ')
            handle_prompt(text,connection,completer,state)

            if state.name == CliStateName.EXIT:
                break
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.

def get_table_names(connection):
    cur = connection.cursor()
    cur.execute(f'SELECT name FROM sqlite_master')
    tables = cur.fetchall()
    return [table[0] for table in tables]

def handle_prompt(prompt:str,connection: sqlite3.Connection,completer:DynamicCompleter,state:CliState):
    if prompt.startswith('table '):
        table_name = prompt[6:]
        cur = connection.cursor()
        cur.execute(f'PRAGMA table_info({table_name})')
        columns = [row[1] for row in cur.fetchall()]
        print(columns)
        # completer.update(key='update', values=columns)
        # completer.add(key='')
        state.update(CliStateName.TABLE, table_name)
        completions = {
            'list': None,
            'next': None,
            'update': set(columns),
            'insert': None,
            'delete': None,
        }
        completer.update(completions)
        # 'list': None, 
        # 'next': None,
        # 'insert': None,
        # 'update': set(),
        # 'delete': None,

    if prompt == 'update':
        completer.add(key='table', value='new value')
    
    if prompt == 'add':
        completer.add(key='table', value='new value')

    if prompt == 'clear':
        completer.clear(key='table')

    if prompt == 'help':
        print_help()

    if prompt == 'exit':
        state.name = CliStateName.EXIT

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