from wtforms.form import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Length, Email, Required, EqualTo

class RegistrationForm(Form):

    first_name = TextField('First Name', [Length(min=4, max=25)])
    last_name = TextField('Last Name', [Length(min=4, max=25)])
    email = TextField('Email/login', [Email()])
    password = PasswordField('Password', [Required()])
    confirm  = PasswordField('Repeat Password', [EqualTo('password', 
        message="Doesn't match")])
