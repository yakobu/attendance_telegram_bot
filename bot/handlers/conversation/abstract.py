from emoji import emojize
from telegram.ext import ConversationHandler, MessageHandler, Filters


class Conversation(ConversationHandler):
    """"""
    @property
    def start_triggers(self):
        raise NotImplementedError("You have to set start_triggers")

    @property
    def states_options(self):
        raise NotImplementedError("You have to set states_options")

    @property
    def fallbacks_oprtions(self):
        return [
            MessageHandler(filters=Filters.all,
                           callback=self.unhandled_message)
        ]

    def __init__(self, **kwargs):
        super(Conversation, self).__init__(entry_points=self.start_triggers,
                                           states=self.states_options,
                                           fallbacks=self.fallbacks_oprtions,
                                           **kwargs)

    def unhandled_message(self, bot, update):
        """"""
        message = emojize('This message cannot be handled :confused:',
                          use_aliases=True)
        update.message.reply_text(message)
