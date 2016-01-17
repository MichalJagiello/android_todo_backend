
from mongoengine import (connect,
                         Document)

from mongoengine.fields import (DateTimeField,
                                IntField,
                                StringField)

connect('aplikacje_wielowarstwowe')


class Event(Document):
    """
    The Event model
    """
    title = StringField(required=True)
    time = DateTimeField(required=True)
    description = StringField()
    
    @classmethod
    def create(cls, title, time, description=None):
        """
        Create an event
        """
        e = Event(title, time, description)
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
