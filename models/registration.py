from datetime import datetime
from hashlib import sha1
from app_components.model import Model

class Registration(Model):

    def __init__(self, user=None):
        if user:
            self.user = user
        

    @property
    def user(self):
        return self._user
        

    @user.setter
    def user(self, value):
        h = sha1()
        h.update(value.email)
        h.update(str(datetime.now()))
        self.reg_id = h.hexdigest()
        self._user = value

