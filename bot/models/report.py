from mongoengine import Document, EmbeddedDocumentListField, DateTimeField, \
    QuerySet

from models.status import Status


class StatusQuerySet(QuerySet):
    def add_status(self, date, status):
        status_exist = self.filter(date=date,
                                   statuses__user_id=status.user_id). \
                           count() > 0

        if status_exist:
            # Remove existing statuses
            self.filter(date=date). \
                update(pull__statuses__user_id=status.user_id)

        # Add the required status
        self.filter(date=date).update(add_to_set__statuses=status, upsert=True)

    def get_awesome(self):
        return self.aggregate({"$unwind": "$statuses"},
                              {"$group":
                                   {"_id": "$statuses.state",
                                    "users": {"$push": "$statuses.user"}}
                               })


class Report(Document):
    meta = {'queryset_class': StatusQuerySet}

    date = DateTimeField(primary_key=True)
    statuses = EmbeddedDocumentListField(Status, default=[])
