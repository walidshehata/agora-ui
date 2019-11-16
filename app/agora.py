import requests
import logging as log
import json

from .models import User, load_user
from . import db


def http_request(url, headers={}, data=None, method='get', timeout=3, token=None, verify_ssl=False):

    if token:
        headers['Authorization'] = 'JWT {}'.format(token)

    try:
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method.lower() == 'post':
            response = requests.post(url, data=json.dumps(data), headers=headers, timeout=timeout)
        else:
            response = None
    except requests.ConnectTimeout:
        log.error('Connection time out while connecting to {}. '
                  'Please check connectivity with backend'.format(url))
        return False
    except requests.ConnectionError:
        log.error('Connection error while connecting to {}. '
                  'Please check connectivity with backend.'.format(url))
        return False
    except requests.HTTPError:
        log.error('Connection error while connecting to {}. '
                  'Please check connectivity with backend.'.format(url))
        return False
    except Exception as error:
        log.error('An unexpected error while connecting to {} - '
                  'Exception: {}'.format(url, error.__class__.__name__))
        return False

    return response


class AuthClient(object):

    backend_ip = '0.0.0.0'
    backend_port = '80'

    def __init__(self, app=None, timeout=3):
        app = app
        self.timeout = timeout

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.backend_ip = app.config['BACKEND_IP']
        self.backend_port = app.config['BACKEND_PORT']

    def authenticate(self, username, password):
        auth_url = 'http://{}:{}/auth'.format(self.backend_ip, self.backend_port)
        headers = {'Content-Type': 'application/json'}
        data = {'username': username, 'password': password}

        result = http_request(auth_url, method='post', data=data, headers=headers, timeout=self.timeout)

        if result.status_code == 200 and 'access_token' in result.json():
            data = result.json()
            user = self.get_user(username, data['access_token'])
            return user
        else:
            log.info('Error authenticating user: {}, bad username or password'.format(username))
            return False

    def get_user(self, username, jwt):
        user_info_url = 'http://{}:{}/secure'.format(self.backend_ip, self.backend_port)
        result = http_request(user_info_url, token=jwt, timeout=self.timeout)

        if result.status_code == 200:
            user_info = result.json()
            user = load_user(user_info['username'])
            if user:
                return user
            else:
                user = User(username=user_info['username'],
                            api_key=jwt, display_name=user_info['display_name'],
                            tenant_id=user_info['tenant_id'], tenant_uuid=user_info['tenant_uuid'])
                db.session.add(user)
                db.session.commit()
                return user
        else:
            log.info('Error get info for user: {}'.format(username))
            return False






