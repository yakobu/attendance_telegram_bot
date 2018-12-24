# encoding: utf-8
from emoji import emojize

# from handlers.conversation.consts import NOT_HERE, HERE
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


class GroupTypeKeyboard(ReplyKeyboard):
    @property
    def options(self):
        return ["Users",
                "Groups",
                "Cancel"]
