from wtforms import Form, TextField, PasswordField
from wtforms.validators import ValidationError, Required
from models.user import User

class LoginForm(Form):
    # TODO place the email validator
    email = TextField('Email', [Required()])
    password = PasswordField('Password', [Required()])

     
    def validate_password(form, field):
        if not hasattr(form, '_user_service'):
            raise Exception(
            'The controller must set the ''_user_service'' attribute with an user service instance bound to the current request')

        email = form.email.data
        password = form.password.data
        user = form._user_service.authenticate(email, password)
        if not user:
            raise ValidationError('Invalid email or password')
        setattr(form, '_user', user)
