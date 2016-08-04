class Locator(object):
    dims = []

    def __init__(self):
        self._preds = []

    def add_pred(self, dim, value):
        # @todo: Check for invalid dims
        self._preds.append((dim, value))

    def __str__(self):
        return ','.join(['%s:%s' % p for p in self._preds])
