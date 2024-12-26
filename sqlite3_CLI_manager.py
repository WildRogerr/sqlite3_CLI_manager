import sqlite3
import sys
from sqlite3 import Connection
from prompt_toolkit import PromptSession
from clistate import CliState, CliStateName
from command import Command, CommandType, InvalidCommand, InvalidArguments
from completer import DynamicCompleter
from dispatcher import CommandDispatcher

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

def main(database: str):
    dispatcher = CommandDispatcher(database)
    session = PromptSession(completer=dispatcher.completer)
    # todo handle all custom exception
    while True:
        try:
            prompt: str = session.prompt('> ')
            dispatcher.execute(prompt)
        except KeyboardInterrupt:
            continue  # Control-C pressed. Try again.
        except EOFError:
            break  # Control-D pressed.
        except (InvalidCommand, InvalidArguments) as error:
            print(error)

if __name__ == '__main__':
    db = sys.argv[1]
    main(db)