
class Todo:
    def __init__(self, name: str, params: dict):
        self.name = name
        self.params = params

    def __repr__(self):
        return "%s(name=%r, params=%r)" % (self.__class__.__name__, self.name, self.params)

    def __str__(self):
        return "%s %r: params=%r" % (self.__class__.__name__, self.name, self.params)
