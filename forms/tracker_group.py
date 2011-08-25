from wtforms.form import Form
from wtforms.fields import TextField, TextAreaField, HiddenField
from wtforms.validators import Length, ValidationError
from app_components.fields import HiddenIntegerField

class TrackerGroupForm(Form):

    id = HiddenIntegerField()
    name = TextField('Name', [Length(min=4, max=25)])
    comment = TextAreaField('Comments', [Length(max=550)])


    def validate_name(form, field):
        if not hasattr(form, '_check_name'):
            return

        if not hasattr(form, '_tracker_group_service'):
            raise Exception('Inject dependencies for this form')

        if form._tracker_group_service.exists_with_name(field.data):
            raise ValidationError('You already have a tracker group with that name')
