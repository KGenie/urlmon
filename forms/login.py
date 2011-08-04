from wtforms import Form, TextField, PasswordField

class LoginForm(Form):
    # TODO place the email validator
    email = TextField('Email')
    password = PasswordField('Password')
