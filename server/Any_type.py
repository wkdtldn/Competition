from werkzeug.routing import BaseConverter

class AnyConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(AnyConverter, self).__init__(url_map)
        self.items = items

    def to_python(self, value):
        for item in self.items:
            try:
                return item(value)
            except ValueError:
                continue
        raise ValueError(f"Value '{value}' does not match any allowed types {self.items}")

    def to_url(self, value):
        return str(value)