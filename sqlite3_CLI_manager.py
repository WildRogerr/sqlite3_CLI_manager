import sqlite3
import sys
from sqlite3 import Connection
from prompt_toolkit import PromptSession
from clistate import CliState, CliStateName
from command import Command, CommandType
from completer import DynamicCompleter
from db import get_table_names

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
    state = CliState(tables)
    
    while True:
        try:
            prompt: str = session.prompt('> ')
            command = Command.from_prompt(prompt)
            if command.command_type == CommandType.EXIT:
                break
            handle_command(command, connection, completer, state)
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.

def handle_command(command: Command, connection: Connection, completer: DynamicCompleter, state: CliState):
    if command.command_type == CommandType.TABLE:
        table_name = command.arguments[0]
        cur = connection.cursor()
        cur.execute(f'PRAGMA table_info({table_name})')
        columns = [row[1] for row in cur.fetchall()]
        state.to_table(table_name, columns)
        completions = {
            'table': set(state.tables),
            'list': None,
            'next': None,
            'update': set(state.columns),
            'insert': None,
            'delete': None,
            'help': None,
            'exit': None,
        }
        completer.update(completions)
    elif command.command_type == CommandType.UPDATE:
        state.to_update(command.arguments[0], int(command.arguments[1]))
        completer.update({})
        print('Input new value:')
    elif command.command_type == CommandType.LIST:
        pass
    elif command.command_type == CommandType.HELP:
        print_help()
    elif command.command_type == CommandType.EXIT:
        return

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