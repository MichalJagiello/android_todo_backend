
from mongoengine import (connect,
                         Document,
                         EmbeddedDocument)

from mongoengine.fields import (DateTimeField,
                                IntField,
                                StringField,
                                BooleanField,
                                EmailField,
                                EmbeddedDocumentListField,)

from passlib.apps import custom_app_context

connect('heroku_wldq7xdd', host="mongodb://app_wielo:app_wielo@ds055855.mongolab.com:55855/heroku_wldq7xdd")


class Event(EmbeddedDocument):
    """
    The Event model
    """
    title = StringField(required=True)
    time = DateTimeField(required=True)
    all_day_event = BooleanField(required=False, default=True)
    
    @classmethod
    def create(cls, title, time, all_day_event=True):
        """
        Create an event
        """
        e = Event(title, time, all_day_event)
        e.save()
        return e

    @classmethod
    def remove(cls, object_id):
        """
        Delete an event
        """
        event = Event.objects(id=object_id).first()
        event.delete()

    @classmethod
    def get(cls, object_id):
        """
        Get the event
        """
        return Event.objects(id=object_id).first()


class User(Document):
    """
    User document
    """
    email = EmailField(required=True)
    password = StringField(required=True)
    events = EmbeddedDocumentListField(Event)

    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)


    @classmethod
    def get(cls, email):
        return User.objects(email=email).first()