from wtforms import HiddenField

class HiddenIntegerField(HiddenField):

    def __init__(self, *args, **kwargs):
        super(HiddenIntegerField, self).__init__(*args, **kwargs)
        self.type = 'HiddenField'
    
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        else:
            return self.data and unicode(self.data) or u'0'

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                raise ValueError(self.gettext(u'Not a valid integer value'))
