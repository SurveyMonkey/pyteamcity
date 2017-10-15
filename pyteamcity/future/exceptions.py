class Error(Exception):
    pass


class MultipleObjectsReturned(Error):
    pass


class InvalidLocatorDimension(Error):
    pass


class IllegalOperation(Error):
    pass


class ArtifactSizeExceeded(Error):
    pass


class ArtifactNotFound(Error):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return 'Artifact not found: %s' % self.path


class ChangeDetailsNotFound(Error):
    def __init__(self, id):
        self.iud = id

    def __str__(self):
        return 'Change details not found: %s' % self.id


class HTTPError(Error):
    def __init__(self, status_code, reason, text):
        self.status_code = status_code
        self.reason = reason
        self.text = text

    def __str__(self):
        return self.reason or self.text


class UnauthorizedError(HTTPError):
    pass
