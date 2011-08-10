from wtforms.form import Form
from wtforms.fields import TextField, SelectField, HiddenField
from wtforms.validators import Length, URL, Required
from services.tracker_group import TrackerGroupService
from app_components.fields import HiddenIntegerField

class TrackerForm(Form):

    id = HiddenIntegerField()
    name = TextField('Name', [Length(min=4, max=25)])
    url = TextField('URL to track', [URL()])
    css_selector = TextField('CSS Selector', [Required()])
    frequency = SelectField('Frequency to check', choices=[('5', '5 minutes'),
        ('10', '10 minutes'), ('20', '20 minutes'), ('40', '40 minutes')])
    tracker_group_id = SelectField('Tracker group', choices=[], coerce=int)
