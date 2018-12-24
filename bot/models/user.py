import datetime
from mongoengine import (Document,
                         IntField,
                         StringField,
                         DateTimeField,
                         BooleanField)


class User(Document):
    id = IntField(primary_key=True)
    name = StringField(max_length=200, required=True)
    is_admin = BooleanField(default=False)
    is_manager = BooleanField(default=False)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
