class InvalidSessionError(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'Invalid session. Please reauth with the auth service.'


class InvalidCredentials(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'Your credentials are invalid. Please check your api_key and token.'


class ConfigNotFoundError(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'Your credentials are invalid. Please check your api_key and token.'


class ConfigValueError(Exception):
    def __init__(self, msg=None, required=()):
        self.msg = msg or ('This command requires the following '
                           'config keys: {0}'.format(required))
