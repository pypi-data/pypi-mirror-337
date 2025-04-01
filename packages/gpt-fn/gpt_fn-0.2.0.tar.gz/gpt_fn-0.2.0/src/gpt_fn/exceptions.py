from typing import Any

from openai.types.chat import ChatCompletion


class GptFnError(Exception):
    pass


class CompletionIncompleteError(GptFnError):
    def __init__(self, msg: str, request: dict[str, Any], response: ChatCompletion) -> None:
        super().__init__(msg)
        self.response = response
        self.request = request


class AiFnError(GptFnError):
    def __init__(self, msg: str, fn_locals: dict[str, Any]) -> None:
        super().__init__(msg)
        self.fn_locals = fn_locals
