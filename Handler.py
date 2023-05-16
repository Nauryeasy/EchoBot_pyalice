from Response import Responser
from MiddlewareDialog import MiddlewareDialog
from flask import Flask, request


class Handler:
    def __init__(self, dialogs_dict: dict, start_dialog: object, host: str = '0.0.0.0', port: int = 6000):
        self.dialogs_dict = dialogs_dict
        self.middleware_dialog_list = MiddlewareDialog.middleware_list
        self.start_dialog = start_dialog

        self.host = host
        self.port = port

        self.app = Flask(__name__)

    def choose_dialog(self, event: dict) -> dict:
        if self.check_new_session(event):
            print('hh')
            responser = Responser(event, self.start_dialog)
            return responser.get_response()

        for middleware_dialog in MiddlewareDialog.middleware_list:
            if self.check_tokens(event, middleware_dialog):
                middleware_dialog.set_last_state(self.dialogs_dict[self.get_state(event)])
                if middleware_dialog.last_state == middleware_dialog:
                    middleware_dialog.set_last_state(self.start_dialog)
                responser = Responser(event, middleware_dialog)
                return responser.get_response()

        trigger_dialogs = self.dialogs_dict[self.get_state(event)].next_states_list

        for dialog in trigger_dialogs:
            keys = list(self.dialogs_dict.keys())
            values = list(self.dialogs_dict.values())
            if self.check_tokens(event, dialog) or dialog.always or keys[values.index(dialog)] in event['state']['session']:
                responser = Responser(event, dialog)
                return responser.get_response()

        return {
            "response": {
                "text": "Простите, не смогла распознать вашу команду\n"
                        "Повторите еще раз или обратитесь в помощь или в 'Что ты умеешь'",
                "tts": "Простите, не смогла распознать вашу команду" 
                        "Повторите еще раз или обратитесь в помощь или в 'Что ты умеешь'",
                "card": None,
                "buttons": Responser.create_buttons(['Помощь', 'Что ты умеешь']),
                "end_session": False
            },
            "session": event["session"],
            "session_state": event['state']['session'],
            "version": event["version"]
        }

    def run(self):

        @self.app.route('/', methods=['POST'])
        def main():
            event = request.get_json()
            response = self.choose_dialog(event)
            print(response)
            return response

        self.app.run(host=self.host, port=self.port)

    @staticmethod
    def get_state(event: dict) -> str:
        return event['state']['session']['branch']

    @staticmethod
    def check_tokens(event: dict, dialog: object) -> bool:
        return dialog.tokens & set(event['request']["nlu"]['tokens'])

    @staticmethod
    def check_new_session(event: dict) -> bool:
        return event['session']['new'] or not "branch" in event["state"]["session"]
