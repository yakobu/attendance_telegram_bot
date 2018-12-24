from emoji import emojize
from telegram import ReplyKeyboardRemove
from telegram.ext import RegexHandler, MessageHandler, Filters

from models import Group, User
from .abstract import Conversation
from handlers.conversation.consts import STATES
from handlers.utils import restricted_for_admin
from keyboards import (AttendanceKeyboard,
                       ManuKeyboard,
                       NotHereRasonsKeyboard,
                       GeneralKeyboard)


class AddGroupConversation(Conversation):
    """Set User status."""

    @property
    def start_triggers(self):
        return [
            RegexHandler(pattern="Add Group",
                         callback=self.request_for_group_name,
                         pass_chat_data=True),
        ]

    @property
    def states_options(self):
        return {
            STATES.ADD_GROUP_NAME: [
                MessageHandler(filters=Filters.text,
                               callback=self.request_for_group_type,
                               pass_chat_data=True)
            ],

            STATES.ADD_GROUP_TYPE: [
                MessageHandler(filters=Filters.text,
                               callback=self.determine_group_type,
                               pass_chat_data=True)
            ]
        }

    GROUP_TYPES = ["Users", "Groups"]

    @restricted_for_admin
    def request_for_group_name(self, bot, update, chat_data):
        self.logger.debug("got message: %s", update.message.text)
        update.message.reply_text('OK, select group name',
                                  reply_markup=ReplyKeyboardRemove())

        return STATES.ADD_GROUP_NAME

    def request_for_group_type(self, bot, update, chat_data):
        """"""
        self.logger.debug("got message: %s", update.message.text)
        chat_data["group"] = Group(name=update.message.text)
        markup = GeneralKeyboard(option_list=self.GROUP_TYPES).markup
        update.message.reply_text('OK, what kind of group?',
                                  reply_markup=markup)

        return STATES.ADD_GROUP_TYPE

    def determine_group_type(self, bot, update, chat_data):
        message = update.message

        if message.text not in self.GROUP_TYPES:
            markup = GeneralKeyboard(option_list=self.GROUP_TYPES).markup
            message.reply_text(
                emojize(
                    "You can't:unamused:, Please select from the keyboard",
                    use_aliases=True),
                reply_markup=markup)
            return

        group = chat_data["group"]
        group.type = message.text

        message.reply_text(
            emojize(
                ":thumbsup:",
                use_aliases=True))

        if group.type == "Groups":
            posible_items = Group.objects.values_list('name')

        if group.type == "Users":
            posible_items = User.objects.values_list('name')

        markup = GeneralKeyboard(option_list=posible_items).markup
        message.reply_text(
            emojize(
                "Now lets create the group:boom:",
                use_aliases=True),
            reply_markup=markup)
