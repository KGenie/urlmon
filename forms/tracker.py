from wtforms.form import Form
from wtforms.fields import TextField, SelectField, HiddenField, TextAreaField
from wtforms.validators import Length, URL, Required
from services.tracker_group import TrackerGroupService
from app_components.fields import HiddenIntegerField

class TrackerForm(Form):

    id = HiddenIntegerField()
    name = TextField('Name', [Length(min=4, max=25)])
    url = TextField('URL to track', [URL()])
    css_selector = TextField('CSS Selector', [Required()])
    frequency = SelectField('Frequency to check', choices=[(5, '5 seconds'),
        (10, '10 seconds'), (20, '20 seconds'), (40, '40 seconds')],
        coerce=int)
    tracker_group_id = SelectField('Tracker group', choices=[], coerce=int)
