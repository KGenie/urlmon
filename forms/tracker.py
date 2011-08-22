from wtforms.form import Form
from wtforms.fields import TextField, SelectField, HiddenField, TextAreaField
from wtforms.validators import Length, URL, Required
from app_components.fields import HiddenIntegerField

class TrackerForm(Form):

    id = HiddenIntegerField()
    name = TextField('Name', [Length(min=4, max=25)])
    comment = TextAreaField('Comments', [Length(max=550)])
    url = TextField('URL to track', [URL()])
    css_selector = TextField('CSS Selector', [Required()])
    frequency = SelectField('Frequency to check', choices=[(5, '5 seconds'),
        (60, '1 minute'), (300, '5 minutes'), (600, '10 minutes'), ],
        coerce=int)
    tracker_group_id = SelectField('Tracker group', choices=[], coerce=int)
