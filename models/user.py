from app_components.model import Model, TableModel
from forms.user import UserForm
from hashlib import sha512

class User(Model):

    def __init__(self, email=None, first_name=None, last_name=None,  
            password=None, full_name=None, roles=None, last_login=None):

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.roles = roles or ['normal']
        self.last_login = last_login


    @property
    def password(self):
        return self._pass


    @password.setter
    def password(self, value):
        if value:
            h = sha512()
            h.update(value)
            self._pass = h.digest()
        else:
            self._pass = value




class UserTable(TableModel):
    form = UserForm
