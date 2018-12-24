from functools import wraps

from models import User


def restricted_for_admin(method):
    @wraps(method)
    def wrapped(self, bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        user = User.objects(id=user_id).first()

        if user is not None and user.is_admin:
            return method(self, bot, update, user, *args, **kwargs)

        print("Unauthorized access denied for {}.".format(user_id))

    return wrapped
