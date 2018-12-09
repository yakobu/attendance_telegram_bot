from telegram.ext import CommandHandler

from default_logger import logger


class Command(CommandHandler):
    """"""
    COMMAND_NAME = NotImplemented

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(self.COMMAND_NAME, self._callback,
                                      *args, **kwargs)
        self.logger = logger

    def _callback(self, bot, update):
        raise NotImplementedError("You cannot access abstract method")
