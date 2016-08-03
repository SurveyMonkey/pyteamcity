class Error(Exception):
    pass


class MultipleObjectsReturned(Error):
    pass


class InvalidLocatorDimension(Error):
    pass


class HTTPError(Error):
    def __init__(self, status_code, msg, text):
        self.status_code = status_code
        self.msg = msg
        self.text = text

    def __str__(self):
        return self.msg


class UnauthorizedError(HTTPError):
    pass
