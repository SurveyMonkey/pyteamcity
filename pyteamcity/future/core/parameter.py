class Parameter(object):
    def __init__(self, ptype=None, value=None):
        self.ptype = ptype
        self.value = value

    def __repr__(self):
        return '<%s.%s: ptype=%r value=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.ptype,
            self.value)
