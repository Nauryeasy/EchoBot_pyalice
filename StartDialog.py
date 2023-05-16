from Dialog import Dialog
from typing import Callable


class StartDialog(Dialog):
    def __init__(self, next_states_list: list, get_response: Callable[[dict], dict], tokens: set):
        super().__init__(next_states_list, get_response, tokens)
        self.last_state = self
