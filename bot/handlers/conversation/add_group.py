from emoji import emojize
from telegram.ext import RegexHandler, MessageHandler, Filters

from .abstract import Conversation
from handlers.conversation.consts import STATES
from handlers.utils import restricted_for_admin
from keyboards import (AttendanceKeyboard,
                       ManuKeyboard,
                       NotHereRasonsKeyboard,
                       GroupTypeKeyboard)


class AddGroupConversation(Conversation):
    """Set User status."""
    @property
    def start_triggers(self):
        return [
            RegexHandler(pattern="Add Group",
                         callback=self.request_for_group_type),
        ]

    @property
    def states_options(self):
        return {
            STATES.ADD_GROUP_TYPE: [
                MessageHandler(filters=Filters.text,
                               callback=self.determine_group_type)
            ]
        }

    @restricted_for_admin
    def request_for_group_type(self, bot, update, admin):
        """"""
        self.logger.debug("got message: %s", update.message.text)
        markup = GroupTypeKeyboard().markup
        update.message.reply_text('OK, what kind of group?',
                                  reply_markup=markup)

        return STATES.ADD_GROUP_TYPE

    def determine_group_type(self, bot, update):
        message = update.message
        if message.text == "Cancel":
            message.reply_text(emojize("OK :smile:", use_aliases=True))
            return STATES.END
