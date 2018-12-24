from collections import namedtuple

from telegram import (KeyboardButton,
                      ReplyKeyboardMarkup,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)


KeyboardData = namedtuple("KeyboardData", ["text", "callback_data"])


class ReplyKeyboard(object):
    def __init__(self, admin=False, manager=False):
        self.admin = admin
        self.manager = manager

    @property
    def options(self):
        return NotImplemented("This is abstract property")

    @property
    def markup(self):
        keyboard = []
        for option in self.options:
            if type(option) is str:
                keyboard.append([KeyboardButton(option)])

            if type(option) is list:
                keyboard.append(KeyboardButton(option_case)
                                for option_case in option)

        return ReplyKeyboardMarkup(keyboard)


class InlineKeyboard(object):
    OPTIONS = []

    @classmethod
    def markup(cls):
        keyboard = []
        for option in cls.OPTIONS:
            if type(option) is KeyboardData:
                keyboard.append([
                    InlineKeyboardButton(text=option.text,
                                         callback_data=option.callback_data)])

            if type(option) is list:
                keyboard.append(
                    InlineKeyboardButton(
                        text=option_case.text,
                        callback_data=option_case.callback_data)
                    for option_case in option)

        return InlineKeyboardMarkup(keyboard)
