import datetime
from mongoengine import (EmbeddedDocument,
                         ReferenceField,
                         StringField,
                         DateTimeField)

from models.user import User


class Status(EmbeddedDocument):
    user = ReferenceField(User)
    state = StringField()
    reason = StringField()
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
