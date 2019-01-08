# encoding: utf-8
from __future__ import unicode_literals

from models.user import User
from abstract import Command
from keyboards import ManuKeyboard


class StartCommand(Command):
    """Register user."""
    COMMAND_NAME = "start"
    USER_NAME_FORMAT = "{first_name} {last_name}"

    def _callback(self, bot, update):
        """Send a message when the command /start is issued."""
        self.logger.debug("got message: %s", update.message.text)
        chat = update.message.chat

        name = self.USER_NAME_FORMAT.format(first_name=chat.first_name,
                                            last_name=chat.last_name) \
            if chat.last_name else chat.first_name

        user = User.objects(id=chat.id).modify(upsert=True,
                                               new=True,
                                               name=name)
        self.logger.debug("Saving user details on db")
        user.save()
        self.logger.debug("Successfully saved user")

        keyboard = ManuKeyboard(admin=user.is_admin,
                                manager=user.is_manager).markup

        update.message.reply_text('You have been mounted successfully',
                                  reply_markup=keyboard)
