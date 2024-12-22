from enum import Enum
from typing import List


class CommandType(Enum):
    def __init__(self, alias):
        self.alias = alias

    TABLE = 'table'
    LIST = 'list'
    NEXT = 'next'
    UPDATE = 'update'
    DELETE = 'delete'
    INSERT = 'insert'
    HELP = 'help'
    EXIT = 'exit'


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
        arguments = split_prompt[1:]

        for command_type in CommandType:
            if command_type.alias == alias:
                return cls(command_type, arguments)

        raise Exception(f'Invalid command {alias}')
