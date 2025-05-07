class FourDigitYear:
    regex = '[0-9]{4}'

    ###Define main methods###
    def to_python(self,value):
        return int(value)
    def to_url(self,value):
        return '%04d' % value