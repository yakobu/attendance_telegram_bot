from telegram import ReplyKeyboardRemove
from telegram.ext import MessageHandler, RegexHandler

from models import User
from default_logger import logger


class FilterMessage(MessageHandler):
    """"""
    FILTERS = NotImplemented

    def __init__(self, *args, **kwargs):
        super(FilterMessage, self).__init__(self.FILTERS, self._callback,
                                            *args, **kwargs)
        self.logger = logger

    def _callback(self, bot, update):
        raise NotImplementedError("You cannot access abstract method")


class RegexMessage(RegexHandler):
    """"""
    PATTERN = NotImplemented

    def __init__(self, *args, **kwargs):
        super(RegexMessage, self).__init__(self.PATTERN, self.handler,
                                           *args, **kwargs)
        self.logger = logger

    def _callback(self, bot, update, user):
        raise NotImplementedError("You cannot access abstract method")

    def handler(self, bot, update):
        user_id = update.message.chat.id
        self.logger.debug("got message: %s from %s",
                          update.message.text,
                          user_id)

        user = User.objects(id=user_id).first()

        if user is not None:
            return self._callback(bot, update, user)

        self.logger.debug("Unmounted user %d try to access this end point",
                          user_id)

        update.message.reply_text("You are not mounted, type /start to mount",
                                  reply_markup=ReplyKeyboardRemove())
