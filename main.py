from Dialog import Dialog
from StartDialog import StartDialog
from MiddlewareDialog import MiddlewareDialog
from Handler import Handler


def main_def(event):
    return {
        "text": f"{event['request']['original_utterance']}",
        "tts":
            f'{event["request"]["original_utterance"]}',
        "buttons": [
            "Что ты умеешь?",
            "Помощь"
        ],
        "session_state": {
            "branch": "main",
            "main": ""
        }
    }


def features_def(event):
    return {
        "text": "Ничего, получается(",
        "tts": "Ничего, получается(",
        "buttons": [
            "Что ты умеешь?",
            "Помощь"
        ],
        "session_state": {
            "branch": "main",
            "main": ""
        }
    }


def help_def(event):
    return {
        "text": "Типо пытаюсь помочь",
        "tts": "Типо пытаюсь помочь",
        "buttons": [
            "Что ты умеешь?",
            "Помощь"
        ],
        "session_state": {
            "branch": "main",
            "main": ""
        }
    }


main = StartDialog([], main_def, set({}))
main.set_next_states_list([main])

help = MiddlewareDialog([], help_def, {'помощь', 'помоги', 'help'})
features = MiddlewareDialog([], features_def, {'умеешь', 'возможности'})

dialogs_dict = {
    'main': main
}

dialog_handler = Handler(dialogs_dict, main, '0.0.0.0', 6000)

if __name__ == '__main__':
    dialog_handler.run()
