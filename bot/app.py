import os
from datetime import time

from mongoengine import connect
from telegram.ext import Updater, MessageHandler, Filters

from commands import StartCommand
from default_logger import logger


class AttendanceTelegramBot(object):
    TOKEN = os.environ["TELEGRAM_TOKEN"]
    MANAGER_ID = os.environ["MANAGER_ID"]
    MONGOSE_URI = os.environ["MONGOSE_URI"]
    PORT = int(os.environ.get("PORT", 8443))
    APP_NAME = os.environ["APP_NAME"]
    APP_URI = "https://{app_name}.herokuapp.com/".format(app_name=APP_NAME)
    DEPLOY_MODE = os.environ.get("DEPLOY_MODE", False)

    COMMANDS = [
        StartCommand,
    ]

    def __init__(self):
        self.logger = logger
        self.updater = Updater(self.TOKEN)
        self.dp = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

    def connect(self):
        if self.DEPLOY_MODE:
            self.logger.debug("Connecting to server via webhook..")
            self.updater.start_webhook(listen="0.0.0.0",
                                       port=self.PORT,
                                       url_path=self.TOKEN)
            self.updater.bot.set_webhook(self.APP_URI + self.TOKEN)

        else:
            self.logger.debug("Polling from server..")
            self.updater.bot.delete_webhook()
            self.updater.start_polling()

        self.updater.idle()

    def initialize(self):
        for command in self.COMMANDS:
            self.logger.debug("Initializing %s command", command.__name__)
            self.dp.add_handler(command())

        # on noncommand i.e message - echo the message on Telegram
        self.dp.add_handler(MessageHandler(Filters.text, self.echo))

        # log all errors
        self.dp.add_error_handler(self.on_error)

        self.job_queue.run_daily(callback=self.daily_reminder,
                                 time=time(18, 53),
                                 days=(0, 1, 2, 3, 4),
                                 context=None,
                                 name="daily_reminder")

    def daily_reminder(self, bot, update):
        bot.send_message(chat_id=self.MANAGER_ID,
                         text='Sending messages with increasing delay up to 10s, then stops.')

    def echo(self, bot, update):
        """Echo the user message."""
        self.logger.debug("got message: %s", update.message.text)
        update.message.reply_text(update.message.text)

    def on_error(self, bot, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def run(self):
        self.logger.debug("Connectig to %s", self.MONGOSE_URI)
        connect(self.MONGOSE_URI)

        self.initialize()
        self.connect()

if __name__ == "__main__":
    bot = AttendanceTelegramBot()
    bot.run()
