# encoding: utf-8
import os

from mongoengine import connect
from telegram.ext import Updater

from default_logger import logger
from handlers import (GetRootPermissionConversation,
                      AddGroupConversation,
                      StartCommand,
                      StopCommand,
                      SetStatusConversation,
                      GetStatusMessage,
                      GetNameMessage,
                      SetNameConversation)


class AttendanceTelegramBot(object):
    MONGOSE_URI_PATTERN = \
        "mongodb://{user}:{password}@ds151127.mlab.com:51127/{db_name}"
    MONGO_DB = os.environ["MONGO_DB"]
    MONGO_USER = os.environ["MONGO_USER"]
    MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]

    HANDLERS = [
        StartCommand,
        SetStatusConversation,
        AddGroupConversation,
        SetNameConversation,
        GetRootPermissionConversation,
        GetStatusMessage,
        GetNameMessage,
        StopCommand,
    ]

    def __init__(self, token, port, app_uri):
        self.logger = logger
        self.token = token
        self.port = port
        self.app_uri = app_uri

        self.updater = Updater(self.token)
        self.dp = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

    def connect(self):
        self.logger.debug("Connecting to server via webhook..")
        # self.updater.start_webhook(listen="0.0.0.0",
        #                            port=self.port,
        #                            url_path=self.token)
        # self.updater.bot.set_webhook(self.app_uri + self.token)
        self.updater.start_polling()
        self.updater.idle()

    def initialize(self):
        for command in self.HANDLERS:
            self.logger.debug("Initializing %s command", command.__name__)
            self.dp.add_handler(command())

        # log all errors
        self.dp.add_error_handler(self.on_error)

        # self.job_queue.run_daily(callback=self.daily_reminder,
        #                          time=time(18, 53),
        #                          days=(0, 1, 2, 3, 4),
        #                          context=None,
        #                          name="daily_reminder")

    # def daily_reminder(self, bot, update):
    #     bot.send_message(chat_id=self.MANAGER_ID,
    #                      text='Sending messages with increasing delay up to 10s, then stops.')

    def on_error(self, bot, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def run(self):
        mongose_uri = self.MONGOSE_URI_PATTERN.format(
            user=self.MONGO_USER,
            password=self.MONGO_PASSWORD,
            db_name=self.MONGO_DB)

        self.logger.debug("Connectig to %s", mongose_uri)
        connect(db=self.MONGO_DB,
                username=self.MONGO_USER,
                password=self.MONGO_PASSWORD,
                host=mongose_uri)

        self.initialize()
        self.connect()


if __name__ == "__main__":
    token = os.environ["TELEGRAM_TOKEN"]
    port = int(os.environ.get("PORT", 8443))

    app_name = os.environ["APP_NAME"]
    app_uri = "https://{app_name}.herokuapp.com/".format(app_name=app_name)

    bot = AttendanceTelegramBot(token=token, port=port, app_uri=app_uri)
    bot.run()
