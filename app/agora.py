import logging as log

from .models import User
from . import db
from .http import http_request


class AuthClient(object):

    config = None

    def __init__(self, app=None, timeout=3):
        app = app
        self.timeout = timeout

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.config = app.config

    def authenticate(self, username, password):
        auth_url = 'auth/'
        data = {'username': username, 'password': password}

        result = http_request(auth_url, method='post', data=data)

        if result.status_code == 200 and 'access_token' in result.json():
            data = result.json()
            user = self.get_user(username, data['access_token'])
            return user
        else:
            log.info('Error authenticating user: {}, bad username or password'.format(username))
            return False

    @staticmethod
    def register_customer(firstname, lastname, mail, company, mobile, username, password):
        pass
        register_url = 'auth/onboard'
        data = {
            'firstname': firstname,
            'lastname': lastname,
            'company': company,
            'mail': mail,
            'mobile': mobile,
            'username': username,
            'password': password
        }

        result = http_request(register_url, data=data, method='post')
        msg = result.json().get('msg', 'Undefined error')

        if result.status_code == 200:
            log.info(f'New customer registration submitted successfully - PC task id {msg}')
            return True, msg
        else:
            log.error(f'Error in registering a new customer - msg: {msg}')
            return False, msg

    @staticmethod
    def get_user(username, token):
        user_info_url = 'auth/me'
        result = http_request(user_info_url, token=token)

        if result.status_code == 200:
            user_info = result.json()
            user = User.load_user(user_info['id'])
            if user:
                return user
            else:
                user = User(id=user_info['id'],
                            api_key=token,
                            display_name=user_info['display_name'],
                            mail=user_info['mail'],
                            company=user_info['company'],
                            mobile=user_info['mobile'])
                db.session.add(user)
                db.session.commit()
                return user
        else:
            log.info('Error get info for user: {}'.format(username))
            return False






