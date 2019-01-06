import os

from emoji import emojize
from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import RegexHandler, Filters, MessageHandler


from models import User
from keyboards import ManuKeyboard
from .abstarct import ConversationType
from handlers.conversation.consts import STATES


class GetRootPermission(ConversationType):
    """"""
    PASSWORD = os.environ["PASSWORD"]

    @property
    def entry_points(self):
        return [
            RegexHandler(pattern="Get Root Permission",
                         callback=self.send_request_for_password)
        ]

    @property
    def states(self):
        return {
            STATES.INSERT_PASSWORD: [
                MessageHandler(filters=Filters.text,
                               callback=self.validate_password)
            ],
        }

    def send_request_for_password(self, bot, update):
        """Send a message when the command /start is issued."""
        self.logger.debug("got message: %s", update.message.text)

        message = ":closed_lock_with_key: Enter Your Password Please :key:"
        update.message.reply_text(text=emojize(message,
                                               use_aliases=True),
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=ReplyKeyboardRemove())

        return STATES.INSERT_PASSWORD

    def validate_password(self, bot, update):
        message = update.message
        chat = message.chat

        user = User.objects(id=chat.id).first()

        if user:
            if message.text.strip() == self.PASSWORD.strip():

                user.is_admin = True
                user.save()

                messagge = ":tada::confetti_ball::tada::confetti_ball:  " \
                           "YOU ARE ADMIN " \
                           ":tada::confetti_ball::tada::confetti_ball:"

                markup = ManuKeyboard(admin=user.is_admin,
                                      manager=user.is_manager).markup
                message.reply_text(emojize(messagge,
                                           use_aliases=True),
                                   reply_markup=markup)

            else:
                markup = ManuKeyboard(admin=user.is_admin,
                                      manager=user.is_manager).markup
                message.reply_text(
                    emojize(":gun: Wrong Password :gun:", use_aliases=True),
                    reply_markup=markup)

        else:
            markup = ManuKeyboard(admin=user.is_admin,
                                  manager=user.is_manager).markup
            message.reply_text("You should mount as a user first, type /start",
                               reply_markup=markup)

        return STATES.END
