from wtforms import Form, TextField, PasswordField

class LoginForm(Form):
    username = TextField('User')
    password = PasswordField('Password')
