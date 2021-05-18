

class InvalidTokenException(Exception):
    def __init__(self, message):
        self.message = message


class ExpiredTokenException(Exception):
    def __init__(self, message):
        self.message = message


class NotAdminException(Exception):
    def __init__(self, message):
        self.message = message
