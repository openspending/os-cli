class InvalidSessionError(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'Invalid session. Please reauth with the auth service.'