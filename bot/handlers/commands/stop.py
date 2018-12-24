from models.user import User
from abstract import Command


class StopCommand(Command):
    """Unregister user."""
    COMMAND_NAME = "stop"

    def _callback(self, bot, update):
        """Send a message when the command /stop is issued."""
        self.logger.debug("got message: %s", update.message.text)
        chat = update.message.chat

        self.logger.debug("Removing user if exist")
        User.objects(id=chat.id).delete()
        self.logger.debug("User has been deleted successfully")

        update.message.reply_text('You have been DELETED successfully')
