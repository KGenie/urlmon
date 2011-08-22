from wtforms.form import Form
from wtforms.fields import TextField, TextAreaField, HiddenField
from wtforms.validators import Length
from app_components.fields import HiddenIntegerField

class TrackerGroupForm(Form):

    id = HiddenIntegerField()
    name = TextField('Name', [Length(min=4, max=25)])
    comment = TextAreaField('Comments', [Length(max=550)])
