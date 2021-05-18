import datetime


class ErrorResponse:

    def __init__(self, error, message):
        self.timestamp = datetime.datetime.now()
        self.error = error
        self.message = message
        self.success = str(False)
