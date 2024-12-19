from typing import Dict, List, Set, Union, Iterable
from prompt_toolkit.completion import Completer, CompleteEvent, Completion, NestedCompleter
from prompt_toolkit.document import Document

Completions = Dict[str, Union[Set[str], None]]

class DynamicCompleter(Completer):
    def __init__(self, completions: Completions) -> None:
        self.completer = NestedCompleter.from_nested_dict(completions)

    @classmethod
    def from_dict(cls, completions: Completions):
        """
        Example completions: {'update': set{'column1', 'column2'}, 'help': None}
        """
        return cls(completions)

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        return self.completer.get_completions(document, complete_event)

    def add(self, key: str, value: str) -> None:
        self.completer.options[key].options[value] = None

    def clear(self, key: str) -> None:
        self.completer.options[key] = None

    # dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    # # Double each value in the dictionary
    # double_dict1 = {k:v*2 for (k,v) in dict1.items()}
    # print(double_dict1) 

    # {'e': 10, 'a': 2, 'c': 6, 'b': 4, 'd': 8}

    def update(self, key: str, values: List[str]) -> None:
        values_dict = {k:None for k in values}
        self.completer.options[key].options = values_dict
    