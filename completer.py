from typing import Dict, Set, Union, Iterable
from prompt_toolkit.completion import WordCompleter, Completer, CompleteEvent, Completion
from prompt_toolkit.document import Document

Completions = Dict[str, Union[Set[str], None]]
CompleterOptions = Dict[str, Union[Completer, None]]

class DynamicCompleter(Completer):
    def __init__(self, options: CompleterOptions) -> None:
        self.options = options
        self.ignore_case = True

    @classmethod
    def from_dict(cls, completions: Completions):
        """
        Example completions = {'update': set{'column1', 'column2'}, 'help': None}
        """
        options: CompleterOptions = {}
        for key, value in completions.items():
            if isinstance(value, set):
                options[key] = cls.from_dict({item: None for item in value})
            else:
                assert value is None
                options[key] = None

        return cls(options)

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        # Split document.
        text = document.text_before_cursor.lstrip()
        stripped_len = len(document.text_before_cursor) - len(text)

        # If there is a space, check for the first term, and use a
        # subcompleter.
        if " " in text:
            first_term = text.split()[0]
            completer = self.options.get(first_term)

            # If we have a sub completer, use this for the completions.
            if completer is not None:
                remaining_text = text[len(first_term):].lstrip()
                move_cursor = len(text) - len(remaining_text) + stripped_len

                new_document = Document(
                    remaining_text,
                    cursor_position=document.cursor_position - move_cursor,
                )

                yield from completer.get_completions(new_document, complete_event)

        # No space in the input: behave exactly like `WordCompleter`.
        else:
            completer = WordCompleter(
                list(self.options.keys()), ignore_case=self.ignore_case
            )
            yield from completer.get_completions(document, complete_event)

    def add(self, key: str, value: str) -> None:
        self.options[key].options[value] = None

    def clear(self, key: str) -> None:
        pass
    