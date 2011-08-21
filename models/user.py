from app_components.model import Model, TableModel
from forms.user import UserForm

class User(Model):

    def __init__(self, email=None, first_name=None, last_name=None,  
            password=None, full_name=None, roles=None, last_login=None):

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.roles = roles or ['normal']
        self.last_login = last_login


class UserTable(TableModel):

    form = UserForm
