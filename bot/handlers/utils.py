from functools import wraps

from models import User


def restricted_for_admin(method):
    @wraps(method)
    def wrapped(self, bot, update, chat_data, *args, **kwargs):
        user_id = update.effective_user.id
        user = User.objects(id=user_id).first()

        if user is not None and user.is_admin:
            chat_data["admin"] = user
            return method(self, bot, update, chat_data, *args, **kwargs)

        print("Unauthorized admin access denied for {}.".format(user_id))

    return wrapped


def restricted_for_manager(method):
    @wraps(method)
    def wrapped(self, bot, update, chat_data, *args, **kwargs):
        user_id = update.effective_user.id
        user = User.objects(id=user_id).first()

        if user is not None and user.is_manager:
            chat_data["manager"] = user
            return method(self, bot, update, chat_data, *args, **kwargs)

        print("Unauthorized manager access denied for {}.".format(user_id))

    return wrapped
