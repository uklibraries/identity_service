class ArkConverter:
    regex = "[0-9]{5}/[0-9bcdfghjkmnpqrstvwxz]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
