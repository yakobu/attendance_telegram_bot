# encoding: utf-8
from __future__ import unicode_literals

from emoji import emojize
from telegram import ReplyKeyboardRemove
from telegram.ext import RegexHandler, MessageHandler, Filters

from models import Group, User
from .abstarct import ConversationType
from handlers.conversation.consts import STATES
from handlers.utils import restricted_for_admin
from keyboards import (AttendanceKeyboard,
                       ManuKeyboard,
                       NotHereRasonsKeyboard,
                       GeneralKeyboard)


class AddGroup(ConversationType):
    """"""
    @property
    def entry_points(self):
        return [
            RegexHandler(pattern="Add Group",
                         callback=self.send_request_for_group_name,
                         pass_chat_data=True),
        ]

    @property
    def states(self):
        return {
            STATES.ADD_GROUP_NAME: [
                MessageHandler(filters=Filters.text,
                               callback=self.set_group_name_ask_for_manager,
                               pass_chat_data=True)
            ],
            STATES.ADD_GROUP_MANAGER: [
                MessageHandler(filters=Filters.text,
                               callback=self.set_manager_and_ask_for_type,
                               pass_chat_data=True)
            ],

            STATES.ADD_GROUP_TYPE: [
                MessageHandler(filters=Filters.text,
                               callback=self.set_group_type_and_ask_for_items,
                               pass_chat_data=True)
            ],
            STATES.ADD_GROUP_ITEMS: [
                MessageHandler(filters=Filters.text,
                               callback=self.add_group_items,
                               pass_chat_data=True)
            ]
        }

    GROUP_TYPES = ["Users", "Groups"]

    @restricted_for_admin
    def send_request_for_group_name(self, bot, update, chat_data):
        self.logger.debug("got message: %s", update.message.text)
        update.message.reply_text('OK, select group name',
                                  reply_markup=ReplyKeyboardRemove())

        return STATES.ADD_GROUP_NAME

    def set_group_name_ask_for_manager(self, bot, update, chat_data):
        """"""
        self.logger.debug("got message: %s", update.message.text)
        gruoup_exist = Group.objects(
            name=update.message.text).first() is not None
        if gruoup_exist:
            update.message.reply_text(emojize('Sorry:no_mouth:, already exist',
                                              use_aliases=True))
            update.message.reply_text('Choose another name')
            return
        chat_data["group"] = Group(name=update.message.text)
        posibole_manager = User.objects.values_list("name", "id")
        options = ["{name}/{id}".format(name=name, id=id)
                   for name, id in posibole_manager]

        markup = GeneralKeyboard(option_list=options).markup
        update.message.reply_text('OK, select group manager please',
                                  reply_markup=markup)

        return STATES.ADD_GROUP_MANAGER

    def set_manager_and_ask_for_type(self, bot, update, chat_data):
        self.logger.debug("got message: %s", update.message.text)
        group = chat_data["group"]
        id = int(update.message.text.split("/")[-1])
        selected_user = User.objects(id=id).first()
        if selected_user is None:
            update.message.reply_text(
                emojize(':shit:Not exist please select from the '
                        'keyboard:shit:', use_aliases=True))
            return
        group.manager = selected_user
        group.manager.is_manager = True

        markup = GeneralKeyboard(option_list=self.GROUP_TYPES).markup
        update.message.reply_text('OK, what kind of group?',
                                  reply_markup=markup)

        return STATES.ADD_GROUP_TYPE

    def set_group_type_and_ask_for_items(self, bot, update, chat_data):
        message = update.message

        if message.text not in self.GROUP_TYPES:
            markup = GeneralKeyboard(option_list=self.GROUP_TYPES).markup
            message.reply_text(
                emojize(
                    "You can't:unamused:, Please select from the keyboard",
                    use_aliases=True),
                reply_markup=markup)
            return

        group = chat_data["group"]
        group.type = message.text

        message.reply_text(emojize(":thumbsup:", use_aliases=True))

        markup = GeneralKeyboard(
            option_list=self.posibole_items(group) + ["Remove", "Done"]).markup
        message.reply_text(
            emojize("Now lets add {type}:boom:".format(type=group.type),
                    use_aliases=True),
            reply_markup=markup)

        return STATES.ADD_GROUP_ITEMS

    def add_group_items(self, bot, update, chat_data):
        group = chat_data["group"]
        message_text = update.message.text
        if message_text == "Remove":
            update.message.reply_text(emojize(":thumbsup:", use_aliases=True))
            if len(group.items) != 0:
                group.items.pop()

            self.send_group_items(group, update)
            return

        if message_text == "Done":
            markup = ManuKeyboard(admin=chat_data["admin"].is_admin,
                                  manager=chat_data["admin"].is_manager).markup
            update.message.reply_text(emojize(":thumbsup:", use_aliases=True),
                                      reply_markup=markup)

            group.manager.save()
            group.save()
            chat_data.clear()
            self.update_group_manager_keyboard(bot, group.manager, group.name)
            return STATES.END

        if message_text not in self.posibole_items(group):
            update.message.reply_text(
                emojize('This option is not possible:tired_face:',
                        use_aliases=True))
            return

        id = int(message_text.split("/")[-1]) if group.type == "Users" \
            else message_text
        item = None

        if group.type == "Users":
            item = User.objects(id=id).first()

        if group.type == "Groups":
            item = Group.objects(name=id).first()

        if item is None:
            update.message.reply_text(
                emojize(':shit:Not exist please select from the '
                        'keyboard:shit:', use_aliases=True))
            return

        group.items.append(item)
        self.send_group_items(group, update)

    def send_group_items(self, group, update):
        items = "\n".join([':dizzy: {name}'.format(name=item.name)
                           for item in group.items])

        markup = GeneralKeyboard(
            option_list=self.posibole_items(group) + ["Remove", "Done"]).markup
        update.message.reply_text(
            emojize('GROUP CONTAINS:\n%s' % items, use_aliases=True),
            reply_markup=markup)

    def posibole_items(self, group):
        posible_items = []

        if group.type == "Groups":
            all_names = Group.objects.values_list("name")
            selcted_names = [item.name for item in group.items]
            posible_items = [name for name in all_names
                             if name not in selcted_names]

        if group.type == "Users":
            all_users = User.objects.values_list("id", "name")
            selcted_ids = [item.id for item in group.items]
            manager_id = group.manager.id
            posible_items = ["{name}/{id}".format(name=name, id=id)
                             for id, name in all_users
                             if id not in selcted_ids and
                             id != manager_id]

        return posible_items

    def update_group_manager_keyboard(self, bot, manager, group_name):
        markup = ManuKeyboard(admin=manager.is_admin,
                              manager=manager.is_manager).markup
        bot.send_message(chat_id=manager.id,
                         text='From now on you are manager of {group_name}'.
                         format(group_name=group_name),
                         reply_markup=markup)
