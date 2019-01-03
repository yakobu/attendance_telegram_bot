# encoding: utf-8
from __future__ import unicode_literals

import textwrap
from datetime import datetime

from emoji import emojize

from models import Report,User

from .abstract import RegexMessage
from keyboards import ManuKeyboard


class GetUsersStatusMessage(RegexMessage):
    """"""
    PATTERN = "Get Users Status"

    STATUS_PATTERN = textwrap.dedent("""\
        {symbol} {status}:
        {users}
        """)

    def user_statuses(self, report, user_id):
        """"""
        if report is None:
            return None

        for status in report.statuses[::-1]:
            if status.user.id == user_id:
                return status

        return None

    def get_users_status(self):
        report = Report.objects(date=datetime.now().date()).first()
        users = User.objects.all()

        here = []
        not_here = []
        not_specified = []

        for user in users:
            status = self.user_statuses(report, user.id)
            if status is None:
                not_specified.append(user.name)
            elif status.state == "Here":
                here.append(user.name)
            elif status.state == "Not Here":
                not_here.append((user.name, status.reason))

        return here, not_here, not_specified

    def _callback(self, bot, update, user):
        self.logger.debug("got message: %s", update.message.text)
        if user.is_admin is False:
            print("Unauthorized admin access denied for {}.".format(user.id))
            return

        here, not_here, not_specified = self.get_users_status()
        statuses = []

        if len(here) != 0:
            users = ["\t\t\t:bust_in_silhouette: {name}".format(name=user_name)
                     for user_name in
                     here]
            statuses.append(self.STATUS_PATTERN.format(
                symbol=":heavy_check_mark:",
                status="Here",
                users="\n".join(users)))

        if len(not_here) != 0:
            users = [
                "\t\t\t:bust_in_silhouette: {name}:\n\t\t\t\t:pencil2:{reason}".format(
                    name=user_name, reason=reason)
                for user_name, reason in not_here]
            statuses.append(self.STATUS_PATTERN.format(
                symbol=":x:",
                status="Not Here",
                users="\n".join(users)))

        if len(not_specified) != 0:
            users = ["\t\t\t:bust_in_silhouette: {name}".format(name=user_name)
                     for user_name in
                     not_specified]
            statuses.append(self.STATUS_PATTERN.format(
                symbol=":question:",
                status="Not Specified",
                users="\n".join(users)))

        reply_markup = ManuKeyboard(admin=user.is_admin,
                                    manager=user.is_manager).markup
        user_status_report = "\n".join(statuses)
        update.message.reply_text(emojize(user_status_report, use_aliases=True),
                                  reply_markup=reply_markup)

