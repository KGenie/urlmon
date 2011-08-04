from wtforms.form import Form
from wtforms.fields import TextField, SelectField
from wtforms.validators import Length, URL
from services.tracker_group import TrackerGroupService

class TrackerForm(Form):

    name = TextField('Name', [Length(min=4, max=25)])
    url = TextField('URL to track', [URL()])
    frequency = SelectField('Frequency to check', choices=[('5', '5 minutes'),
        ('10', '10 minutes'), ('20', '20 minutes'), ('40', '40 minutes')])
    tracker_groups = SelectField('Tracker group', choices=[])
