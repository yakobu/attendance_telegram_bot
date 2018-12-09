from abstract import Command


class StartCommand(Command):
    """"""
    COMMAND_NAME = "start"

    def _callback(self, bot, update):
        """Send a message when the command /start is issued."""
        self.logger.debug("got message: %s", update.message.text)
        update.message.reply_text('Hi!')
