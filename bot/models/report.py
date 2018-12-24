from mongoengine import Document, EmbeddedDocumentListField, DateTimeField

from models.status import Status


class Report(Document):
    date = DateTimeField(primary_key=True)
    statuses = EmbeddedDocumentListField(Status, default=[])
