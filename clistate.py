
from enum import Enum
from typing import List


class InvalidStateTransition(Exception):
    pass

class CliStateName(Enum):
    DEFAULT = 1
    TABLE = 2
    UPDATE = 3
    INSERT = 4

class CliState:
    name = CliStateName.DEFAULT
    table: str
    tables: List[str]
    column: str
    columns: List[str]
    row_id: int

    def __init__(self, tables: List[str]):
        self.tables = tables

    def to_table(self, table: str, columns: List[str]) -> None:
        self.name = CliStateName.TABLE
        self.table = table
        self.columns = columns

    def to_update(self, column: str, row_id: int) -> None:
        if self.table is None:
            raise InvalidStateTransition('Moving to state "update" when no table was selected')

        self.name = CliStateName.UPDATE
        self.column = column
        self.row_id = row_id

    # TODO: Add to_insert method
