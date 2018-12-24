# encoding: utf-8
from emoji import emojize

from .abstract import ReplyKeyboard, InlineKeyboard, KeyboardData


class NotHereRasonsKeyboard(ReplyKeyboard):
    @property
    def options(self):
        return [
            "מחוץ ליחידה - תפקיד",
            "מחוץ ליחידה - הפניה",
            "מחוץ ליחידה - משמרות",
            'אבט"ש / הגנ"ש',
            "יום ד'",
            "גימלים",
            "מחוץ ליחידה - לימודים",
            "חופשת חובה",
            "חופשה שנתית",
            "חופשה מיוחדת",
            'חל"ת',
            'חו"ל בתפקיד',
            'חו"ל',
            "יום מחלה בהצהרה",
            "מסופח מקצועי",
            "מסופח קורס",
            "יום סידורים",
            "חופשת לידה",
        ]


class ManuKeyboard(ReplyKeyboard):
    @property
    def options(self):
        all_commands = [["Set Status", "Get Status"],
                        # "Set Name",
                        "Get Name",
                        "Get Root Permission"]
        if self.admin:
            all_commands.append("Add Group")
            all_commands.remove("Get Root Permission")

        return all_commands


class AttendanceKeyboard(InlineKeyboard):
    OPTIONS = [
        [
            KeyboardData(text=emojize(":thumbsdown:", use_aliases=True),
                         callback_data="Not Here"),
            KeyboardData(text=emojize(":thumbsup:", use_aliases=True),
                         callback_data="Here")],

    ]


class GeneralKeyboard(ReplyKeyboard):
    def __init__(self, option_list=None, *args, **kwargs):
        super(GeneralKeyboard, self).__init__(*args, **kwargs)
        self.option_list = option_list

    @property
    def options(self):
        return self.option_list
