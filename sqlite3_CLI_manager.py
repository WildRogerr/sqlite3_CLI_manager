import sqlite3
import sys
from sqlite3 import Connection
from prompt_toolkit import PromptSession
from app.clistate import CliState, CliStateName
from app.command import Command, CommandType, InvalidCommand, InvalidArguments
from app.completer import DynamicCompleter
from app.dispatcher import CommandDispatcher

#Program structure:
#> table [tableslist]
#> list [optional_page]
#> next
#> update "column_name" "primary_key"
#> insert "optional_id"
#> delete "primary_key"
#> help
#> exit

def main(database: str):
    dispatcher = CommandDispatcher(database)
    session = PromptSession(completer=dispatcher.completer)
    while True:
        try:
            prompt: str = session.prompt('> ')
            dispatcher.execute(prompt)
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.
        except (InvalidCommand, InvalidArguments, sqlite3.Error) as error:
            print(error)

if __name__ == '__main__':
    db = sys.argv[1]
    main(db)