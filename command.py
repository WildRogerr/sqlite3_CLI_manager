from enum import Enum
from typing import List, Tuple


class InvalidCommand(Exception):
    pass


class InvalidArguments(Exception):
    pass


class CommandType(Enum):
    alias: str
    args_range: Tuple[int, int]


    def __init__(self, alias, args_range):
        self.alias = alias
        self.args_range = args_range

    TABLE = 'table', (1, 1)
    LIST = 'list', (0, 1)
    NEXT = 'next', (0, 0)
    UPDATE = 'update', (2, 2)
    DELETE = 'delete', (1, 1)
    INSERT = 'insert', (0, 1)
    HELP = 'help', (0, 0)
    EXIT = 'exit', (0, 0)


class Command:
    command_type: CommandType
    arguments: List[str]

    def __init__(self, command_type: CommandType, arguments: List[str]):
        self.command_type = command_type
        self.arguments = arguments

    @classmethod
    def from_prompt(cls, prompt: str):
        split_prompt = prompt.split(' ')
        alias = split_prompt[0]
        
        for command_type in CommandType:
            if command_type.alias == alias:
                arguments = split_prompt[1:]
                len_args = len(arguments)
                min_args = command_type.args_range[0]
                max_args = command_type.args_range[1]
                if len_args >= min_args and len_args <= max_args:
                    return cls(command_type, arguments)
                else:
                    raise InvalidArguments(f'Invalid number of arguments for command {alias}. Must be in range [{min_args}, {max_args}]')

        raise InvalidCommand(f'Invalid command {alias}')
