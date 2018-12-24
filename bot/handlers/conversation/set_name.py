from emoji import emojize
from telegram import ReplyKeyboardRemove, ParseMode
from telegram.ext import RegexHandler, MessageHandler, Filters

from models import User
from keyboards import ManuKeyboard
from .abstract import Conversation
from handlers.conversation.consts import STATES


class SetNameConversation(Conversation):
    """"""
    USER_NAME_MESSAGE_FORMAT = "{header}\n{name}".decode("utf-8")

    @property
    def start_triggers(self):
        return [RegexHandler(pattern="Set Name",
                             callback=self.get_name_request)]

    @property
    def states_options(self):
        return {
            STATES.INSERT_NAME: [
                MessageHandler(filters=Filters.text,
                               callback=self.set_user_name)
            ],
        }

    def get_name_request(self, bot, update):
        """Send a message when the command /start is issued."""
        message = update.message
        self.logger.debug("got message: %s", message.text)

        message.reply_text(
            emojize(":pencil2: Please enter your full name (English) :pencil2:",
                    use_aliases=True),
            reply_markup=ReplyKeyboardRemove())

        return STATES.INSERT_NAME

    def set_user_name(self, bot, update):
        message = update.message
        chat = message.chat

        user = User.objects(id=chat.id).modify(upsert=True,
                                               name=message.text)

        name_header = ":paperclip: Your name have been set"
        name = ":guardsman:  *{name}*".encode("utf-8").format(
            name=message.text.encode("utf-8"))

        name_message = self.USER_NAME_MESSAGE_FORMAT.format(
            header=name_header.decode("utf-8"),
            name=name.decode("utf-8"))

        reply_markup = ManuKeyboard(admin=user.is_admin,
                                    manager=user.is_manager).markup

        update.message.reply_text(text=emojize(name_message,
                                               use_aliases=True),
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=reply_markup)

        return STATES.END
