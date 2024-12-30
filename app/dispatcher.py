import sys
from typing import List, Callable, Dict
from app.clistate import CliState, CliStateName
from app.command import Command, CommandType
from app.completer import DynamicCompleter
from app.db import DB, PAGE_SIZE
from app.format import format_db_rows
from app.validator import print_error, validate_command


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
            CommandType.INSERT.alias: self.insert_handler,
            CommandType.DELETE.alias: self.delete_handler,
            CommandType.META.alias: self.meta_handler,
            CommandType.HELP.alias: self.help_handler,
            CommandType.EXIT.alias: self.exit_handler,
        }

    def table_handler(self, args: List[str]):
        table_name = args[0]
        columns = self.db.get_column_names(table_name)
        self.state.to_table(table_name, columns)
        completions = {
            'table': set(self.state.tables),
            'list': None,
            'next': None,
            'update': set(self.state.columns),
            'insert': None,
            'meta': None,
            'delete': None,
            'help': None,
            'exit': None,
        }
        self.completer.update(completions)
        primary_key_column = self.db.get_primary_key(self.state.table)[0]
        primary_key_type = self.db.get_primary_key(self.state.table)[1]
        print(f'Connected to table {table_name}.')
        print(f"Primary key column: {primary_key_column}, Data type: {primary_key_type}")

    def update_handler(self, args: List[str]):
        column = args[0]
        row_id = int(args[1])
        self.state.to_update(column, row_id)
        self.completer.update({})
        print("Input new value:")

    def value_handler(self, value: str):
        if self.state.name == CliStateName.UPDATE:
            self.db.update_table(self.state.table, self.state.column, self.state.row_id, value)
            print("Row updated")
        self.table_handler([self.state.table])
    
    def list_handler(self, args: List[str]):
        if len(args) == 0:
            self.state.page_number = 1
        else:
            self.state.page_number = int(args[0])
        rows = self.db.list_rows(self.state.table, self.state.page_number)
        table_size = self.db.get_table_size(self.state.table)
        formatted_rows = format_db_rows(self.state.columns,rows,self.state.page_number,table_size)
        print(formatted_rows)
        
    def next_handler(self, args: List[str]):
        next_page = self.state.page_number + 1
        table_size = self.db.get_table_size(self.state.table)
        if next_page*PAGE_SIZE <= table_size:
            self.list_handler([next_page])
        else:
            print('End table.')

    def insert_handler(self, args: List[str]):
        if len(args) > 0:
            primary_key_column = self.db.get_primary_key(self.state.table)[0]
            row_id_db = self.db.get_row_id(self.state.table, primary_key_column, args[0])
            if f'{row_id_db}' in args:
                print(f"Row {row_id_db} already exists, enter another primary key!")
            else:
                rowid = self.db.insert_row(self.state.table,primary_key_column, args[0])
                print(f'Row inserted. Row id: {rowid}')
        else:
            primary_key_column = self.db.get_primary_key(self.state.table)[0]
            rowid = self.db.insert_row(self.state.table, primary_key_column, None)
            print(f'Row inserted. Row id: {rowid}')

    def delete_handler(self, args: List[str]):
        answer = input('Are you sure? yes/no: ')
        answers = ['yes','no']
        while answer not in answers:
            answer = input('Enter yes/no!: ')
        if answer == 'yes':
            primary_key_column = self.db.get_primary_key(self.state.table)[0]
            row_id = self.db.get_row_id(self.state.table, primary_key_column, args[0])
            if f'{row_id}' in args:
                self.db.delete_row(self.state.table, primary_key_column, args[0])
                print(f"Row deleted")
            else:
                print(f"Enter existed primary key!")
        elif answer == 'no':
            print(f"Row is not deleted")

    def meta_handler(self, args: List[str]):
        primary_key_column = self.db.get_primary_key(self.state.table)[0]
        primary_key_type = self.db.get_primary_key(self.state.table)[1]
        print(f"# Primary key column: {primary_key_column}, Data type: {primary_key_type}")

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
        print('meta')
        print('    Display table metadata, for example primary key column and its type.')
        print('delete [primary key]')
        print('    Delete the row. Primary key must exist')
        print('help')
        print('    Show this help.')
        print('exit')
        print('    Terminate the CLI program.')

    def exit_handler(self, _: List[str]):
        sys.exit(0)
    
    def execute(self, prompt: str):
        if self.state.name == CliStateName.UPDATE:
            self.value_handler(prompt)
        else:
            command = Command.from_prompt(prompt)
            error_code = validate_command(command, self.state)

            if error_code:
                print_error(error_code)
            else:
                handler = self.handlers[command.command_type.alias]
                handler(command.arguments)