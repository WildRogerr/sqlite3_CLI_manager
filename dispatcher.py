import sys
from typing import List, Callable, Dict

from clistate import CliState, CliStateName
from command import Command, CommandType
from completer import DynamicCompleter
from db import DB, PAGE_SIZE
from format import format_db_rows


class CommandDispatcher:
    db: DB
    completer: DynamicCompleter
    state: CliState
    handlers: Dict[str, Callable]

    def __init__(self, db_path: str):
        self.db = DB(db_path)
        tables = self.db.get_table_names()
        autocomplete_options = {
            'table': set(tables),
            'help': None,
            'exit': None,
        }
        self.completer = DynamicCompleter.from_dict(autocomplete_options)
        self.state = CliState(tables)
        self.handlers = {
            CommandType.TABLE.alias: self.table_handler,
            CommandType.UPDATE.alias: self.update_handler,
            CommandType.LIST.alias: self.list_handler,
            CommandType.NEXT.alias: self.next_handler,
            CommandType.HELP.alias: self.help_handler,
            CommandType.EXIT.alias: self.exit_handler,
        }

    def table_handler(self, args: List[str]):
        # todo remove try/except
        # todo handle invalid command in different states
        try: 
            table_name = args[0]
            columns = self.db.get_column_names(table_name)
            self.state.to_table(table_name, columns)
            completions = {
                'table': set(self.state.tables),
                'list': None,
                'next': None,
                'update': set(self.state.columns),
                'insert': None,
                'delete': None,
                'help': None,
                'exit': None,
            }
            self.completer.update(completions)
            print(f'Table {table_name} choosed.')
        except:
            print('Enter Table Name!')

    def update_handler(self, args: List[str]):
        column = args[0]
        row_id = int(args[1])
        self.state.to_update(column, row_id)
        self.completer.update({})
        print("Input new value:")
    
    def list_handler(self, args: List[str]):
        # todo create custom exception and remove try/except
        try:
            if len(args) == 0:
                self.state.page_number = 1
            else:
                self.state.page_number = int(args[0])
            rows = self.db.list_rows(self.state.table, self.state.page_number)
            table_size = self.db.get_table_size(self.state.table)
            formatted_rows = format_db_rows(self.state.columns,rows,self.state.page_number,table_size)
            print(formatted_rows)
        except:
            print('Enter Table Name!')

    def next_handler(self, args: List[str]):
        next_page = self.state.page_number + 1
        table_size = self.db.get_table_size(self.state.table)
        if next_page*PAGE_SIZE <= table_size:
            self.list_handler([next_page])
        else:
            print('End table.')

    def value_handler(self, value: str):
        if self.state.name == CliStateName.UPDATE:
            self.db.update_table(self.state.table, self.state.column, self.state.row_id, value)
            print("Row updated")
        elif self.state.name == CliStateName.INSERT:
            pass # TODO

        self.table_handler([self.state.table])

    def help_handler(self, _: List[str]):
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

    def exit_handler(self, _: List[str]):
        sys.exit(0)
    # todo validate arguments lengths before calling handlers
    def execute(self, prompt: str):
        if self.state.name == CliStateName.UPDATE:
            self.value_handler(prompt)
        else:
            command = Command.from_prompt(prompt)
            handler = self.handlers[command.command_type.alias]
            handler(command.arguments)
