from wtforms.form import Form
from wtforms.fields import TextField, TextAreaField
from wtforms.validators import Length

class TrackerGroupForm(Form):

    name = TextField('Name', [Length(min=4, max=25)])
    comment = TextAreaField('Comments')
