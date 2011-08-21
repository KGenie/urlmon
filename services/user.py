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
        ret = self.session.query(User).\
                filter(User.email == email).\
                filter(User.password == password).first()
        self.session.refresh(ret)
        self.session.expunge(ret)
        return ret



    def exists(self, email):
        debug('Checking if email %s exists' % email)
        return bool(list(self.session.query(User).get(email)))
