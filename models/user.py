from app_components.model import Model

class User(Model):

    def __init__(self, username=None, password=None, full_name=None,
            roles=None, last_login=None):
        
        self.username = username
        self.password = password
        self.full_name = full_name
        self.roles = roles or ['normal']
        self.last_login = last_login
