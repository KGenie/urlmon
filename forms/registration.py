from wtforms.form import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Length, Email, Required, EqualTo,\
        ValidationError

class RegistrationForm(Form):

    first_name = TextField('First Name', [Length(min=4, max=25)])
    last_name = TextField('Last Name', [Length(min=4, max=25)])
    email = TextField('Email/login', [Email()])
    password = PasswordField('Password', [Required()])
    confirm  = PasswordField('Repeat Password', [EqualTo('password', 
        message="Doesn't match")])


    def validate_email(form, field):
        if not hasattr(form, '_user_service'):
            raise Exception(
            'The controller must set the ''_user_service'' attribute with an user service instance bound to the current request')

        if form._user_service.exists(field.data):
            raise ValidationError('An user with that email is already registered')
