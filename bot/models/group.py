import datetime
from mongoengine import (StringField,
                         DateTimeField,
                         DynamicField,
                         ListField,
                         Document, ReferenceField)

from models import User


class Group(Document):
    name = StringField(primary_key=True, max_length=200, required=True)
    manager = ReferenceField(User, required=True)
    type = StringField(regex="^Groups$|^Users$", required=True)
    items = ListField(DynamicField())
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
