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
        u = User()
        u.email = email
        u.password = password
        ret = self.session.query(User).\
                filter(User.email == u.email).\
                filter(User._pass == u.password).first()
        if ret:
            self.session.refresh(ret)
            self.session.expunge(ret)
        return ret


    def exists(self, email):
        debug('Checking if email %s exists' % email)
        return bool(self.session.query(User).\
                filter(User.email == email).all())
