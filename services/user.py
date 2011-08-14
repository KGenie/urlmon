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

    @classmethod
    def authenticate(cls, email, password):
        for u in cls.get_all():
            if unicode(u.email) == unicode(email):
                if unicode(u.password) == unicode(password):
                    return u
                return None


    @classmethod
    def stub_data(cls):
        cls.insert(User(email='tpadilha84@gmail.com', first_name='Thiago',
            last_name='Padilha', password='123', roles=['admin']))


    @classmethod
    def exists(cls, email):
        l = list(u for u in cls.get_all() if\
                unicode(u.email) == unicode(email))
        return len(l)
