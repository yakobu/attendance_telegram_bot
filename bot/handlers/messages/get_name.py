# encoding: utf-8
from __future__ import unicode_literals

from emoji import emojize

from .abstract import RegexMessage
from keyboards import ManuKeyboard


class GetNameMessage(RegexMessage):
    """"""
    PATTERN = "Get Name"

    def _callback(self, bot, update, user):
        """Send a message when the command /start is issued."""
        message = update.message
        name_message = ":guardsman:  {name}".format(name=user.name)
        keyboard = ManuKeyboard(admin=user.is_admin,
                                manager=user.is_manager).markup

        message.reply_text(emojize(name_message, use_aliases=True),
                           reply_markup=keyboard)
