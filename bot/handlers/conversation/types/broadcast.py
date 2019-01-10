# encoding: utf-8
from __future__ import unicode_literals

import textwrap

from emoji import emojize
from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import RegexHandler, MessageHandler, Filters

from models import User

from keyboards import ManuKeyboard
from .abstarct import ConversationType
from handlers.conversation.consts import STATES
from handlers.utils import restricted_for_admin


class Broadcast(ConversationType):
    """"""

    @property
    def entry_points(self):
        return [
            RegexHandler(pattern="Broadcast",
                         callback=self.ask_for_message,
                         pass_chat_data=True),
        ]

    @property
    def states(self):
        return {
            STATES.BROADCAST_MESSAGE: [
                MessageHandler(filters=Filters.text,
                               callback=self.send_message,
                               pass_chat_data=True)
            ]
        }

    BROADCAST_MESSAGE = textwrap.dedent("""
    :mega: Message from *{user_name}*:
    {message}
    """)

    @restricted_for_admin
    def ask_for_message(self, bot, update, chat_data):
        self.logger.debug("got message: %s", update.message.text)
        message = emojize(":love_letter: Type in your message please",
                          use_aliases=True)
        update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

        return STATES.BROADCAST_MESSAGE

    def send_message(self, bot, update, chat_data):
        admin = chat_data["admin"]
        message = emojize(self.BROADCAST_MESSAGE.format(user_name=admin.name,
                                                        message=update.message.text),
                          use_aliases=True)

        for user_id in User.objects.values_list("id"):
            self.logger.debug("Send message to %s by Broadcast from %s",
                              user_id, admin.name)

            bot.send_message(chat_id=user_id,
                             text=message,
                             parse_mode=ParseMode.MARKDOWN)

        reply_markup = ManuKeyboard(admin=admin.is_admin,
                                    manager=admin.is_manager).markup
        update.message.reply_text(emojize("Done:thumbsup:", use_aliases=True),
                                  reply_markup=reply_markup)

        return STATES.END
