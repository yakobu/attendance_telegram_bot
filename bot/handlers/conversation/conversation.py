from emoji import emojize
from telegram.ext import ConversationHandler, MessageHandler, Filters


class Conversation(ConversationHandler):
    """"""

    def __init__(self, types, **kwargs):
        entry_points = []
        states = {}
        fallbacks = [
            MessageHandler(filters=Filters.all,
                           callback=self.unhandled_message)
        ]

        for conversation_type in types:
            conversation_obj = conversation_type()
            entry_points.extend(conversation_obj.entry_points)
            states.update(conversation_obj.states)

        super(Conversation, self).__init__(entry_points=entry_points,
                                           states=states,
                                           fallbacks=fallbacks,
                                           **kwargs)

    def unhandled_message(self, bot, update):
        """"""
        message = emojize('This message cannot be handled :confused:',
                          use_aliases=True)
        update.message.reply_text(message)
