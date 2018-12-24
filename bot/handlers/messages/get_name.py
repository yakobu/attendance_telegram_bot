from emoji import emojize

from .abstract import RegexMessage
from keyboards import ManuKeyboard


class GetNameMessage(RegexMessage):
    """"""
    PATTERN = "Get Name"

    def _callback(self, bot, update, user):
        """Send a message when the command /start is issued."""
        message = update.message
        self.logger.debug("got message: %s", message.text)

        messagge = ":guardsman:  {name}". \
            format(name=user.name.encode("utf-8"))

        name_message = emojize(messagge.decode("utf-8"), use_aliases=True)

        keyboard = ManuKeyboard(admin=user.is_admin,
                                manager=user.is_manager).markup

        message.reply_text(name_message, reply_markup=keyboard)
