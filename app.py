from flask import Flask
from flask_restful import Api

from views import Event as EventView
from views import Events as EventsView
from views import User as UserView

import logging

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level=logging.DEBUG)

api.add_resource(EventsView, '/api/events/')
api.add_resource(EventView, '/api/events/<string:event_id>/')
api.add_resource(UserView, '/api/users/')

if __name__ == "__main__":
    app.run(debug=True)
