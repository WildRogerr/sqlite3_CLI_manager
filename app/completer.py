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

    def update(self, completions: Completions) -> None:
        self.completer = NestedCompleter.from_nested_dict(completions)
