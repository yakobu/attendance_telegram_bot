from datetime import datetime

from emoji import emojize
from telegram import ParseMode
from telegram.ext import (RegexHandler,
                          CallbackQueryHandler,
                          MessageHandler,
                          Filters)

from .abstarct import ConversationType
from models import Status, Report, User
from handlers.conversation.consts import HERE, NOT_HERE, STATES
from keyboards import AttendanceKeyboard, ManuKeyboard, NotHereRasonsKeyboard


class SetStatus(ConversationType):
    """Set User status."""
    @property
    def entry_points(self):
        return [
            RegexHandler(pattern="Set Status",
                         callback=self.send_status_keyboard),
            CallbackQueryHandler(pattern=HERE,
                                 callback=self.mark_user_as_present),
            CallbackQueryHandler(pattern=NOT_HERE,
                                 callback=self.send_not_here_reason_keyboard),
        ]

    @property
    def states(self):
        return {
            STATES.STATUS: [
                CallbackQueryHandler(pattern=HERE,
                                     callback=self.mark_user_as_present),
                CallbackQueryHandler(pattern=NOT_HERE,
                                     callback=self.send_not_here_reason_keyboard)],
            STATES.REASON: [
                MessageHandler(filters=Filters.all,
                               callback=self.save_not_here_reason)],
        }

    def send_status_keyboard(self, bot, update):
        """Triggered by set status message

        Send as a response status keyboard.
        """
        self.logger.debug("got message: %s", update.message.text)

        attendance_message = emojize(
            "Have a nice day:innocent: what is your status:interrobang:",
            use_aliases=True)
        update.message.reply_text(attendance_message,
                                  reply_markup=AttendanceKeyboard.markup())

        return STATES.STATUS

    def mark_user_as_present(self, bot, update):
        """Save User status has present."""
        chat = update.callback_query.message.chat
        user = User.objects(id=chat.id).first()
        status = Status(state=HERE,
                        reason="Present",
                        user_id=chat.id,
                        user_name=user.name)

        Report.objects.add_status(date=datetime.now().date(), status=status)

        bot.edit_message_text(
            chat_id=chat.id,
            message_id=update.callback_query.message.message_id,
            text=emojize("*Here* :wink:", use_aliases=True),
            parse_mode=ParseMode.MARKDOWN)

        reply_markup = ManuKeyboard(admin=user.is_admin,
                                    manager=user.is_manager).markup

        update.callback_query.message. \
            reply_text(emojize(":thumbsup:", use_aliases=True),
                       reply_markup=reply_markup)

        return STATES.END

    def send_not_here_reason_keyboard(self, bot, update):
        """Send all reasons for not here message."""
        bot.edit_message_text(
            chat_id=update.effective_user.id,
            message_id=update.callback_query.message.message_id,
            text=emojize("*Not Here*:worried::question::question:",
                         use_aliases=True), parse_mode=ParseMode.MARKDOWN)

        markup = NotHereRasonsKeyboard().markup
        update.callback_query.message.reply_text('why?',
                                                 reply_markup=markup)

        return STATES.REASON

    def save_not_here_reason(self, bot, update):
        """Save user state as 'not here' with given reason."""
        chat = update.message.chat
        user = User.objects(id=chat.id).first()
        status = Status(state=NOT_HERE,
                        reason=update.message.text,
                        user_id=chat.id,
                        user_name=user.name)

        Report.objects.add_status(date=datetime.now().date(), status=status)

        reply_markup = ManuKeyboard(admin=user.is_admin,
                                    manager=user.is_manager).markup
        message = emojize('got it!! thanks :punch:', use_aliases=True)
        update.message.reply_text(message)

        update.message.reply_text(text=emojize(":thumbsup:", use_aliases=True),
                                  reply_markup=reply_markup)

        return STATES.END
