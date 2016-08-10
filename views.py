from flask import abort, jsonify, request
from flask_restful import Resource, reqparse

import logging

from datetime import datetime

from mongoengine.errors import ValidationError

from models import Event as EventModel
from models import User as UserModel

from decorators import requires_login, requires_token

class Event(Resource):
    def get(self, event_id):
        logging.info('Get event with %s id' % event_id)
        logging.info(EventModel.objects)
        event = EventModel.get(event_id)
        if not event:
            abort(400)
        return event.to_json()

    def put(self, event_id):
        logging.info('Update an event with %s id' % event_id)
        if not request.form or \
           not request.form.get('title') or \
           not request.form.get('time'):
            logging.error("Invalid data parameters")
            abort(400)
        event = EventModel.get(event_id)
        if not event:
            abort(400)
        event['title'] = request.form.get('title')
        event['time'] = datetime.fromtimestamp(int(request.form.get('time')))
        event['description'] = request.form.get('description')
        event.save()
        return event.to_json()

    def delete(self, event_id):
        logging.info('Delete en event with %s id' % event_id)
        EventModel.remove(event_id)


class Events(Resource):
    def get(self):
        logging.info('Get events list')
        return {'events': EventModel.objects().to_json()}

    def post(self):
        logging.info('Create an event')
        if not request.form or \
           not request.form.get('title') or \
           not request.form.get('time'):
            logging.error("Invalid data parameters")
            abort(400)
        e = EventModel.create(request.form['title'],
                              datetime.fromtimestamp(int(request.form['time'])),
                              request.form.get('description'))
                              
        e.save()
        
        return e.to_json()


class User(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, location='json', required=True)
        self.reqparse.add_argument('password', type=str, location='json', required=True)
        super(User, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        email = args.get('email')
        password = args.get('password')
        if UserModel.get(email) is not None:
            abort(400, 'User with given mail exists')
        user = UserModel(email = email)
        user.hash_password(password)
        try:
            user.save()
        except ValidationError as err:
            logging.info(err.errors)
            abort(400, str(err.errors))
        return jsonify({'email': user.email})

    @requires_login
    def get(self):
        logging.info(request.user.email)