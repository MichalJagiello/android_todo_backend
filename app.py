from flask import Flask
from flask_restful import Api

from views import Event as EventView
from views import Events as EventsView

import logging

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level=logging.DEBUG)

api.add_resource(EventsView, '/')
api.add_resource(EventView, '/<string:event_id>/')

if __name__ == "__main__":
    app.run(debug=True)
