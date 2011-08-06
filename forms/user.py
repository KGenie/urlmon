from wtforms.form import Form
from wtforms.fields import TextField, TextAreaField, HiddenField
from wtforms.validators import Length, Email

class UserForm(Form):

    id = HiddenField()
    email = TextField('Email', [Email()])
    first_name = TextField('First name', [Length(min=4, max=25)])
    last_name = TextField('Last name', [Length(min=4, max=25)])
