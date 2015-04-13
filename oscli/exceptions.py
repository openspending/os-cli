class InvalidSessionError(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'Invalid session. Please reauth with the auth service.'


class InvalidCredentials(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'Your credentials are invalid. Please check your api_key and token.'
