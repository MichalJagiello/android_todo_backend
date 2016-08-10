__author__ = 'michal'

import logging

from functools import wraps
from flask import request, Response

from models import User as UserModel

def check_auth(email, password):
    user = UserModel.get(email)
    logging.info(UserModel.objects())
    for u in UserModel.objects():
        logging.info(u.email)
    if user is None or not user.verify_password(password):
        return False
    request.user = user
    return True


def check_token(token):
    #TODO fix it
    request.user = UserModel.objects()[0]
    return True


def requires_login(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth = request.authorization
        logging.info(auth)
        if not auth or check_auth(auth.username,
                                  auth.password) is False:
            return Response('Could not verify your access level for that URL.\n'
                            'You have to login with proper credentials', 401,
                            {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return function(*args, **kwargs)
    return decorated


def requires_token(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None or check_token(token) is False:
            return Response(401)
        return function(*args, **kwargs)
    return decorated