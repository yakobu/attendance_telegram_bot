import datetime
from mongoengine import (EmbeddedDocument,
                         StringField,
                         DateTimeField, IntField)


class Status(EmbeddedDocument):
    user_id = IntField()
    user_name = StringField(max_length=200, required=True)
    state = StringField()
    reason = StringField()
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
