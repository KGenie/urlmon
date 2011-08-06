from wtforms import Form, TextField, PasswordField
from wtforms.validators import ValidationError
from models.user import User

class LoginForm(Form):
    # TODO place the email validator
    email = TextField('Email')
    password = PasswordField('Password')

     
    def validate_password(form, field):
        if not hasattr(form, '_user_service'):
            raise Exception(
            'The controller must set the ''_user_service'' attribute with an user service instance bound to the current request')

        user = User()
        form.populate_obj(user)
        if not form._user_service.authenticate(user):
            raise ValidationError('Invalid email or password')
