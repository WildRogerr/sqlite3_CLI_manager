import sqlite3
import sys
from prompt_toolkit import PromptSession
from app.command import InvalidCommand, InvalidArguments
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
    try:
        db = sys.argv[1]
        main(db)
    except IndexError:
        print('Enter "database_path"!')