import logging
from models.user import User
from app_components.service import Service
from storage import StorageService


__logger = logging.getLogger('services.user')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


class UserService(StorageService):

    entity = User

    def authenticate(self, email, password):
        return self.session.query(User).\
                filter(User.email == email).\
                filter(User.password == password).first()



    def exists(self, email):
        debug('Checking if email %s exists' % email)
        return self.session.query(User).get(email)
