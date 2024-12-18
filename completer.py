from typing import Dict, Set, Union, Iterable
from prompt_toolkit.completion import WordCompleter, Completer, CompleteEvent, Completion
from prompt_toolkit.document import Document

class DynamicCompleter(Completer):
    def __init__(self, options):
        self.options = options
        self.completions = {}

    @classmethod
    def from_dict(self, data: Dict[str, Union[Set[str], None]]) -> Iterable[Completion]:
        # data = {'update': {'column1', 'column2'}, 'help': None}
        return DynamicCompleter({})

    def get_completions(self, document: Document, complete_event: CompleteEvent):
        print(document)
        print(complete_event)
        completer = WordCompleter(['test1', 'test2'])
        yield completer.get_completions(document, complete_event)

    def add(self, key, value):
        pass

    def clear(self, key):
        pass
    