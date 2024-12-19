
from enum import Enum

class CliStateName(Enum):
    DEFAULT = 1
    TABLE = 2
    UPDATE = 3
    INSERT = 4
    EXIT = 5

class CliState:
    name = CliStateName.DEFAULT
    column: str
    primary_key: int
