# encoding: utf-8
from __future__ import unicode_literals

import textwrap
from datetime import datetime
from emoji import emojize
from telegram.ext import RegexHandler, MessageHandler, Filters

from models import Group, User, Report
from .abstarct import ConversationType
from handlers.conversation.consts import STATES
from handlers.utils import restricted_for_manager
from keyboards import (AttendanceKeyboard,
                       ManuKeyboard,
                       NotHereRasonsKeyboard,
                       GeneralKeyboard)


class GetGroupStatus(ConversationType):
    """Set User status."""

    @property
    def entry_points(self):
        return [
            RegexHandler(pattern="Get Group Status",
                         callback=self.group_status,
                         pass_chat_data=True),
        ]

    @property
    def states(self):
        return {
            STATES.SELECT_GROUP: [
                MessageHandler(filters=Filters.text,
                               callback=self.send_status_for_selected_group,
                               pass_chat_data=True)
            ]
        }

    STATUS_PATTERN = textwrap.dedent("""\
    {symbol} {status}:
    {users}
    """)

    def user_statuses(self, report, user_id):
        """"""
        if report is None:
            return None

        for status in report.statuses[::-1]:
            if status.user_id == user_id:
                return status

        return None

    def get_users_group_status(self, group):
        report = Report.objects(date=datetime.now().date()).first()

        here = []
        not_here = []
        not_specified = []

        for item in group.items:
            status = self.user_statuses(report, item.id)
            if status is None:
                not_specified.append(item.name)
            elif status.state == "Here":
                here.append(item.name)
            elif status.state == "Not Here":
                not_here.append((item.name, status.reason))

        return here, not_here, not_specified

    def send_users_guoup_status(self, group, update):
        here, not_here, not_specified = self.get_users_group_status(group)
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

        reply_markup = ManuKeyboard(admin=group.manager.is_admin,
                                    manager=group.manager.is_manager).markup
        user_group_status_report = \
            "{group_name}\n".format(group_name=group.name) + "\n".join(statuses)
        update.message.reply_text(emojize(user_group_status_report,
                                          use_aliases=True),
                                  reply_markup=reply_markup)

    def send_group_status(self, group, update):
        if group.type == "Users":
            self.send_users_guoup_status(group, update)
            return

        update.message.reply_text("{group_name}".format(group_name=group.name))
        for item in group.items:
            self.send_group_status(item, update)

    @restricted_for_manager
    def group_status(self, bot, update, chat_data):
        self.logger.debug("got message: %s", update.message.text)
        manager = chat_data["manager"]
        groups = Group.objects(manager=manager)
        if len(groups) == 0:
            reply_markup = ManuKeyboard(admin=manager.is_admin,
                                        manager=manager.is_manager).markup
            update.message.reply_text(text="You have no groups",
                                      reply_markup=reply_markup)
            return STATES.END

        if len(groups) == 1:
            self.send_users_guoup_status(groups[0], update)
            return STATES.END

        optional_groups = [group.name for group in groups]
        markup = GeneralKeyboard(option_list=optional_groups).markup
        update.message.reply_text(
            emojize('OK, select group name'
                    ':grey_exclamation::grey_exclamation:', use_aliases=True),
            reply_markup=markup)

        return STATES.SELECT_GROUP

    def send_status_for_selected_group(self, bot, update, chat_data):
        self.logger.debug("got message: %s", update.message.text)
        manager = chat_data["manager"]
        name = update.message.text
        selected_group = Group.objects(manager=manager, name=name).first()
        if selected_group is None:
            update.message.reply_text(
                emojize('Select from the Keyboard:unamused:', use_aliases=True))
            return

        self.send_group_status(selected_group, update)
        return STATES.END
