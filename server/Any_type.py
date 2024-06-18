from werkzeug.routing import BaseConverter

class AnyConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(AnyConverter, self).__init__(url_map)
        self.items = items

    def to_python(self, value):
        if value in self.items:
            return value
        else:
            raise ValueError()

    def to_url(self, value):
        return value