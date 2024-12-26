from typing import Dict, Final, Set
from clistate import CliState, CliStateName
from command import Command, CommandType


VALID_COMMANDS: Final[Dict[CliStateName, Set[CommandType]]] = {
    CliStateName.DEFAULT: {
        CommandType.TABLE,
        CommandType.HELP,
        CommandType.EXIT,
    },
    CliStateName.TABLE: {
        CommandType.TABLE,
        CommandType.HELP,
        CommandType.EXIT,
        CommandType.UPDATE,
        CommandType.INSERT,
        CommandType.DELETE,
        CommandType.LIST,
        CommandType.NEXT,
    },
    CliStateName.UPDATE: set(),
    CliStateName.INSERT: set(),
}


class CliErrorCode:
    NEEDS_TABLE_STATE = 1


def validate_command(command: Command, state: CliState) -> CliErrorCode:
    if state.name == CliStateName.DEFAULT:
        if not is_in_valid_command(state.name,command.command_type):
            return CliErrorCode.NEEDS_TABLE_STATE
    return None

def is_in_valid_command(state_name:CliStateName,command_type:CommandType) -> bool:
    return command_type in VALID_COMMANDS[state_name]

def print_error(error_code: CliErrorCode) -> None:
    if error_code == CliErrorCode.NEEDS_TABLE_STATE:
        print('First use table [tablename], to connect to table.')