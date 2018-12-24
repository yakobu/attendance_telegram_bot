from attrdict import AttrDict
from telegram.ext import ConversationHandler

STATES = AttrDict({
    "STATUS": 0,
    "REASON": 1,
    "INSERT_NAME": 2,
    "INSERT_PASSWORD": 3,
    "ADD_GROUP_NAME": 4,
    "ADD_GROUP_TYPE": 5,
    "END": ConversationHandler.END
})

HERE = "Here"
NOT_HERE = "Not Here"
