# encoding: utf-8
from __future__ import unicode_literals

from datetime import datetime

from emoji import emojize
from telegram import ParseMode

from models import Report
from .abstract import RegexMessage
from keyboards import ManuKeyboard
from handlers.conversation.consts import NOT_HERE


class GetStatusMessage(RegexMessage):
    """"""
    PATTERN = "Get Status"
    DATE_FORMAT = "%d/%m/%Y"

    STATUS_MESSAGE_FORMAT = """
    :date: *status for {date}*
    *{state}*: {reason}
    """

    @staticmethod
    def user_statuses(report, user_id):
        """"""
        all_user_statuses = []

        if report is None:
            return all_user_statuses

        for status in report.statuses:
            if status.user_id == user_id:
                all_user_statuses.append(status)

        return all_user_statuses

    def status_message_response(self, update, date, state, reason, user):
        message = self.STATUS_MESSAGE_FORMAT.format(date=date,
                                                    state=state,
                                                    reason=reason)

        reply_markup = ManuKeyboard(admin=user.is_admin,
                                    manager=user.is_manager).markup
        update.message.reply_text(text=emojize(message, use_aliases=True),
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=reply_markup)

    def _callback(self, bot, update, user):
        now = datetime.now().date()
        formated_day = now.strftime(self.DATE_FORMAT)
        user_id = update.message.chat.id

        report = Report.objects(date=now).first()

        user_statuses = self.user_statuses(report, user_id)

        if len(user_statuses) == 0:
            self.logger.debug("status not exist")
            self.status_message_response(update=update,
                                         date=formated_day,
                                         state=NOT_HERE,
                                         reason="Not Specified",
                                         user=user)
            return

        status = user_statuses[-1]
        self.status_message_response(update=update,
                                     date=formated_day,
                                     state=status.state,
                                     reason=status.reason,
                                     user=user)
