
class FourDigitYear:
    regex = '[0_9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value
